"""Pull the real contribution calendar from the GitHub GraphQL API into
data/contributions.json. Runs inside the daily Action (GITHUB_TOKEN is
enough) or locally with a classic token that has read:user.

    GITHUB_TOKEN=ghp_... GH_USER=ayush-jena-721 python tools/fetch_github.py
"""
import datetime
import json
import os
import pathlib
import sys
import urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
USER = os.environ.get("GH_USER", "ayush-jena-721")
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "contributions.json"

if not TOKEN:
    sys.exit("GITHUB_TOKEN is not set")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}"""
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json",
             "User-Agent": "profile-readme-sync"},
)
with urllib.request.urlopen(req, timeout=30) as r:
    payload = json.load(r)
if "errors" in payload:
    sys.exit(json.dumps(payload["errors"], indent=2))

cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks = [[{"date": d["date"], "count": d["contributionCount"], "level": LEVEL[d["contributionLevel"]]}
          for d in w["contributionDays"]] for w in cal["weeks"]]
out = {
    "user": USER,
    "total": cal["totalContributions"],
    "from": weeks[0][0]["date"],
    "to": weeks[-1][-1]["date"],
    "source": "GitHub GraphQL contributionCalendar",
    "synced": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "weeks": weeks,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out))
print(f"{USER}: {out['total']} contributions, {len(weeks)} weeks -> {OUT}")
