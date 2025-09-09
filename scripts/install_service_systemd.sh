#!/usr/bin/env bash
set -euo pipefail

UNIT_SRC="$(cd "$(dirname "$0")" && pwd)/linux/systemd/story-goal-mcp.service"
UNIT_DIR="${HOME}/.config/systemd/user"
UNIT_DST="${UNIT_DIR}/story-goal-mcp.service"

mkdir -p "$UNIT_DIR"
cp -f "$UNIT_SRC" "$UNIT_DST"

systemctl --user daemon-reload
systemctl --user enable --now story-goal-mcp.service

echo "story-goal-mcp installed and started."
echo "Check status: systemctl --user status story-goal-mcp.service"
echo "Logs: journalctl --user -u story-goal-mcp.service -f"

