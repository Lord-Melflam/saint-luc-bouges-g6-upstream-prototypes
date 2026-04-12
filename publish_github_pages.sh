#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:-Lord-Melflam}"
REPO="${2:-saint-luc-bouges-g6-upstream-prototypes}"
PAGES_PATH="${3:-/}"
COMMIT_MSG="${4:-Update upstream prototypes}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: GitHub CLI (gh) is not installed."
  exit 1
fi

gh auth status >/dev/null

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
python daily_huddle_board.py
python communication_flow.py

if [[ ! -d ".git" ]]; then
  git init -b main
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
    git remote add origin "https://github.com/$OWNER/$REPO.git"
  else
    gh repo create "$OWNER/$REPO" --public --source=. --remote=origin
  fi
fi

git add .
if ! git diff --cached --quiet; then
  git commit -m "$COMMIT_MSG" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
fi

git push -u origin main

if ! gh api "repos/$OWNER/$REPO/pages" >/dev/null 2>&1; then
  gh api -X POST "repos/$OWNER/$REPO/pages" \
    -f "source[branch]=main" \
    -f "source[path]=$PAGES_PATH" >/dev/null
fi

echo "Published."
echo "URL: https://${OWNER,,}.github.io/$REPO/"
