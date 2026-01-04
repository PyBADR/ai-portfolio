"""
Train Classical ML Model for Insurance Claims Decision Support
==============================================================

GOVERNANCE CONSTRAINTS:
- Classical ML ONLY (XGBoost used here - NO neural networks, NO LLMs)
- Advisory system only (NO autonomous decisions)
- Must align with decision_spec.yaml frozen boundaries
- Human-in-the-loop is MANDATORY
- All outputs are NON-BINDING suggestions

Dataset: BDR-AI/insurance_decision_boundaries_v1 (Hugging Face)
Model: XGBoost Classifier
Purpose: Demonstration of AI governance principles
"""

import pandas as pd
import numpy as np
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import xgboost as xgb
import joblib
import json
from datetime import datetime

# FROZEN DECISION BOUNDARIES - DO NOT MODIFY
DECISION_BOUNDARIES = {
    'damage_thresholds': {
        'low': 5000,
        'medium': 15000,
        'high': 50000
    },
    'risk_weights': {
        'low': 1.0,
        'medium': 1.5,
        'high': 2.0
    },
    'injury_multiplier': 1.8,
    'severity_thresholds': {
        'low': 5,
        'medium': 15
    }
}

def load_and_prepare_data():
    """
    Load dataset from Hugging Face and prepare for training.
    
    Returns:
        X_train, X_test, y_train, y_test, encoders
    """
    print("=" * 70)
    print("LOADING DATASET: BDR-AI/insurance_decision_boundaries_v1")
    print("=" * 70)
    
    # Load dataset from Hugging Face
    dataset = load_dataset("BDR-AI/insurance_decision_boundaries_v1")
    df = pd.DataFrame(dataset['train'])
    
    print(f"\nDataset loaded: {len(df)} samples")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    # GOVERNANCE CHECK: Verify only allowed features present
    allowed_features = ['claim_type', 'damage_amount', 'injury_involved', 'risk_factor']
    feature_cols = [col for col in df.columns if col != 'severity']
    
    print(f"\n{'='*70}")
    print("GOVERNANCE CHECK: Verifying feature compliance")
    print(f"{'='*70}")
    print(f"Allowed features: {allowed_features}")
    print(f"Found features: {feature_cols}")
    
    for col in feature_cols:
        if col not in allowed_features:
            raise ValueError(f"GOVERNANCE VIOLATION: Unauthorized feature '{col}' found in dataset!")
    
    print("✓ Feature compliance verified - proceeding with training")
    
    # Prepare features (4 inputs only - FROZEN)
    X = df[allowed_features].copy()
    y = df['severity']
    
    print(f"\n{'='*70}")
    print("TARGET DISTRIBUTION (Advisory Severity Levels)")
    print(f"{'='*70}")
    print(y.value_counts())
    
    # Encode categorical features
    encoders = {}
    
    # Encode claim_type
    le_claim = LabelEncoder()
    X['claim_type_encoded'] = le_claim.fit_transform(X['claim_type'])
    encoders['claim_type'] = le_claim
    
    # Encode risk_factor
    le_risk = LabelEncoder()
    X['risk_factor_encoded'] = le_risk.fit_transform(X['risk_factor'])
    encoders['risk_factor'] = le_risk
    
    # Convert injury_involved to int
    X['injury_involved_encoded'] = X['injury_involved'].astype(int)
    
    # Create feature matrix with encoded values
    X_processed = X[['claim_type_encoded', 'damage_amount', 'injury_involved_encoded', 'risk_factor_encoded']].copy()
    X_processed.columns = ['claim_type', 'damage_amount', 'injury_involved', 'risk_factor']
    
    # Encode target
    le_target = LabelEncoder()
    y_encoded = le_target.fit_transform(y)
    encoders['target'] = le_target
    
    print(f"\n{'='*70}")
    print("ENCODING SUMMARY")
    print(f"{'='*70}")
    print(f"claim_type mapping: {dict(zip(le_claim.classes_, le_claim.transform(le_claim.classes_)))}")
    print(f"risk_factor mapping: {dict(zip(le_risk.classes_, le_risk.transform(le_risk.classes_)))}")
    print(f"target mapping: {dict(zip(le_target.classes_, le_target.transform(le_target.classes_)))}")
    
    # Train-test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"\n{'='*70}")
    print("TRAIN/TEST SPLIT")
    print(f"{'='*70}")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test, encoders

