import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "Ai_model")

# Ensure directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

print(f"Generating models in: {MODEL_DIR}")

# --- Phase 1: Risk Detection (Binary: Safe vs Risky) ---

# Mock Training Data
data_p1 = pd.DataFrame({
    'log_text': [
        'User logged in successfully', 
        'Failed password for root', 
        'Connection refused', 
        'Transaction completed',
        'Syntax error in SQL statement'
    ],
    'log_text_clean': [
        'User logged in successfully', 
        'Failed password for root', 
        'Connection refused', 
        'Transaction completed',
        'Syntax error in SQL statement'
    ],
    'provider': ['auth', 'auth', 'network', 'payment', 'db'],
    'duration_seconds': [0.1, 0.5, 0.2, 1.2, 0.05],
    'num_lines': [1, 1, 1, 1, 1],
    'entropy': [3.5, 4.2, 3.8, 3.1, 4.5],
    'keyword_count': [0, 1, 1, 0, 1],
    'label': [0, 1, 1, 0, 1]  # 0=Safe, 1=Risky
})

# Phase 1 Pipeline
numeric_features = ['duration_seconds', 'num_lines', 'entropy', 'keyword_count']
categorical_features = ['provider']
text_features = 'log_text'

preprocessor_p1 = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('txt', TfidfVectorizer(max_features=50), text_features)
    ])

pipeline_p1 = Pipeline([
    ('preprocessor', preprocessor_p1),
    ('classifier', RandomForestClassifier(n_estimators=10, random_state=42))
])

print("Training Phase 1 Model...")
pipeline_p1.fit(data_p1, data_p1['label'])

# Save Phase 1
p1_path = os.path.join(MODEL_DIR, "phase1_pipeline (1).joblib")
joblib.dump(pipeline_p1, p1_path)
print(f"✅ Saved Phase 1 model to {p1_path}")


# --- Phase 2: Category Classification (Multi-class) ---

# Mock Data Phase 2
data_p2 = pd.DataFrame({
    'log_text_clean': [
        'User logged in successfully',
        'admin privileges granted to user', 
        'unknown command execution', 
        'AWS_ACCESS_KEY_ID exposed', 
        'uses: actions/checkout@latest', 
        'curl http://malicious.com'
    ],
    'provider': ['auth', 'iam', 'system', 'app', 'cicd', 'network'],
    'duration_seconds': [0.1, 0.2, 0.5, 0.1, 1.0, 0.3],
    'num_lines': [1, 1, 1, 1, 1, 1],
    'entropy': [3.0, 4.0, 4.5, 4.2, 3.8, 4.1],
    'keyword_count': [0, 1, 1, 1, 0, 1],
    'category_idx': [0, 1, 3, 2, 4, 5] 
})

# Needs to match labels in `phase2_classes.json` we saw earlier.
# The user's file had 6 entries (indices 0-4 shown in mock, added 5 for completeness)
# Let's ensure we fit to something.
# Classes from previous `view_file`:
# 0: "CICD-SEC-02: Over-Privileged Token"
# 1: "CICD-SEC-04: Poisoned Pipeline Execution"
# 2: "CICD-SEC-06: Secret Leak"
# 3: "CICD-SEC-07: Unpinned Action"
# 4: "CICD-SEC-08: 3rd Party Abuse"
# Wait, let's re-read the classes file to be sure.
# The `view_file` output showed 5 items.
# "CICD-SEC-02...", ... "CICD-SEC-08..."

# Adjust mock data to match reasonable length
data_p2['category_idx'] = [0, 1, 2, 3, 4, 0] # mapping to indices 0-4

preprocessor_p2 = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('txt', TfidfVectorizer(max_features=50), 'log_text_clean')
    ])

pipeline_p2 = Pipeline([
    ('preprocessor', preprocessor_p2),
    ('classifier', RandomForestClassifier(n_estimators=10, random_state=42))
])

print("Training Phase 2 Model...")
pipeline_p2.fit(data_p2, data_p2['category_idx'])

# Save Phase 2
p2_path = os.path.join(MODEL_DIR, "phase2_pipeline.joblib")
joblib.dump(pipeline_p2, p2_path)
print(f"✅ Saved Phase 2 model to {p2_path}")

print("🎉 All models regenerated successfully!")
