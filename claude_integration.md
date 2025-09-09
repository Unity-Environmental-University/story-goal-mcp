# Claude Code Integration Guide

How to integrate Story-Goal MCP with your local Claude Code installation.

## 🔌 Integration Options

### Option 1: MCP Server Integration (Recommended)

Add Story-Goal MCP as a proper MCP server in Claude Code:

1. **Create MCP Configuration**

Add to your Claude Code MCP configuration (usually `~/.claude/mcp_servers.json`):

```json
{
  "story-goal-mcp": {
    "command": "python3",
    "args": ["/Users/hallie/Documents/repos/tools/story-goal-mcp/mcp_server.py"],
    "cwd": "/Users/hallie/Documents/repos/tools/story-goal-mcp"
  }
}
```

2. **Restart Claude Code**

After adding the configuration, restart Claude Code to load the new MCP server.

3. **Verify Integration**

Claude should now have access to these tools:
- `story_goal_handshake`
- `create_goal`  
- `create_story`
- `update_story_progress`
- `list_goals`
- `list_stories`
- `get_story_details`

### Option 2: Direct Tool Integration

If MCP server configuration isn't available, use bash tool integration:

1. **Add to .claude/settings.local.json**

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 /Users/hallie/Documents/repos/tools/story-goal-mcp/story_goal_mcp.py:*)"
    ]
  }
}
```

2. **Create Wrapper Script**

```bash
# Create a wrapper for easier access
cat > ~/.local/bin/story-goal << 'EOF'
#!/bin/bash
cd /Users/hallie/Documents/repos/tools/story-goal-mcp
python3 story_goal_mcp.py "$@"
EOF
chmod +x ~/.local/bin/story-goal
```

3. **Usage in Claude Sessions**

```bash
# Register your session
story-goal handshake my-session "My Name"

# Create goals and stories
story-goal create-goal my-session "Build Authentication" "Secure user login system" "Users can safely access app"
story-goal create-story my-session "Login Form" "As a user" "I want to log in" "So I can access my data"
```

## 🎯 Recommended Workflow

### Session Setup (Once per project/session)

```bash
# 1. Register your session with unique identifier
python3 story_goal_mcp.py handshake project-auth-system "Your Name"

# 2. Create high-level goal
python3 story_goal_mcp.py create-goal project-auth-system \
  "User Authentication System" \
  "Secure, reliable user authentication with modern UX" \
  "Users can log in/out safely, 99.9% uptime"
```

### During Development

Instead of TodoWrite:
```bash
# OLD: TodoWrite([{"content": "Fix login bug", "status": "pending"}])

# NEW: Create outcome-focused story
python3 story_goal_mcp.py create-story project-auth-system \
  "Reliable Login Experience" \
  "As a user" \
  "I want login to work consistently" \
  "So that I can access my account without frustration" \
  goal-id-here

# Track progress through phases
python3 story_goal_mcp.py update-story project-auth-system story-id \
  "developing" "Fixed session timeout bug, added comprehensive tests"

python3 story_goal_mcp.py update-story project-auth-system story-id \
  "validating" "Testing with various browsers and edge cases"

python3 story_goal_mcp.py update-story project-auth-system story-id \
  "complete" "Login working reliably, all tests passing, deployed"
```

### Session Review

```bash
# Check goal progress
python3 story_goal_mcp.py list-goals project-auth-system

# View active work
python3 story_goal_mcp.py list-stories project-auth-system "" "developing"
python3 story_goal_mcp.py list-stories project-auth-system "" "validating"

# Review completed stories
python3 story_goal_mcp.py list-stories project-auth-system "" "complete"
```

## 🔧 Configuration Examples

### Project-Specific Setup

For each project, create a unique workspace:

```bash
# Web app project
python3 story_goal_mcp.py handshake webapp-v2 "Developer Name"

# Mobile app project  
python3 story_goal_mcp.py handshake mobile-app "Developer Name"

# API service project
python3 story_goal_mcp.py handshake api-service "Developer Name"
```

### Team Usage

Each team member gets their own workspace:

```bash
# Team member A
python3 story_goal_mcp.py handshake alice-frontend "Alice Smith"

# Team member B  
python3 story_goal_mcp.py handshake bob-backend "Bob Johnson"

# Shared goals, individual stories
python3 story_goal_mcp.py create-goal alice-frontend "E-commerce Checkout" "Streamlined purchase flow" "85%+ completion rate"
python3 story_goal_mcp.py create-goal bob-backend "E-commerce Checkout" "Streamlined purchase flow" "85%+ completion rate"
```

## 💡 Claude Code Integration Tips

### 1. Session Persistence
- Database persists between Claude sessions
- Use consistent user_key for continuity
- Goals and stories carry forward automatically

### 2. Context-Rich Development
- Every story includes full user context
- Progress notes capture learning and decisions
- Goals provide high-level direction

### 3. Outcome Tracking
- Focus on user value, not just task completion  
- Stories connect to meaningful business outcomes
- Progress phases track real development stages

### 4. Tool Synergy
- Story-Goal MCP complements other development tools
- Can be combined with project management systems
- Provides rich context for retrospectives and planning

## 🚀 Quick Start Commands

```bash
# Essential commands for Claude Code integration
cd /Users/hallie/Documents/repos/tools/story-goal-mcp

# Session setup
python3 story_goal_mcp.py handshake $(whoami)-$(basename $(pwd)) "$(git config user.name)"

# Quick goal creation
python3 story_goal_mcp.py create-goal $(whoami)-$(basename $(pwd)) \
  "$(basename $(pwd)) Development" \
  "Build and ship valuable features for users" \
  "Features delivered that solve real user problems"

# Quick story creation  
python3 story_goal_mcp.py create-story $(whoami)-$(basename $(pwd)) \
  "Feature Name" \
  "As a [user type]" \
  "I want [capability]" \
  "So that [benefit]" \
  goal-id-from-above

# Check progress anytime
python3 story_goal_mcp.py list-goals $(whoami)-$(basename $(pwd))
python3 story_goal_mcp.py list-stories $(whoami)-$(basename $(pwd))
```

## 🎯 Success Metrics

You'll know the integration is working when:

✅ **Context-Rich Work**: Every task has clear user value  
✅ **Goal Alignment**: Stories connect to meaningful outcomes  
✅ **Progress Visibility**: Can see development phases clearly  
✅ **Session Continuity**: Work persists between Claude sessions  
✅ **Outcome Focus**: Building features, not just checking tasks  

Story-Goal MCP transforms development from task-checking to value-delivery!