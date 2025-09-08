#!/usr/bin/env python3
"""
Story-Goal MCP Server
A lightweight MCP server for managing user stories and goals with proper user separation.

Replaces task-focused TodoWrite with outcome-focused story tracking.
"""
import json
import sqlite3
import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class StoryPhase(Enum):
    DEFINING = "defining"
    DEVELOPING = "developing" 
    VALIDATING = "validating"
    COMPLETE = "complete"

@dataclass
class UserStory:
    id: str
    title: str
    as_a: str           # "As a developer"
    i_want: str         # "I want secure authentication"
    so_that: str        # "So that user data is protected"
    acceptance_criteria: List[str]
    current_phase: str  # StoryPhase value
    progress_notes: List[str]
    goal_id: Optional[str]
    user_key: str
    created_at: str
    updated_at: str

@dataclass
class Goal:
    id: str
    title: str
    vision: str                 # High-level outcome
    success_metrics: str        # How we know we succeeded
    user_key: str
    created_at: str
    updated_at: str

class StoryGoalMCP:
    def __init__(self, db_path: str = "story_goals.db"):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with user-separated tables."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_key TEXT PRIMARY KEY,
                name TEXT,
                created_at TEXT
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                vision TEXT NOT NULL,
                success_metrics TEXT,
                user_key TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_key) REFERENCES users (user_key)
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stories (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                as_a TEXT NOT NULL,
                i_want TEXT NOT NULL,
                so_that TEXT NOT NULL,
                acceptance_criteria TEXT NOT NULL, -- JSON array
                current_phase TEXT NOT NULL,
                progress_notes TEXT NOT NULL,      -- JSON array
                goal_id TEXT,
                user_key TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_key) REFERENCES users (user_key),
                FOREIGN KEY (goal_id) REFERENCES goals (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def handshake(self, user_key: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Register or verify user, return their current state."""
        conn = sqlite3.connect(self.db_path)
        
        # Check if user exists
        cursor = conn.execute("SELECT name FROM users WHERE user_key = ?", (user_key,))
        existing = cursor.fetchone()
        
        if not existing:
            # Create new user
            conn.execute("""
                INSERT INTO users (user_key, name, created_at) 
                VALUES (?, ?, ?)
            """, (user_key, name or "Unknown", datetime.now().isoformat()))
            conn.commit()
            
        # Get user's current state
        cursor = conn.execute("""
            SELECT COUNT(*) FROM goals WHERE user_key = ?
        """, (user_key,))
        goal_count = cursor.fetchone()[0]
        
        cursor = conn.execute("""
            SELECT COUNT(*) FROM stories WHERE user_key = ?
        """, (user_key,))
        story_count = cursor.fetchone()[0]
        
        cursor = conn.execute("""
            SELECT COUNT(*) FROM stories 
            WHERE user_key = ? AND current_phase != 'complete'
        """, (user_key,))
        active_stories = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "user_key": user_key,
            "name": name or existing[0] if existing else "Unknown",
            "goals": goal_count,
            "stories": story_count,
            "active_stories": active_stories,
            "handshake_time": datetime.now().isoformat()
        }
    
    def create_goal(self, user_key: str, title: str, vision: str, 
                   success_metrics: str = "") -> Dict[str, Any]:
        """Create a new goal for the user."""
        goal_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO goals (id, title, vision, success_metrics, user_key, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (goal_id, title, vision, success_metrics, user_key, now, now))
        conn.commit()
        conn.close()
        
        return {
            "id": goal_id,
            "title": title,
            "vision": vision,
            "success_metrics": success_metrics,
            "created_at": now
        }
    
    def create_story(self, user_key: str, title: str, as_a: str, i_want: str, 
                    so_that: str, goal_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new user story."""
        story_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO stories (id, title, as_a, i_want, so_that, acceptance_criteria, 
                               current_phase, progress_notes, goal_id, user_key, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (story_id, title, as_a, i_want, so_that, "[]", StoryPhase.DEFINING.value, 
              "[]", goal_id, user_key, now, now))
        conn.commit()
        conn.close()
        
        return {
            "id": story_id,
            "title": title,
            "as_a": as_a,
            "i_want": i_want,
            "so_that": so_that,
            "current_phase": StoryPhase.DEFINING.value,
            "goal_id": goal_id,
            "created_at": now
        }
    
    def update_story_progress(self, user_key: str, story_id: str, 
                            phase: str, notes: str) -> bool:
        """Update story phase and add progress notes."""
        if phase not in [p.value for p in StoryPhase]:
            return False
            
        conn = sqlite3.connect(self.db_path)
        
        # Get current progress notes
        cursor = conn.execute("""
            SELECT progress_notes FROM stories 
            WHERE id = ? AND user_key = ?
        """, (story_id, user_key))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
            
        current_notes = json.loads(result[0])
        current_notes.append({
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "notes": notes
        })
        
        conn.execute("""
            UPDATE stories 
            SET current_phase = ?, progress_notes = ?, updated_at = ?
            WHERE id = ? AND user_key = ?
        """, (phase, json.dumps(current_notes), datetime.now().isoformat(), story_id, user_key))
        
        conn.commit()
        conn.close()
        return True
    
    def add_acceptance_criteria(self, user_key: str, story_id: str, 
                              criteria: List[str]) -> bool:
        """Add acceptance criteria to a story."""
        conn = sqlite3.connect(self.db_path)
        
        cursor = conn.execute("""
            SELECT acceptance_criteria FROM stories 
            WHERE id = ? AND user_key = ?
        """, (story_id, user_key))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
            
        current_criteria = json.loads(result[0])
        current_criteria.extend(criteria)
        
        conn.execute("""
            UPDATE stories 
            SET acceptance_criteria = ?, updated_at = ?
            WHERE id = ? AND user_key = ?
        """, (json.dumps(current_criteria), datetime.now().isoformat(), story_id, user_key))
        
        conn.commit()
        conn.close()
        return True
    
    def get_user_goals(self, user_key: str) -> List[Dict[str, Any]]:
        """Get all goals for a user with story counts."""
        conn = sqlite3.connect(self.db_path)
        
        cursor = conn.execute("""
            SELECT g.*, 
                   COUNT(s.id) as total_stories,
                   COUNT(CASE WHEN s.current_phase = 'complete' THEN 1 END) as completed_stories
            FROM goals g
            LEFT JOIN stories s ON g.id = s.goal_id
            WHERE g.user_key = ?
            GROUP BY g.id
            ORDER BY g.created_at DESC
        """, (user_key,))
        
        goals = []
        for row in cursor.fetchall():
            goals.append({
                "id": row[0],
                "title": row[1], 
                "vision": row[2],
                "success_metrics": row[3],
                "created_at": row[5],
                "updated_at": row[6],
                "total_stories": row[7],
                "completed_stories": row[8]
            })
            
        conn.close()
        return goals
    
    def get_user_stories(self, user_key: str, goal_id: Optional[str] = None, 
                        phase: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get stories for a user, optionally filtered by goal or phase."""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM stories WHERE user_key = ?"
        params = [user_key]
        
        if goal_id:
            query += " AND goal_id = ?"
            params.append(goal_id)
            
        if phase:
            query += " AND current_phase = ?"
            params.append(phase)
            
        query += " ORDER BY updated_at DESC"
        
        cursor = conn.execute(query, params)
        
        stories = []
        for row in cursor.fetchall():
            stories.append({
                "id": row[0],
                "title": row[1],
                "as_a": row[2],
                "i_want": row[3], 
                "so_that": row[4],
                "acceptance_criteria": json.loads(row[5]),
                "current_phase": row[6],
                "progress_notes": json.loads(row[7]),
                "goal_id": row[8],
                "created_at": row[10],
                "updated_at": row[11]
            })
            
        conn.close()
        return stories
    
    def get_story_details(self, user_key: str, story_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed view of a specific story."""
        conn = sqlite3.connect(self.db_path)
        
        cursor = conn.execute("""
            SELECT s.*, g.title as goal_title, g.vision as goal_vision
            FROM stories s
            LEFT JOIN goals g ON s.goal_id = g.id
            WHERE s.id = ? AND s.user_key = ?
        """, (story_id, user_key))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        return {
            "id": row[0],
            "title": row[1],
            "as_a": row[2],
            "i_want": row[3],
            "so_that": row[4], 
            "acceptance_criteria": json.loads(row[5]),
            "current_phase": row[6],
            "progress_notes": json.loads(row[7]),
            "goal_id": row[8],
            "created_at": row[10],
            "updated_at": row[11],
            "goal_title": row[12],
            "goal_vision": row[13]
        }

# MCP Server Interface
if __name__ == "__main__":
    import sys
    
    mcp = StoryGoalMCP()
    
    if len(sys.argv) < 2:
        print("Usage: python story_goal_mcp.py <command> <args>")
        print("Commands: handshake, create-goal, create-story, update-story, list-goals, list-stories")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "handshake":
        user_key = sys.argv[2] if len(sys.argv) > 2 else "default-user"
        name = sys.argv[3] if len(sys.argv) > 3 else None
        result = mcp.handshake(user_key, name)
        print(json.dumps(result, indent=2))
    
    elif command == "create-goal":
        if len(sys.argv) < 5:
            print("Usage: create-goal <user_key> <title> <vision> [success_metrics]")
            sys.exit(1)
        user_key, title, vision = sys.argv[2:5]
        success_metrics = sys.argv[5] if len(sys.argv) > 5 else ""
        result = mcp.create_goal(user_key, title, vision, success_metrics)
        print(json.dumps(result, indent=2))
    
    elif command == "create-story":
        if len(sys.argv) < 7:
            print("Usage: create-story <user_key> <title> <as_a> <i_want> <so_that> [goal_id]")
            sys.exit(1)
        user_key, title, as_a, i_want, so_that = sys.argv[2:7]
        goal_id = sys.argv[7] if len(sys.argv) > 7 else None
        result = mcp.create_story(user_key, title, as_a, i_want, so_that, goal_id)
        print(json.dumps(result, indent=2))
    
    elif command == "list-goals":
        user_key = sys.argv[2] if len(sys.argv) > 2 else "default-user"
        goals = mcp.get_user_goals(user_key)
        print(json.dumps(goals, indent=2))
    
    elif command == "list-stories":
        user_key = sys.argv[2] if len(sys.argv) > 2 else "default-user"
        goal_id = sys.argv[3] if len(sys.argv) > 3 else None
        phase = sys.argv[4] if len(sys.argv) > 4 else None
        stories = mcp.get_user_stories(user_key, goal_id, phase)
        print(json.dumps(stories, indent=2))
    
    elif command == "update-story":
        if len(sys.argv) < 6:
            print("Usage: update-story <user_key> <story_id> <phase> <notes>")
            sys.exit(1)
        user_key, story_id, phase, notes = sys.argv[2:6]
        success = mcp.update_story_progress(user_key, story_id, phase, notes)
        if success:
            print(f"Updated story {story_id} to phase '{phase}'")
        else:
            print(f"Failed to update story {story_id}")
            sys.exit(1)
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)