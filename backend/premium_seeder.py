import sqlite3
import random
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import sys
import os

# Add project root to path so we can import ml_engine
project_root = Path(r'c:\Users\dhara\Desktop\An-End-to-End-Semantic-AI-System-for-Automated-Support-Ticket-Handling-main')
sys.path.append(str(project_root))

from ml_engine.inference import TicketModelHandler

DB_PATH = project_root / 'data' / 'db' / 'tickets.db'
DATA_PATH = project_root / 'data' / 'processed' / 'unified_tickets.csv'

HUMAN_NAMES = [
    "James Wilson", "Mary Johnson", "Robert Smith", "Patricia Brown", "Michael Miller",
    "Jennifer Davis", "William Garcia", "Linda Rodriguez", "David Martinez", "Elizabeth Hernandez",
    "Joseph Lopez", "Barbara Gonzalez", "Thomas Wilson", "Susan Anderson", "Charles Thomas",
    "Jessica Taylor", "Christopher Moore", "Sarah Jackson", "Daniel Martin", "Karen Lee",
    "Matthew Perez", "Nancy Thompson", "Anthony White", "Lisa Harris", "Mark Sanchez",
    "Betty Clark", "Donald Ramirez", "Margaret Lewis", "Steven Robinson", "Sandra Walker"
]

DOMAINS = ["gmail.com", "outlook.com", "company-it.net", "business-ops.com", "startup-hub.io"]

def generate_human():
    name = random.choice(HUMAN_NAMES)
    email = f"{name.split()[0].lower()}.{name.split()[1].lower()}@{random.choice(DOMAINS)}"
    return f"{name} <{email}>"

def premium_seed():
    print("Initializing Premium AI Seeder...")
    
    # 1. Initialize AI Handler
    handler = TicketModelHandler()
    print("Loading AI Models for Proper Classification...")
    handler.load_models() # This will be the first load, might take a bit
    
    # 2. Load Source Data
    print(f"Reading unified dataset from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    # 3. Connect to DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Clear existing demo tickets (keep it clean)
    print("Cleaning existing tickets...")
    c.execute('DELETE FROM tickets')
    
    # 4. Process Samples
    sample_count = 60
    # Mix of different categories from the dataset
    samples = df.sample(min(sample_count, len(df)))
    
    print(f"Processing {len(samples)} tickets through the AI Brain...")
    
    for i, (_, row) in enumerate(samples.iterrows()):
        desc = str(row['description'])
        if len(desc) > 300: desc = desc[:297] + "..." # Truncate for UI
        
        # Use AI to Classified Properly
        prediction = handler.predict(desc)
        
        # Humanize
        requester = generate_human()
        
        # Determine Status (80% Open for demo visibility)
        status = random.choice(["Open", "Open", "Open", "Open", "Open", "Pending", "Solved"])
        
        # Subject extraction (first sentence or generic)
        subject = desc.split('.')[0]
        if len(subject) > 60: subject = subject[:57] + "..."
        if not subject: subject = "Inquiry regarding " + prediction['category']
        
        # Random Date within last 3 days
        created_at = (datetime.now() - timedelta(minutes=random.randint(10, 4320))).strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute('''
            INSERT INTO tickets (subject, requester, support_team, priority, status, description, resolution, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            subject, 
            requester, 
            prediction['team'], 
            prediction['priority'], 
            status, 
            desc, 
            "", 
            created_at
        ))
        
        if (i+1) % 10 == 0:
            print(f"  [{i+1}/{len(samples)}] Categorized: {prediction['category']} -> Team: {prediction['team']}")
        
    conn.commit()
    conn.close()
    print(f"SUCCESS: 60 Premium AI-Classified tickets added to {DB_PATH}")

if __name__ == "__main__":
    premium_seed()
