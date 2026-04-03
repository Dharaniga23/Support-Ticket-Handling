import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'data' / 'db' / 'tickets.db'

def seed_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    sample_tickets = [
        ("Login Issue", "alice@example.com", "Technical Support", "High", "Open", "I cannot log into my account since the update. It says invalid credentials.", ""),
        ("Billing Error", "bob@business.com", "Financial Operations", "High", "Open", "I was charged twice for the premier subscription this month. Please refund one.", ""),
        ("Feature Request", "charlie@startup.io", "Product Team", "Low", "Solved", "It would be great if the dashboard had a dark mode option.", "Logged feedback and informed the user we will consider it for Q3."),
        ("API Timeout", "dev@integration.net", "Technical Support", "Critical", "Open", "The analytics API endpoint is timing out after 30 seconds consistently.", ""),
        ("Password Reset", "eve@personal.com", "Customer Success", "Medium", "Solved", "I forgot my password and the reset link is not arriving in my email.", "Sent manual reset link verified account ownership."),
        ("Subscription Upgrade", "sam@pro.com", "Sales", "Medium", "Open", "I want to upgrade my team of 50 to the Enterprise tier.", ""),
        ("Bug in Reports", "manager@corp.com", "Technical Support", "High", "Open", "The PDF export for March reports is missing the last two pages.", ""),
        ("Slow UI", "user123@gmail.com", "Technical Support", "Low", "Open", "The settings page takes 5 seconds to load.", ""),
    ]

    c.execute('DELETE FROM tickets')
    
    for i, t in enumerate(sample_tickets):
        # generate random past dates within the last 7 days
        days_ago = random.randint(0, 7)
        created_at = (datetime.now() - timedelta(days=days_ago, hours=random.randint(1, 23))).strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute('''
            INSERT INTO tickets (subject, requester, support_team, priority, status, description, resolution, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*t, created_at))
        
    conn.commit()
    conn.close()
    print("Database seeded with sample tickets successfully.")

if __name__ == '__main__':
    seed_db()
