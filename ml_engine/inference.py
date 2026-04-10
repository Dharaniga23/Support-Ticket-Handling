import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class TicketModelHandler:
    def __init__(self):
        self.models_base = Path(__file__).parent.parent / 'models'
        self.sbert = None
        self.cat_model = None
        self.cat_le = None
        self.team_model = None
        self.team_le = None
        self.priority_model = None
        self.priority_le = None
        self.ttr_model = None
        self.ttr_le = None
        self.kb_df = None
        self.kb_embeddings = None
        self.last_error = None
        self.is_loaded = False

    def load_models(self):
        if self.is_loaded:
            return
            
        try:
            print("[STARTUP] Initializing Unified SBERT...")
            self.sbert = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Error loading SBERT: {e}")
            self.sbert = None

        try:
            print("[SYNC] Syncing Category Module...")
            self.cat_model = pickle.load(open(self.models_base / 'category_classifier' / 'sbert_classifier.pkl', 'rb'))
            self.cat_le = pickle.load(open(self.models_base / 'category_classifier' / 'label_encoder.pkl', 'rb'))
        except Exception as e:
            print(f"Error loading category model: {e}")
            self.cat_model = None
            self.cat_le = None

        try:
            print("[SYNC] Syncing Team & Priority Modules...")
            self.team_model = pickle.load(open(self.models_base / 'team_priority_classifier' / 'team_classifier.pkl', 'rb'))
            self.team_le = pickle.load(open(self.models_base / 'team_priority_classifier' / 'le_team.pkl', 'rb'))
            self.priority_model = pickle.load(open(self.models_base / 'team_priority_classifier' / 'priority_classifier.pkl', 'rb'))
            self.priority_le = pickle.load(open(self.models_base / 'team_priority_classifier' / 'le_priority.pkl', 'rb'))
        except Exception as e:
            print(f"Error loading team/priority models: {e}")
            self.team_model = None
            self.team_le = None
            self.priority_model = None
            self.priority_le = None

        try:
            print("[SYNC] Syncing Resolution Time Module...")
            self.ttr_model = pickle.load(open(self.models_base / 'resolution_time_predictor' / 'ttr_model.pkl', 'rb'))
            self.ttr_le = pickle.load(open(self.models_base / 'resolution_time_predictor' / 'ttr_le.pkl', 'rb'))
        except Exception as e:
            print(f"Error loading TTR model: {e}")
            self.ttr_model = None
            self.ttr_le = None

        try:
            print("[SYNC] Syncing Action Retrieval Module (Stable CSV + Numpy)...")
            kb_path = self.models_base / 'action_generator' / 'action_kb_text.csv'
            emb_path = self.models_base / 'action_generator' / 'action_embeddings.npy'
            
            if kb_path.exists() and emb_path.exists():
                self.kb_df = pd.read_csv(kb_path)
                self.kb_embeddings = np.load(emb_path)
                print("[SUCCESS] Action Knowledge Base Loaded Successfully")
            else:
                print("[WARNING] Action KB files missing. Please run Notebook 05 again.")
        except Exception as e:
            self.last_error = str(e)
            print(f"[ERROR] Failed to load action KB: {e}")
            self.kb_df = None
            self.kb_embeddings = None
            
        self.is_loaded = True
        print("[READY] All modules initialized (Lazy Load Complete)")

    def predict(self, description):
        # Lazy load on first request
        if not self.is_loaded:
            self.load_models()

        if not self.sbert:
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "team": "Unknown",
                "priority": "Unknown",
                "eta": "Unknown",
                "suggested_action": "Please contact support",
                "routing_status": "Escalate"
            }

        # Encode the description
        embedding = self.sbert.encode([description])[0]

        # Category prediction
        category = "Unknown"
        confidence = 0.0
        if self.cat_model and self.cat_le:
            try:
                pred = self.cat_model.predict([embedding])[0]
                category = self.cat_le.inverse_transform([pred])[0]
                confidence = max(self.cat_model.predict_proba([embedding])[0])
            except Exception as e:
                print(f"Category prediction error: {e}")

        # Team and Priority prediction
        team = "Unknown"
        priority = "Unknown"
        if self.team_model and self.team_le and self.priority_model and self.priority_le:
            try:
                team_pred = self.team_model.predict([embedding])[0]
                team = self.team_le.inverse_transform([team_pred])[0]
                priority_pred = self.priority_model.predict([embedding])[0]
                priority = self.priority_le.inverse_transform([priority_pred])[0]
            except Exception as e:
                print(f"Team/Priority prediction error: {e}")

        # ETA prediction
        eta = "Unknown"
        if self.ttr_model and self.ttr_le:
            try:
                ttr_pred = self.ttr_model.predict([embedding])[0]
                eta_hours = self.ttr_le.inverse_transform([ttr_pred])[0]
                eta = f"{eta_hours} hours"
            except Exception as e:
                print(f"TTR prediction error: {e}")

        # Action retrieval
        suggested_action = "Please contact support for assistance"
        if self.kb_df is not None and self.kb_embeddings is not None:
            try:
                # Semantic Similarity Search
                similarities = cosine_similarity([embedding], self.kb_embeddings)[0]
                best_idx = np.argmax(similarities)
                
                # Retrieve from DataFrame (column 'action')
                suggested_action = self.kb_df.iloc[best_idx]['action']
                print(f"[SUCCESS] Action Retrieved (Idx: {best_idx})")
            except Exception as e:
                print(f"[ERROR] Action retrieval error: {e}")

        # Routing status based on confidence
        routing_status = "Auto" if confidence > 0.8 else "Review" if confidence > 0.5 else "Escalate"

        friendly_action = f"Hello! I've analyzed this ticket. Based on our knowledge base, here is the recommended fix: {suggested_action}. I hope this helps!"
        return {
            "category": category,
            "confidence": float(confidence),
            "team": team,
            "priority": priority,
            "eta": eta,
            "suggested_action": friendly_action,
            "routing_status": routing_status
        }