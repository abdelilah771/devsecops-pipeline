import os
import joblib
import json
import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for paths - assuming models are in 'Ai_model' directory in the root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "Ai_model")

class AIEngine:
    def __init__(self):
        self.phase1_pipeline = None
        self.phase1_config = {}
        self.phase2_pipeline = None
        self.phase2_config = {}
        self.phase2_classes = []
        self.models_loaded = False

    def load_models(self):
        """
        Loads Phase 1 and Phase 2 models and configurations from the Ai_model directory.
        """
        try:
            logger.info("Loading AI Models from %s...", MODEL_DIR)

            # Phase 1
            p1_config_path = os.path.join(MODEL_DIR, "phase1_config (1).json")
            with open(p1_config_path, "r") as f:
                self.phase1_config = json.load(f)
            
            p1_model_path = os.path.join(MODEL_DIR, "phase1_pipeline (1).joblib")
            self.phase1_pipeline = joblib.load(p1_model_path)

            # Phase 2
            p2_config_path = os.path.join(MODEL_DIR, "phase2_config.json")
            with open(p2_config_path, "r") as f:
                self.phase2_config = json.load(f)
            
            p2_model_path = os.path.join(MODEL_DIR, "phase2_pipeline.joblib")
            self.phase2_pipeline = joblib.load(p2_model_path)

            # Phase 2 Classes (Label Encoding)
            p2_classes_path = os.path.join(MODEL_DIR, "phase2_classes.json")
            with open(p2_classes_path, "r") as f:
                self.phase2_classes = json.load(f)

            self.models_loaded = True
            logger.info("AI Models loaded successfully.")

        except Exception as e:
            logger.error("Failed to load AI models: %s", e)
            self.models_loaded = False

    def extract_features(self, message: str, provider: str, duration_seconds: float = 0.0) -> pd.DataFrame:
        """
        Extracts features required by the models from a single log message.
        """
        # Basic feature extraction logic matching training time
        # This MUST be consistent with how the models were trained
        
        # 1. log_text / log_text_clean
        log_text = str(message)
        
        # 2. num_lines (assuming 1 for single event, or count newlines if multiline)
        num_lines = log_text.count('\n') + 1

        # 3. entropy (Simple Shannon entropy estimation)
        import math
        from collections import Counter
        
        prob = [float(log_text.count(c)) / len(log_text) for c in dict.fromkeys(list(log_text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob]) if prob else 0.0

        # 4. keyword_count (Count specific suspicious keywords - simplified)
        # In a real scenario, this should match exactly the list used during training
        keywords = ["error", "fail", "exception", "fatal", "denied", "forbidden", "unauthorized"]
        keyword_count = sum(1 for k in keywords if k in log_text.lower())

        # Construct DataFrame
        # Phase 1 expects: log_text, provider, duration_seconds, num_lines, entropy, keyword_count
        # Phase 2 expects: log_text_clean, provider, duration_seconds, num_lines, entropy, keyword_count
        
        data = {
            "log_text": [log_text],
            "log_text_clean": [log_text], # Assuming minimal cleaning for now
            "provider": [provider],
            "duration_seconds": [duration_seconds],
            "num_lines": [num_lines],
            "entropy": [entropy],
            "keyword_count": [keyword_count]
        }
        
        return pd.DataFrame(data)

    def predict_risk(self, df: pd.DataFrame) -> Tuple[bool, float]:
        """
        Runs Phase 1 model to detect if the log is risky.
        Returns (is_risky, risk_score)
        """
        if not self.models_loaded:
            return False, 0.0

        try:
            # Predict probability
            # The model is likely a classifier, so predict_proba gives [prob_safe, prob_risky]
            probs = self.phase1_pipeline.predict_proba(df)
            risk_score = probs[0][1] # Probability of class 1 (Risky)
            
            threshold = self.phase1_config.get("threshold", 0.5)
            is_risky = risk_score >= threshold
            
            return is_risky, risk_score
        except Exception as e:
            logger.error("Phase 1 prediction failed: %s", e)
            return False, 0.0

    def predict_category(self, df: pd.DataFrame) -> Tuple[str, float]:
        """
        Runs Phase 2 model to classify the specific OWASP category.
        Returns (category_name, confidence)
        """
        if not self.models_loaded:
            return "Unknown", 0.0

        try:
            # Predict class
            probs = self.phase2_pipeline.predict_proba(df)
            top_class_idx = np.argmax(probs[0])
            confidence = probs[0][top_class_idx]
            
            # Map index to class name
            if 0 <= top_class_idx < len(self.phase2_classes):
                category = self.phase2_classes[top_class_idx]
            else:
                category = "Unknown"

            return category, confidence
        except Exception as e:
            logger.error("Phase 2 prediction failed: %s", e)
            return "Unknown", 0.0

# Singleton instance
ai_engine = AIEngine()
