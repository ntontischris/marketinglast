import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
import os

class MemoryManager:
    """
    Advanced memory management system for AI agents.
    Stores conversation history, user preferences, campaign performance, and learnings.
    """
    
    def __init__(self, db_path: str = "database/marketing_memory.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize the memory database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User preferences and brand voice
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            brand_voice TEXT,
            industry TEXT,
            target_audience TEXT,
            preferred_tone TEXT,
            color_preferences TEXT,
            logo_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Campaign history and performance
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            topic TEXT,
            creative_brief TEXT,
            final_content TEXT,
            platform TEXT,
            engagement_score REAL DEFAULT 0,
            conversion_rate REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Agent learnings and feedback
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_learnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT,
            context TEXT,
            user_feedback TEXT,
            improvement_note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Trending topics and insights
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trend_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            industry TEXT,
            engagement_potential REAL,
            keywords TEXT,
            best_platforms TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_user_profile(self, user_id: str, profile_data: Dict[str, Any]):
        """Save or update user profile and preferences."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO user_profiles 
        (user_id, brand_voice, industry, target_audience, preferred_tone, 
         color_preferences, logo_description, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (
            user_id,
            profile_data.get('brand_voice', ''),
            profile_data.get('industry', ''),
            profile_data.get('target_audience', ''),
            profile_data.get('preferred_tone', ''),
            json.dumps(profile_data.get('color_preferences', [])),
            profile_data.get('logo_description', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user profile and preferences."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT brand_voice, industry, target_audience, preferred_tone, 
               color_preferences, logo_description
        FROM user_profiles WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'brand_voice': result[0],
                'industry': result[1],
                'target_audience': result[2],
                'preferred_tone': result[3],
                'color_preferences': json.loads(result[4]) if result[4] else [],
                'logo_description': result[5]
            }
        return None
    
    def save_campaign(self, user_id: str, campaign_data: Dict[str, Any]):
        """Save campaign data for learning and optimization."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO campaigns 
        (user_id, topic, creative_brief, final_content, platform, engagement_score, conversion_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            campaign_data.get('topic', ''),
            campaign_data.get('creative_brief', ''),
            campaign_data.get('final_content', ''),
            campaign_data.get('platform', 'general'),
            campaign_data.get('engagement_score', 0),
            campaign_data.get('conversion_rate', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def get_similar_campaigns(self, topic: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get similar past campaigns for learning."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT topic, creative_brief, final_content, platform, engagement_score
        FROM campaigns 
        WHERE topic LIKE ? OR creative_brief LIKE ?
        ORDER BY engagement_score DESC
        LIMIT ?
        ''', (f'%{topic}%', f'%{topic}%', limit))
        
        results = cursor.fetchall()
        conn.close()
        
        campaigns = []
        for result in results:
            campaigns.append({
                'topic': result[0],
                'creative_brief': result[1],
                'final_content': result[2],
                'platform': result[3],
                'engagement_score': result[4]
            })
        
        return campaigns
    
    def save_agent_learning(self, agent_name: str, context: str, feedback: str, improvement: str):
        """Save agent feedback for continuous learning."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO agent_learnings (agent_name, context, user_feedback, improvement_note)
        VALUES (?, ?, ?, ?)
        ''', (agent_name, context, feedback, improvement))
        
        conn.commit()
        conn.close()
    
    def get_agent_learnings(self, agent_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get past learnings for an agent."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT context, user_feedback, improvement_note, created_at
        FROM agent_learnings 
        WHERE agent_name = ?
        ORDER BY created_at DESC
        LIMIT ?
        ''', (agent_name, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        learnings = []
        for result in results:
            learnings.append({
                'context': result[0],
                'user_feedback': result[1],
                'improvement_note': result[2],
                'created_at': result[3]
            })
        
        return learnings
