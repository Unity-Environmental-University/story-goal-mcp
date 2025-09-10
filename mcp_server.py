#!/usr/bin/env python3
"""
Story-Goal MCP Protocol Server
Native MCP server implementation that wraps the Story-Goal functionality.
"""
import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from story_goal_mcp import StoryGoalMCP, StoryPhase

class StoryGoalMCPServer:
    def __init__(self):
        self.story_goal = StoryGoalMCP()
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP JSON-RPC request."""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {
                                "listChanged": True
                            }
                        },
                        "serverInfo": {
                            "name": "story-goal-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "story_goal_handshake",
                                "description": "Register or verify user workspace",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "user_key": {"type": "string"},
                                        "name": {"type": "string", "optional": True}
                                    },
                                    "required": ["user_key"]
                                }
                            },
                            {
                                "name": "create_goal", 
                                "description": "Create a new goal with vision and success metrics",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "user_key": {"type": "string"},
                                        "title": {"type": "string"},
                                        "vision": {"type": "string"},
                                        "success_metrics": {"type": "string", "optional": True}
                                    },
                                    "required": ["user_key", "title", "vision"]
                                }
                            },
                            {
                                "name": "create_story",
                                "description": "Create a user story with full context",
                                "inputSchema": {
                                    "type": "object", 
                                    "properties": {
                                        "user_key": {"type": "string"},
                                        "title": {"type": "string"},
                                        "as_a": {"type": "string"},
                                        "i_want": {"type": "string"},
                                        "so_that": {"type": "string"},
                                        "goal_id": {"type": "string", "optional": True}
                                    },
                                    "required": ["user_key", "title", "as_a", "i_want", "so_that"]
                                }
                            },
                            {
                                "name": "update_story_progress",
                                "description": "Update story phase and add progress notes",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "user_key": {"type": "string"},
                                        "story_id": {"type": "string"},
                                        "phase": {"type": "string", "enum": ["defining", "developing", "validating", "complete"]},
                                        "notes": {"type": "string"}
                                    },
                                    "required": ["user_key", "story_id", "phase", "notes"]
                                }
                            },
                            {
                                "name": "list_goals",
                                "description": "Get all goals for a user with story counts",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "user_key": {"type": "string"}
                                    },
                                    "required": ["user_key"]
                                }
                            },
                            {
                                "name": "list_stories", 
                                "description": "Get stories for a user, optionally filtered",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "user_key": {"type": "string"},
                                        "goal_id": {"type": "string", "optional": True},
                                        "phase": {"type": "string", "optional": True}
                                    },
                                    "required": ["user_key"]
                                }
                            },
                            {
                                "name": "get_story_details",
                                "description": "Get detailed view of a specific story",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "user_key": {"type": "string"},
                                        "story_id": {"type": "string"}
                                    },
                                    "required": ["user_key", "story_id"]
                                }
                            }
                        ]
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                result = await self.execute_tool(tool_name, arguments)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a Story-Goal MCP tool."""
        user_key = arguments.get("user_key")
        
        if tool_name == "story_goal_handshake":
            name = arguments.get("name")
            return self.story_goal.handshake(user_key, name)
            
        elif tool_name == "create_goal":
            title = arguments.get("title")
            vision = arguments.get("vision") 
            success_metrics = arguments.get("success_metrics", "")
            return self.story_goal.create_goal(user_key, title, vision, success_metrics)
            
        elif tool_name == "create_story":
            title = arguments.get("title")
            as_a = arguments.get("as_a")
            i_want = arguments.get("i_want")
            so_that = arguments.get("so_that")
            goal_id = arguments.get("goal_id")
            return self.story_goal.create_story(user_key, title, as_a, i_want, so_that, goal_id)
            
        elif tool_name == "update_story_progress":
            story_id = arguments.get("story_id")
            phase = arguments.get("phase") 
            notes = arguments.get("notes")
            success = self.story_goal.update_story_progress(user_key, story_id, phase, notes)
            return {"success": success, "story_id": story_id, "phase": phase}
            
        elif tool_name == "list_goals":
            return self.story_goal.get_user_goals(user_key)
            
        elif tool_name == "list_stories":
            goal_id = arguments.get("goal_id")
            phase = arguments.get("phase")
            since = arguments.get("since")
            fields = arguments.get("fields") or []
            confirm = bool(arguments.get("confirm", False))
            stories = self.story_goal.get_user_stories(user_key, goal_id, phase)
            # Optional since filter
            if since:
                try:
                    import datetime
                    since_dt = datetime.datetime.fromisoformat(since.replace('Z','+00:00'))
                    def _u(s):
                        ts = s.get('updated_at') or s.get('created_at')
                        try:
                            return datetime.datetime.fromisoformat(str(ts).replace('Z','+00:00'))
                        except Exception:
                            return since_dt
                    stories = [s for s in stories if _u(s) > since_dt]
                except Exception:
                    pass
            # Optional projection
            if fields:
                proj = []
                for s in stories:
                    out = {k: s.get(k) for k in fields if k in s}
                    if 'last_note' in fields:
                        notes = s.get('progress_notes') or []
                        out['last_note'] = (notes[-1] if notes else None)
                    proj.append(out)
                stories = proj
            # Optional confirm summary
            if confirm:
                for s in stories:
                    try:
                        ln = None
                        if isinstance(s.get('last_note'), dict):
                            ln = s['last_note'].get('notes')
                        elif isinstance(s.get('progress_notes'), list) and s['progress_notes']:
                            ln = s['progress_notes'][-1].get('notes')
                        s['summary'] = f"{s.get('title','')} — {s.get('current_phase','')}: {ln or ''}"
                    except Exception:
                        continue
            return stories

        elif tool_name == "list_story_changes":
            since = arguments.get("since")
            phase = arguments.get("phase")
            story_ids = set(arguments.get("story_ids") or [])
            confirm = bool(arguments.get("confirm", False))
            stories = self.story_goal.get_user_stories(user_key, None, phase)
            import datetime
            try:
                def _parse_iso(ts: str):
                    ts = str(ts)
                    if not ts:
                        return None
                    if ts.endswith('Z'):
                        ts = ts.replace('Z', '+00:00')
                    dt = datetime.datetime.fromisoformat(ts)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=datetime.timezone.utc)
                    return dt
                since_dt = _parse_iso(since) if since else None
            except Exception:
                since_dt = None
            deltas = []
            for s in stories:
                if story_ids and s.get('id') not in story_ids:
                    continue
                upd = s.get('updated_at') or s.get('created_at')
                try:
                    upd_dt = _parse_iso(upd)
                except Exception:
                    upd_dt = None
                if since_dt and upd_dt and not (upd_dt > since_dt):
                    continue
                last_note = (s.get('progress_notes') or [])[-1] if (s.get('progress_notes') or []) else None
                delta = {
                    'id': s.get('id'),
                    'updated_at': upd,
                    'changed': {
                        'current_phase': s.get('current_phase'),
                        'title': s.get('title'),
                        'acceptance_criteria_changed': True if (s.get('acceptance_criteria') not in (None, [])) else False,
                        'last_note': last_note
                    }
                }
                if not confirm:
                    # Keep compact: remove None values
                    ch = {k:v for k,v in delta['changed'].items() if v is not None}
                    delta['changed'] = ch
                else:
                    ln = (last_note or {}).get('notes') if isinstance(last_note, dict) else None
                    delta['summary'] = f"{s.get('title','')} — {s.get('current_phase','')}: {ln or ''}"
                deltas.append(delta)
            deltas.sort(key=lambda d: str(d.get('updated_at')))
            return deltas
            
        elif tool_name == "get_story_details":
            story_id = arguments.get("story_id")
            return self.story_goal.get_story_details(user_key, story_id)
            
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

async def main():
    """Run the MCP server."""
    server = StoryGoalMCPServer()
    
    # Read from stdin, write to stdout (MCP protocol)
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