def train_model(X_train, y_train):
    """
    Train XGBoost classifier (classical ML).
    
    GOVERNANCE: XGBoost is a classical ML algorithm (tree-based).
                NO neural networks, NO LLMs, NO reinforcement learning.
    """
    print(f"\n{'='*70}")
    print("TRAINING XGBOOST CLASSIFIER (Classical ML)")
    print(f"{'='*70}")
    print("Model type: XGBoost (tree-based gradient boosting)")
    print("Governance status: ✓ Classical ML approved")
    print("Autonomous decisions: ✗ DISABLED (advisory only)")
    
    # Train XGBoost model
    model = xgb.XGBClassifier(
        objective='multi:softprob',
        num_class=3,
        max_depth=6,
        learning_rate=0.1,
        n_estimators=100,
        random_state=42,
        eval_metric='mlogloss'
    )
    
    model.fit(X_train, y_train)
    
    print("\n✓ Model training complete")
    
    return model

def evaluate_model(model, X_test, y_test, encoders):
    """
    Evaluate model performance on test set.
    """
    print(f"\n{'='*70}")
    print("MODEL EVALUATION")
    print(f"{'='*70}")
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nTest Set Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Classification report
    target_names = encoders['target'].classes_
    print(f"\n{'='*70}")
    print("CLASSIFICATION REPORT (Advisory Predictions)")
    print(f"{'='*70}")
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"{'='*70}")
    print("CONFUSION MATRIX")
    print(f"{'='*70}")
    print(f"              Predicted")
    print(f"              Low  Medium  High")
    for i, label in enumerate(target_names):
        print(f"Actual {label:8s} {cm[i]}")
    
    # Feature importance
    feature_importance = model.feature_importances_
    feature_names = ['claim_type', 'damage_amount', 'injury_involved', 'risk_factor']
    
    print(f"\n{'='*70}")
    print("FEATURE IMPORTANCE (Explainability)")
    print(f"{'='*70}")
    for name, importance in sorted(zip(feature_names, feature_importance), key=lambda x: x[1], reverse=True):
        print(f"{name:20s}: {importance:.4f}")
    
    return {
        'accuracy': accuracy,
        'classification_report': classification_report(y_test, y_pred, target_names=target_names, output_dict=True),
        'confusion_matrix': cm.tolist(),
        'feature_importance': dict(zip(feature_names, feature_importance.tolist()))
    }

def save_artifacts(model, encoders, metrics):
    """
    Save trained model, encoders, and metrics.
    """
    print(f"\n{'='*70}")
    print("SAVING MODEL ARTIFACTS")
    print(f"{'='*70}")
    
    # Save model
    joblib.dump(model, 'model.pkl')
    print("✓ Model saved to: model.pkl")
    
    # Save encoders
    joblib.dump(encoders, 'encoders.pkl')
    print("✓ Encoders saved to: encoders.pkl")
    
    # Save metrics and metadata
    metadata = {
        'model_type': 'XGBoost Classifier',
        'model_architecture': 'Classical ML (tree-based gradient boosting)',
        'governance_status': 'ADVISORY ONLY - NO AUTONOMOUS DECISIONS',
        'human_review_required': True,
        'training_date': datetime.now().isoformat(),
        'dataset': 'BDR-AI/insurance_decision_boundaries_v1',
        'dataset_type': 'synthetic',
        'features': ['claim_type', 'damage_amount', 'injury_involved', 'risk_factor'],
        'target': 'severity (advisory levels: Low/Medium/High)',
        'decision_boundaries': DECISION_BOUNDARIES,
        'metrics': metrics
    }
    
    with open('model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    print("✓ Metadata saved to: model_metadata.json")
    
    print(f"\n{'='*70}")
    print("GOVERNANCE REMINDER")
    print(f"{'='*70}")
    print("⚠ This model produces ADVISORY outputs only")
    print("⚠ Human confirmation is MANDATORY for all decisions")
    print("⚠ All outputs are NON-BINDING suggestions")
    print("⚠ Audit trail must be maintained for all uses")

def main():
    """
    Main training pipeline.
    """
    print("\n" + "="*70)
    print("INSURANCE DECISION SUPPORT MODEL - TRAINING PIPELINE")
    print("="*70)
    print("Governance Mode: ADVISORY (Human-in-the-Loop Required)")
    print("Model Type: Classical ML (XGBoost)")
    print("Autonomous Decisions: DISABLED")
    print("="*70 + "\n")
    
    # Load and prepare data
    X_train, X_test, y_train, y_test, encoders = load_and_prepare_data()
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    metrics = evaluate_model(model, X_test, y_test, encoders)
    
    # Save artifacts
    save_artifacts(model, encoders, metrics)
    
    print(f"\n{'='*70}")
    print("TRAINING COMPLETE")
    print(f"{'='*70}")
    print(f"✓ Model accuracy: {metrics['accuracy']*100:.2f}%")
    print(f"✓ Model saved: model.pkl")
    print(f"✓ Encoders saved: encoders.pkl")
    print(f"✓ Metadata saved: model_metadata.json")
    print(f"\n{'='*70}")
    print("NEXT STEPS:")
    print("  1. Run evaluate.py for detailed evaluation")
    print("  2. Run predict.py for advisory predictions")
    print("  3. Review model_card.md for limitations")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
