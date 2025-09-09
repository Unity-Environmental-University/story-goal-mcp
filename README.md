# Story-Goal MCP Server

> Part of the LXD MCP Suite — a cohesive set of MCP servers for learning experience design (coaching, Kanban, stories, and optional LLM adapters).

## What it is
Story/Goal MCP server that tracks outcomes (goals) and user stories with phases and progress notes.

## Why it helps
Keeps focus on deliverable outcomes and progress over time; complements Kanban for planning and execution.

A lightweight MCP server that replaces task-focused todo lists with outcome-focused user stories and goals. Track meaningful progress toward user value instead of just checking off tasks.

## 🎯 Philosophy

**Instead of:** "Write authentication tests"  
**Think:** "As a user, I can securely log in so that my data is protected"

Stories carry full context and connect to larger goals, making development more intentional and outcome-driven.

## 🚀 Quick Start

### Installation

```bash
git clone <this-repo>
cd story-goal-mcp
```

No dependencies! Uses Python's built-in SQLite.

### Basic Usage

```bash
# 1. Register as a user (creates isolated workspace)
python3 story_goal_mcp.py handshake your-username "Your Name"

# 2. Create a goal (high-level outcome)
python3 story_goal_mcp.py create-goal your-username \
  "Build User Authentication" \
  "Secure user login/logout with session management" \
  "Users can safely access protected features"

# 3. Create stories toward that goal
python3 story_goal_mcp.py create-story your-username \
  "Secure Login Form" \
  "As a user" \
  "I want to log in with email/password" \
  "So that I can access my personal data"

# 4. View your progress
python3 story_goal_mcp.py list-goals your-username
python3 story_goal_mcp.py list-stories your-username
```

### Install (local PATH)

```bash
bash scripts/install_local.sh
export PATH="$HOME/.local/bin:$PATH"   # add to shell profile for persistence

# Start MCP server from anywhere
story-goal-mcp
```

### Run at Login

macOS (launchd):

```bash
bash scripts/install_service_macos.sh
# Logs:
tail -f "$HOME/Library/Logs/story-goal-mcp.out" "$HOME/Library/Logs/story-goal-mcp.err"
```

Linux (systemd user):

```bash
bash scripts/install_service_systemd.sh
systemctl --user status story-goal-mcp.service
journalctl --user -u story-goal-mcp.service -f
```

## 📋 Commands

### User Management

```bash
# Register/check user state
python3 story_goal_mcp.py handshake <user_key> [name]
```

### Goal Management

```bash
# Create a goal
python3 story_goal_mcp.py create-goal <user_key> <title> <vision> [success_metrics]

# List all goals with story counts
python3 story_goal_mcp.py list-goals <user_key>
```

### Story Management

```bash
# Create a story
python3 story_goal_mcp.py create-story <user_key> <title> <as_a> <i_want> <so_that> [goal_id]

# List stories (all, by goal, or by phase)
python3 story_goal_mcp.py list-stories <user_key> [goal_id] [phase]

# Update story progress (TODO: implement)
python3 story_goal_mcp.py update-story <user_key> <story_id> <phase> <notes>
```

## 🏗️ Data Structure

### Goal
```json
{
  "id": "c420c3ad",
  "title": "Build User Authentication",
  "vision": "Secure login system with session management",
  "success_metrics": "Users can safely access protected features",
  "total_stories": 3,
  "completed_stories": 1,
  "created_at": "2025-09-08T19:18:20.682533"
}
```

### User Story
```json
{
  "id": "33bbaf8b",
  "title": "Secure Login Form",
  "as_a": "As a user",
  "i_want": "I want to log in with email/password",
  "so_that": "So that I can access my personal data",
  "current_phase": "defining",
  "acceptance_criteria": ["Form validates email format", "Password is hashed"],
  "progress_notes": [
    {
      "timestamp": "2025-09-08T19:20:15.123456",
      "phase": "developing",
      "notes": "Started implementing form validation"
    }
  ],
  "goal_id": "c420c3ad"
}
```

## 📈 Story Phases

1. **Defining** - Writing acceptance criteria, understanding requirements
2. **Developing** - Building, coding, implementing  
3. **Validating** - Testing, reviewing, getting feedback
4. **Complete** - Story delivers value to users

