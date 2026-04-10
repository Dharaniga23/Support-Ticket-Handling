import imaplib
import email
from email.header import decode_header
import sqlite3
import sys
from pathlib import Path

# Add project root to path to use the ML engine
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from ml_engine.inference import TicketModelHandler
from backend.database import DB_PATH

# === CONFIGURATION (For Explanation) ===
IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = "support@yourcompany.com"
EMAIL_PASS = "your-app-password"  # Use Google App Passwords for security

def connect_to_inbox():
    """Establishes a secure connection to the live email server."""
    print(f"Connecting to {IMAP_SERVER}...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    return mail

def fetch_and_process_emails():
    """
    Main logic for the guide: 
    1. Polls the inbox for UNSEEN (new) messages.
    2. Uses AI to 'read' and classify them instantly.
    3. Saves them to the database for the dashboard.
    """
    
    # Initialize the AI Brain
    ai_handler = TicketModelHandler()
    ai_handler.load_models()
    
    mail = connect_to_inbox()
    mail.select("inbox")
    
    # Search for all unread emails
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    
    print(f"Found {len(email_ids)} new emails to process.")
    
    conn = sqlite3.connect(DB_PATH)
    
    for e_id in email_ids:
        # Fetch the email body
        res, msg = mail.fetch(e_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                
                # Extract Subject and Sender
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                sender = msg.get("From")
                
                # Extract Body
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                # --- THE AI INTELLIGENCE LAYER ---
                # This is where the project's 'Brain' takes over
                prediction = ai_handler.predict(body)
                
                print(f"Processed email from {sender} -> Predicted {prediction['team']}")

                # --- PERSIST TO DATABASE ---
                conn.execute('''
                    INSERT INTO tickets (subject, requester, support_team, priority, status, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (subject, sender, prediction['team'], prediction['priority'], "Open", body))
                
    conn.commit()
    conn.close()
    mail.logout()

if __name__ == "__main__":
    # In a real company, this script would run every 5 minutes using a 'Cron Job'
    print("Email-to-AI Connector Template Active")
    # fetch_and_process_emails() # Uncomment to run with real credentials
