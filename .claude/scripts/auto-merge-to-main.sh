#!/bin/bash
# Auto-merge current claude/* branch into main after session completes

set -e

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

# Only run for claude/* branches
if [[ "$BRANCH" != claude/* ]]; then
  exit 0
fi

echo "Auto-merging $BRANCH into main..." >&2

# Fetch latest main
git fetch origin main 2>/dev/null

# Check if there's anything to merge
MERGE_BASE=$(git merge-base HEAD origin/main)
BRANCH_TIP=$(git rev-parse HEAD)

if [ "$MERGE_BASE" = "$BRANCH_TIP" ]; then
  echo "Nothing to merge (branch is behind or equal to main)." >&2
  exit 0
fi

# Switch to main, merge, push
git checkout main 2>/dev/null
git merge --no-ff "$BRANCH" -m "Merge $BRANCH into main" 2>/dev/null
git push origin main 2>/dev/null

# Return to original branch
git checkout "$BRANCH" 2>/dev/null

echo '{"systemMessage": "✅ '"$BRANCH"' を main に自動マージしました"}'