## 🔒 User Separation

Each user gets completely isolated data:

```bash
# User A's workspace
python3 story_goal_mcp.py handshake alice "Alice Smith"
python3 story_goal_mcp.py create-goal alice "Build Chat App" "..."

# User B's workspace (completely separate)  
python3 story_goal_mcp.py handshake bob "Bob Jones"
python3 story_goal_mcp.py create-goal bob "E-commerce Site" "..."
```

Data is stored in SQLite with user_key separation ensuring privacy.

## 💡 Usage Patterns

### 1. Sprint Planning
```bash
# Create goal for the sprint
python3 story_goal_mcp.py create-goal alice \
  "Sprint 1: Core Features" \
  "MVP with essential user flows working" \
  "Users can complete primary workflows"

# Break into stories
python3 story_goal_mcp.py create-story alice \
  "User Registration" "As a new user" "I want to create account" "So that I can use the app"

python3 story_goal_mcp.py create-story alice \
  "Dashboard View" "As a user" "I want to see my data" "So that I can track progress"
```

### 2. Feature Development
```bash
# Create focused goal
python3 story_goal_mcp.py create-goal dev123 \
  "Search Functionality" \
  "Fast, accurate search across all content" \
  "Users find what they need in <2 seconds"

# Multiple stories toward same goal
python3 story_goal_mcp.py create-story dev123 \
  "Search API" "As a developer" "I want search endpoint" "So that frontend can query data"

python3 story_goal_mcp.py create-story dev123 \
  "Search UI" "As a user" "I want search box" "So that I can find content quickly"
```

### 3. Bug Fixes as Stories
```bash
python3 story_goal_mcp.py create-story dev123 \
  "Fix Login Redirect" \
  "As a user" \
  "I want to go to intended page after login" \
  "So that my workflow isn't interrupted"
```

## 🆚 vs TodoWrite

| TodoWrite | Story-Goal MCP |
|-----------|----------------|
| "Fix login bug" | "As a user, I want login to redirect properly so that my workflow isn't interrupted" |
| Task-focused | Outcome-focused |
| No context | Full user story context |
| Single user | Multi-user with isolation |
| No goals | Stories roll up to goals |
| Binary done/not-done | Phases: defining → developing → validating → complete |

## 🔌 MCP Protocol Integration

Story-Goal MCP now supports **native MCP protocol** for Claude Code integration!

### Using as MCP Server

```bash
# Start MCP server (communicates via JSON-RPC)
python3 mcp_server.py

# Or use CLI version directly
python3 story_goal_mcp.py handshake your-user "Your Name"
```

### Available MCP Tools

- `story_goal_handshake` - Register/verify user workspace
- `create_goal` - Create outcome-focused goals  
- `create_story` - Create user stories with full context
- `update_story_progress` - Update story phases with notes
- `list_goals` - View goals with progress metrics
- `list_stories` - View stories (all/filtered by goal/phase)
- `get_story_details` - Detailed story view with goal context

### Testing MCP Integration

```bash
# Run comprehensive protocol test
python3 test_mcp_protocol.py

# Expected: All tests pass, ready for Claude integration
```

## 🔮 Future Features

- [x] Link stories to goals automatically ✅ DONE
- [x] Progress updates with notes ✅ DONE  
- [ ] Story dependencies 
- [ ] Time tracking per phase
- [x] MCP protocol integration ✅ DONE
- [ ] Web interface
- [ ] Story templates
- [ ] Acceptance criteria management
- [ ] Story estimation/velocity

## 🛠️ Development

The server is a single Python file with no external dependencies. Uses SQLite for persistence.

### Database Schema
- `users` - User registration and metadata
- `goals` - High-level outcomes users want to achieve  
- `stories` - User stories with full context and progress tracking

### Adding Features
The code is designed to be simple and extensible. Key methods:
- `handshake()` - User registration/state
- `create_goal()` - Goal management
- `create_story()` - Story creation
- `update_story_progress()` - Progress tracking
- `get_user_*()` - Querying user data

## 📄 License

MIT License - Use freely for any purpose.

---

*Build software that matters. Track outcomes, not just tasks.*
