#!/usr/bin/env bash
# Deploy AYUSH OS to your GitHub profile repo.
#
#   ./deploy.sh                      first push, or any later update
#   ./deploy.sh someone-else         deploy under a different username
#
# Run this from inside the ayush-os folder. It never force-pushes and never
# touches anything outside this directory.

set -euo pipefail

USER="${1:-ayush-jena-721}"
REPO="https://github.com/${USER}/${USER}.git"

say() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }

say "pre-flight"
if command -v python3 >/dev/null; then
  python3 tools/check.py || {
    echo
    read -r -p "check.py flagged something. Push anyway? [y/N] " a
    [[ "$a" == "y" || "$a" == "Y" ]] || exit 1
  }
fi

say "git"
if [ ! -d .git ]; then
  git init -q
  git branch -M main
  git remote add origin "$REPO"
  echo "initialised, remote -> $REPO"
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "$REPO"
  echo "existing repo, remote -> $(git remote get-url origin)"
fi

git add -A
if git diff --staged --quiet; then
  echo "nothing to commit"
else
  git commit -q -m "AYUSH OS v7.2 - engineering interface"
  echo "committed"
fi

say "push"
echo "GitHub will ask for your username and a Personal Access Token as the"
echo "password (your account password will not work). Create one at:"
echo "  https://github.com/settings/tokens  ->  scope: repo"
echo
git push -u origin main

say "done"
cat <<EOF
Open  https://github.com/${USER}

Two workflows need one manual kick to populate real data:
  1. https://github.com/${USER}/${USER}/actions
  2. run "sync HUD"            -> real contribution matrix + stat cards
  3. run "contribution snake"  -> creates output/snake-*.svg

Give them a minute each, then hard-refresh your profile.
EOF