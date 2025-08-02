import sqlite3
import os
import re
from datetime import datetime

# Define the path for the database in the root of the project
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'marketing_agent.db')

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    print("-- Initializing Database --")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Campaigns Table: To store the main topics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Ideas Table: To store the generated ideas for each campaign
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            idea_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
    ''')

    # Drafts Table: To store the generated drafts for each idea
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idea_id INTEGER NOT NULL,
            draft_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idea_id) REFERENCES ideas (id)
        )
    ''')

    # Create a new table for specialized drafts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specialized_drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_draft_id INTEGER,
            platform TEXT NOT NULL, -- e.g., 'twitter', 'instagram'
            specialized_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (original_draft_id) REFERENCES drafts (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("-- Database Initialized Successfully --")


def add_campaign_and_ideas(topic: str, ideas_text: str) -> list:
    """Adds a new campaign and its ideas, then returns the ideas with their new DB IDs."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Add the campaign
    cursor.execute('INSERT INTO campaigns (topic) VALUES (?)', (topic,))
    campaign_id = cursor.lastrowid

    # 2. Parse and add the ideas
    # Use regex to remove leading numbers (e.g., "1. ") from each idea
    ideas = [re.sub(r'^\d+\.?\s*', '', idea.strip()) for idea in ideas_text.split('\n') if idea.strip()]
    # 2. Parse, add the ideas, and collect them with their new IDs
    created_ideas = []
    ideas = [re.sub(r'^\d+\.?\s*', '', idea.strip()) for idea in ideas_text.split('\n') if idea.strip()]
    for idea_text in ideas:
        cursor.execute('INSERT INTO ideas (campaign_id, idea_text) VALUES (?, ?)', (campaign_id, idea_text))
        idea_id = cursor.lastrowid
        created_ideas.append({'id': idea_id, 'text': idea_text})
    
    conn.commit()
    conn.close()
    print(f"-- Saved campaign '{topic}' and {len(ideas)} ideas to DB. --")
    return created_ideas


def add_draft(idea_id: int, draft_text: str) -> int:
    """Adds a draft for a specific idea using its ID and returns the new draft's ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the draft using the provided idea_id
    cursor.execute('INSERT INTO drafts (idea_id, draft_text) VALUES (?, ?)', (idea_id, draft_text))
    new_draft_id = cursor.lastrowid # Get the ID of the newly inserted draft
    conn.commit()
    print(f"-- Saved draft for idea ID: {idea_id} to DB with draft ID: {new_draft_id}. --")
    conn.close()
    return new_draft_id


def add_specialized_draft(original_draft_id: int, platform: str, specialized_text: str):
    """Adds a specialized draft linked to an original draft."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO specialized_drafts (original_draft_id, platform, specialized_text) VALUES (?, ?, ?)',
        (original_draft_id, platform, specialized_text)
    )
    conn.commit()
    print(f"-- Saved specialized {platform} draft for original draft ID: {original_draft_id}. --")
    conn.close()


def get_full_history():
    """Retrieves all campaigns with their ideas, drafts, and specialized drafts."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch all drafts and specialized drafts first for efficiency
    cursor.execute('SELECT id, idea_id, draft_text, created_at FROM drafts ORDER BY created_at DESC')
    all_drafts = cursor.fetchall()
    
    cursor.execute('SELECT id, original_draft_id, platform, specialized_text, created_at FROM specialized_drafts ORDER BY created_at DESC')
    all_specialized_drafts = cursor.fetchall()

    # 2. Group specialized drafts by their original draft ID
    specialized_drafts_by_original_id = {}
    for sd in all_specialized_drafts:
        oid = sd['original_draft_id']
        if oid not in specialized_drafts_by_original_id:
            specialized_drafts_by_original_id[oid] = []
        specialized_drafts_by_original_id[oid].append(dict(sd))

    # 3. Group drafts by idea_id and attach their specialized drafts
    drafts_by_idea_id = {}
    for draft in all_drafts:
        draft_dict = dict(draft)
        draft_dict['specialized_drafts'] = specialized_drafts_by_original_id.get(draft['id'], [])
        
        idea_id = draft['idea_id']
        if idea_id not in drafts_by_idea_id:
            drafts_by_idea_id[idea_id] = []
        drafts_by_idea_id[idea_id].append(draft_dict)

    # 4. Fetch all campaigns and build the final history object
    cursor.execute('SELECT id, topic, created_at FROM campaigns ORDER BY id DESC')
    campaigns = cursor.fetchall()
    history = []

    for campaign in campaigns:
        campaign_dict = dict(campaign)
        
        # Fetch ideas for the current campaign
        cursor.execute('SELECT id, idea_text, created_at FROM ideas WHERE campaign_id = ? ORDER BY id ASC', (campaign['id'],))
        ideas = cursor.fetchall()
        
        # Attach the pre-fetched drafts to each idea
        ideas_list = []
        for idea in ideas:
            idea_dict = dict(idea)
            idea_dict['drafts'] = drafts_by_idea_id.get(idea['id'], [])
            ideas_list.append(idea_dict)
            
        campaign_dict['ideas'] = ideas_list
        history.append(campaign_dict)

    conn.close()
    return history
