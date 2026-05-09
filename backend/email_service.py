import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
import sqlite3
import os
from pathlib import Path
import sys
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from ml_engine.inference import TicketModelHandler
from backend.database import DB_PATH

class EmailManager:
    def __init__(self):
        # Configuration from environment variables
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASS")
        self.imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        
        self.ai_handler = TicketModelHandler()
        self.ai_handler.load_models()

    def fetch_emails(self):
        """Polls the inbox for new tickets and processes them with AI."""
        if not self.user or not self.password:
            print("[EMAIL] Error: Email credentials not set in environment.")
            return []

        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.user, self.password)
            mail.select("inbox")
            
            # Search for all emails to ensure we don't miss ones viewed in a mail client
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                return []

            email_ids = messages[0].split()
            # Only process the last 30 emails to avoid unnecessary overhead
            email_ids = email_ids[-30:]
            print(f"[EMAIL] Checking last {len(email_ids)} emails for new tickets.")

            conn = sqlite3.connect(DB_PATH)
            new_tickets = []

            for e_id in email_ids:
                res, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        
                        sender = msg.get("From")

                        # Filter out automated/system emails
                        sender_lower = sender.lower() if sender else ""
                        if any(keyword in sender_lower for keyword in ["no-reply", "noreply", "accounts.google.com", "mailer-daemon"]):
                            continue
                            
                        # Extract Body
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                                elif content_type == "text/html" and not body:
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                        else:
                            body = msg.get_payload(decode=True).decode(errors="ignore")
                            
                        # Clean HTML tags if body contains them
                        if "<html>" in body.lower() or "<h2>" in body.lower() or "<p>" in body.lower() or "<div>" in body.lower():
                            import re
                            body = re.sub(r'<[^>]+>', ' ', body)
                            body = " ".join(body.split())
                            
                        # Override sender if it's a Structured Support Ticket
                        if "STRUCTURED SUPPORT TICKET" in body:
                            import re
                            match = re.search(r'User:\s*.*?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', body)
                            if match:
                                sender = match.group(1)

                        # Prevent Duplicate Tickets
                        cursor = conn.cursor()
                        if "[TKT-" in subject:
                            cursor.execute("SELECT id FROM tickets WHERE subject = ?", (subject,))
                        else:
                            cursor.execute("SELECT id FROM tickets WHERE subject = ? AND requester = ?", (subject, sender))
                            
                        if cursor.fetchone():
                            # Already processed
                            continue

                        # --- AI PROCESSING ---
                        prediction = self.ai_handler.predict(body)
                        
                        # Save to Database
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO tickets (subject, requester, support_team, priority, status, description, suggested_action)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            subject, 
                            sender, 
                            prediction['team'], 
                            prediction['priority'], 
                            "Open", 
                            body, 
                            prediction['suggested_action']
                        ))
                        ticket_id = cursor.lastrowid
                        new_tickets.append({"id": ticket_id, "subject": subject, "sender": sender})
                        print(f"[EMAIL] Created Ticket #{ticket_id} from {sender}")

            conn.commit()
            conn.close()
            mail.logout()
            return new_tickets

        except Exception as e:
            print(f"[EMAIL] Retrieval Error: {e}")
            return []

    def send_reply(self, ticket_id, custom_body=None):
        """Sends an email reply to the requester of a specific ticket."""
        if not self.user or not self.password:
            return False

        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            ticket = conn.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,)).fetchone()
            conn.close()

            if not ticket:
                print(f"[EMAIL] Error: Ticket #{ticket_id} not found.")
                return False

            recipient = ticket['requester']
            
            # If the requester is the system email, try to extract the real user from the description
            desc = ticket['description']
            if desc and "STRUCTURED SUPPORT TICKET" in desc:
                import re
                match = re.search(r'User:\s*.*?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', desc)
                if match:
                    recipient = match.group(1)
            
            # Simple extraction of email from "Name <email@domain.com>" or just "email@domain.com"
            if "<" in recipient and ">" in recipient:
                recipient = recipient.split("<")[1].split(">")[0]

            subject = f"Re: {ticket['subject']}"
            
            # Use AI draft if no custom body provided
            body = custom_body if custom_body else ticket['suggested_action']
            if not body:
                body = "Hello, we have received your ticket and are looking into it."

            # Create message
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.user
            msg["To"] = recipient

            # Send via SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"[EMAIL] Reply sent to {recipient} for Ticket #{ticket_id}")
            return True

        except Exception as e:
            print(f"[EMAIL] Sending Error: {e}")
            return False
