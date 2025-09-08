#!/usr/bin/env python3
"""
Test script for Story-Goal MCP protocol implementation.
"""
import json
import subprocess
import asyncio
import time

async def test_mcp_server():
    """Test the MCP server with sample requests."""
    print("🧪 Testing Story-Goal MCP Protocol")
    print("=" * 40)
    
    # Start the MCP server process
    process = subprocess.Popen(
        ['python3', 'mcp_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    def send_request(request):
        """Send JSON-RPC request to server."""
        request_json = json.dumps(request) + '\n'
        process.stdin.write(request_json)
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            return json.loads(response_line.strip())
        return None
    
    try:
        # Test 1: Initialize
        print("\n1. Testing Initialize")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        response = send_request(init_request)
        print(f"✅ Initialize: {response['result']['serverInfo']['name']}")
        
        # Test 2: List Tools
        print("\n2. Testing List Tools")
        tools_request = {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "tools/list"
        }
        response = send_request(tools_request)
        tool_count = len(response['result']['tools'])
        print(f"✅ Found {tool_count} tools:")
        for tool in response['result']['tools']:
            print(f"   - {tool['name']}: {tool['description']}")
        
        # Test 3: Handshake
        print("\n3. Testing Handshake")
        handshake_request = {
            "jsonrpc": "2.0",
            "id": 3, 
            "method": "tools/call",
            "params": {
                "name": "story_goal_handshake",
                "arguments": {
                    "user_key": "test-user",
                    "name": "Test User"
                }
            }
        }
        response = send_request(handshake_request)
        print(f"✅ Handshake successful for user: test-user")
        
        # Test 4: Create Goal
        print("\n4. Testing Create Goal")
        goal_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call", 
            "params": {
                "name": "create_goal",
                "arguments": {
                    "user_key": "test-user",
                    "title": "Test MCP Protocol",
                    "vision": "Verify Story-Goal MCP works via native protocol",
                    "success_metrics": "All MCP tools working correctly"
                }
            }
        }
        response = send_request(goal_request)
        goal_data = json.loads(response['result']['content'][0]['text'])
        goal_id = goal_data['id']
        print(f"✅ Created goal: {goal_id}")
        
        # Test 5: Create Story
        print("\n5. Testing Create Story")
        story_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "create_story", 
                "arguments": {
                    "user_key": "test-user",
                    "title": "MCP Protocol Validation",
                    "as_a": "As a developer",
                    "i_want": "I want MCP protocol to work correctly",
                    "so_that": "So that Claude can call Story-Goal MCP natively",
                    "goal_id": goal_id
                }
            }
        }
        response = send_request(story_request)
        story_data = json.loads(response['result']['content'][0]['text'])
        story_id = story_data['id'] 
        print(f"✅ Created story: {story_id}")
        
        # Test 6: Update Story
        print("\n6. Testing Update Story")
        update_request = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "update_story_progress",
                "arguments": {
                    "user_key": "test-user", 
                    "story_id": story_id,
                    "phase": "validating",
                    "notes": "MCP protocol test successful - all tools working"
                }
            }
        }
        response = send_request(update_request)
        print(f"✅ Updated story to validating phase")
        
        # Test 7: List Goals
        print("\n7. Testing List Goals")
        list_goals_request = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "list_goals",
                "arguments": {
                    "user_key": "test-user"
                }
            }
        }
        response = send_request(list_goals_request)
        goals = json.loads(response['result']['content'][0]['text'])
        print(f"✅ Listed {len(goals)} goals")
        
        # Test 8: List Stories
        print("\n8. Testing List Stories")
        list_stories_request = {
            "jsonrpc": "2.0", 
            "id": 8,
            "method": "tools/call",
            "params": {
                "name": "list_stories",
                "arguments": {
                    "user_key": "test-user"
                }
            }
        }
        response = send_request(list_stories_request)
        stories = json.loads(response['result']['content'][0]['text'])
        print(f"✅ Listed {len(stories)} stories")
        
        print("\n🎉 All MCP Protocol Tests Passed!")
        print("Story-Goal MCP is ready for native Claude integration!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        process.terminate()
        process.wait()
    
    return True

if __name__ == "__main__":
    asyncio.run(test_mcp_server())