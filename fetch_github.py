"""Pull verified numbers from the GitHub GraphQL API into ../data/*.json.

Nothing here estimates or invents. If a field cannot be read it is simply left
out and the cards render a dash instead.

Run locally:  GITHUB_TOKEN=ghp_xxx GH_USER=ayush-jena-721 python tools/fetch_github.py
In Actions:   the workflow passes the built-in token.
"""

import os, json, urllib.request

USER = os.environ.get("GH_USER", "ayush-jena-721")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")

QUERY = """
query($login:String!) {
  user(login:$login) {
    followers { totalCount }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false,
                 orderBy:{field:STARGAZERS, direction:DESC}) {
      totalCount
      nodes {
        stargazerCount
        languages(first:8, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name color } }
        }
      }
    }
    pullRequests { totalCount }
    issues { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}
"""


def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}",
                 "Content-Type": "application/json",
                 "User-Agent": "ayush-os-hud"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def levels(counts):
    """Map raw counts onto 0-4 using the user's own non-zero quartiles, so the
    scale reflects this account rather than an arbitrary constant."""
    nz = sorted(c for c in counts if c > 0)
    if not nz:
        return lambda c: 0
    q = [nz[int(len(nz) * f)] for f in (0.25, 0.5, 0.75)]
    q = [max(1, x) for x in q]

    def lv(c):
        if c <= 0:
            return 0
        if c <= q[0]:
            return 1
        if c <= q[1]:
            return 2
        if c <= q[2]:
            return 3
        return 4
    return lv


def main():
    if not TOKEN:
        raise SystemExit("no GITHUB_TOKEN in the environment - nothing written, "
                         "assets keep their current values")
    d = gql(QUERY, {"login": USER})["user"]
    cal = d["contributionsCollection"]["contributionCalendar"]

    counts, weeks_raw = [], []
    for wk in cal["weeks"]:
        col = [day["contributionCount"] for day in wk["contributionDays"]]
        col += [0] * (7 - len(col))
        weeks_raw.append(col)
        counts += col
    lv = levels(counts)
    weeks = [[lv(c) for c in col] for col in weeks_raw][-53:]
    while len(weeks) < 53:
        weeks.insert(0, [0] * 7)

    first = cal["weeks"][0]["contributionDays"][0]["date"]
    last = cal["weeks"][-1]["contributionDays"][-1]["date"]

    os.makedirs(OUT, exist_ok=True)
    json.dump({"weeks": weeks, "total": cal["totalContributions"],
               "range": f"{first}/{last}", "user": USER},
              open(os.path.join(OUT, "contributions.json"), "w"))

    repos = d["repositories"]
    stars = sum(n["stargazerCount"] for n in repos["nodes"])
    sizes = {}
    for n in repos["nodes"]:
        for e in n["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    tot = sum(sizes.values()) or 1
    langs = [{"name": k, "pct": v * 100 / tot}
             for k, v in sorted(sizes.items(), key=lambda kv: -kv[1])[:6]]

    cc = d["contributionsCollection"]
    stats = {
        "repos": repos["totalCount"],
        "stars": stars,
        "followers": d["followers"]["totalCount"],
        "prs": d["pullRequests"]["totalCount"],
        "issues": d["issues"]["totalCount"],
        "commits": cc["totalCommitContributions"],
        "reviews": cc["totalPullRequestReviewContributions"],
        "contributions": cal["totalContributions"],
        "langs": langs,
    }
    stats["trophies"] = [
        {"k": "REPOSITORIES", "v": f'{stats["repos"]:,}'},
        {"k": "STARS", "v": f'{stats["stars"]:,}'},
        {"k": "FOLLOWERS", "v": f'{stats["followers"]:,}'},
        {"k": "COMMITS", "v": f'{stats["commits"]:,}'},
        {"k": "PULL REQUESTS", "v": f'{stats["prs"]:,}'},
        {"k": "ISSUES", "v": f'{stats["issues"]:,}'},
        {"k": "REVIEWS", "v": f'{stats["reviews"]:,}'},
    ]
    json.dump(stats, open(os.path.join(OUT, "stats.json"), "w"), indent=1)
    print("synced", USER, "-", cal["totalContributions"], "contributions")


if __name__ == "__main__":
    main()
