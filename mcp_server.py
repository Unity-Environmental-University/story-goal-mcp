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
            return self.story_goal.get_user_stories(user_key, goal_id, phase)
            
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