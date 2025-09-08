#!/bin/bash
# Demo script for Story-Goal MCP
set -e

echo "🎯 Story-Goal MCP Demo"
echo "======================"
echo

echo "1. User Registration & Handshake"
echo "---------------------------------"
python3 story_goal_mcp.py handshake demo-user "Demo Developer"
echo

echo "2. Creating a Goal"
echo "------------------"
GOAL_OUTPUT=$(python3 story_goal_mcp.py create-goal demo-user \
  "Build Task Manager" \
  "Create a productivity app that helps users organize and complete tasks" \
  "Users actively managing 50+ tasks, 90%+ completion rate")
echo "$GOAL_OUTPUT"
GOAL_ID=$(echo "$GOAL_OUTPUT" | grep -o '"id": "[^"]*"' | cut -d'"' -f4)
echo

echo "3. Creating User Stories"
echo "------------------------"
python3 story_goal_mcp.py create-story demo-user \
  "Task Creation Interface" \
  "As a user" \
  "I want to quickly add new tasks" \
  "So that I can capture todos without breaking my workflow" \
  "$GOAL_ID"
echo

python3 story_goal_mcp.py create-story demo-user \
  "Task Priority System" \
  "As a busy professional" \
  "I want to mark tasks as high/medium/low priority" \
  "So that I focus on what matters most" \
  "$GOAL_ID"
echo

python3 story_goal_mcp.py create-story demo-user \
  "Progress Tracking" \
  "As a user" \
  "I want to see my completion statistics" \
  "So that I stay motivated and can improve my productivity" \
  "$GOAL_ID"
echo

echo "4. Viewing Progress"
echo "-------------------"
echo "Goals:"
python3 story_goal_mcp.py list-goals demo-user
echo
echo "Stories:"
python3 story_goal_mcp.py list-stories demo-user
echo

echo "5. User Separation Demo"
echo "-----------------------"
echo "Creating second user workspace:"
python3 story_goal_mcp.py handshake other-user "Other Developer"
python3 story_goal_mcp.py create-goal other-user \
  "Learn Rust Programming" \
  "Become proficient in Rust for systems programming" \
  "Built 3 Rust projects, contributed to open source"
echo
echo "Other user's goals (completely separate):"
python3 story_goal_mcp.py list-goals other-user
echo

echo "✅ Demo Complete!"
echo "=================="
echo "Data persisted in story_goals.db"
echo "Try more commands from README.md"