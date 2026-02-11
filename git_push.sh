#!/usr/bin/env bash

# Load environment variable
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Switch into project folder for git
cd "$SCRIPT_DIR" || exit 1

# Make sure there is a token for push
if [ -z "$GITHUB_TOKEN" ]; then
    source "$SCRIPT_DIR/onsync.env"
fi
    
# Get the url to push to
ORIGIN=$(git config --get remote.origin.url)
PUSH_URL="https://$GITHUB_TOKEN@${ORIGIN#https://}"

# Add and commit
git add .
git commit -m "Update snapshots/"

# Push using token
git push "$PUSH_URL" docker-v5
