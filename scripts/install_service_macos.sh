#!/usr/bin/env bash
set -euo pipefail

PLIST_SRC="$(cd "$(dirname "$0")" && pwd)/macos/launchagents/com.story.goal.mcp.plist"
PLIST_DST="${HOME}/Library/LaunchAgents/com.story.goal.mcp.plist"

mkdir -p "${HOME}/Library/LaunchAgents" "${HOME}/Library/Logs"
cp -f "$PLIST_SRC" "$PLIST_DST"

launchctl unload "$PLIST_DST" >/dev/null 2>&1 || true
launchctl load "$PLIST_DST"
launchctl start com.story.goal.mcp

echo "story-goal-mcp loaded. Logs:"
echo "  tail -f \"$HOME/Library/Logs/story-goal-mcp.out\" \"$HOME/Library/Logs/story-goal-mcp.err\""

