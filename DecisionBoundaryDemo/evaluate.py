"""
Evaluate Classical ML Model for Insurance Claims Decision Support
=================================================================

GOVERNANCE CONSTRAINTS:
- Advisory system only (NO autonomous decisions)
- Human-in-the-loop is MANDATORY
- All outputs are NON-BINDING suggestions
- Evaluate confidence calibration and uncertainty quantification

Purpose: Comprehensive evaluation of trained model
"""

import pandas as pd
import numpy as np
import joblib
import json
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, 
    accuracy_score, 
    precision_recall_fscore_support,
    confusion_matrix,
    log_loss
)
from sklearn.preprocessing import LabelEncoder

def load_test_data():
    """
    Load test data (same split as training).
    """
    print("=" * 70)
    print("LOADING TEST DATA")
    print("=" * 70)
    
    # Load dataset
    dataset = load_dataset("BDR-AI/insurance_decision_boundaries_v1")
    df = pd.DataFrame(dataset['train'])
    
    # Load encoders
    encoders = joblib.load('encoders.pkl')
    
    # Prepare features
    allowed_features = ['claim_type', 'damage_amount', 'injury_involved', 'risk_factor']
    X = df[allowed_features].copy()
    y = df['severity']
    
    # Encode features
    X['claim_type_encoded'] = encoders['claim_type'].transform(X['claim_type'])
    X['risk_factor_encoded'] = encoders['risk_factor'].transform(X['risk_factor'])
    X['injury_involved_encoded'] = X['injury_involved'].astype(int)
    
    X_processed = X[['claim_type_encoded', 'damage_amount', 'injury_involved_encoded', 'risk_factor_encoded']].copy()
    X_processed.columns = ['claim_type', 'damage_amount', 'injury_involved', 'risk_factor']
    
    # Encode target
    y_encoded = encoders['target'].transform(y)
    
    # Use same split as training
    _, X_test, _, y_test = train_test_split(
        X_processed, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"✓ Test set loaded: {len(X_test)} samples")
    
    return X_test, y_test, encoders

def evaluate_classification_performance(model, X_test, y_test, encoders):
    """
    Evaluate classification metrics.
    """
    print(f"\n{'='*70}")
    print("CLASSIFICATION PERFORMANCE EVALUATION")
    print(f"{'='*70}")
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Get class names
    target_names = encoders['target'].classes_
    
    # Overall accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nOverall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Detailed classification report
    print(f"\n{'='*70}")
    print("DETAILED CLASSIFICATION REPORT")
    print(f"{'='*70}")
    report = classification_report(y_test, y_pred, target_names=target_names, digits=4)
    print(report)
    report_dict = classification_report(y_test, y_pred, target_names=target_names, output_dict=True)
    
    # Per-class metrics
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average=None)
    
    print(f"{'='*70}")
    print("PER-CLASS METRICS (Advisory Severity Levels)")
    print(f"{'='*70}")
    print(f"{'Class':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("-" * 70)
    for i, class_name in enumerate(target_names):
        print(f"{class_name:<15} {precision[i]:<12.4f} {recall[i]:<12.4f} {f1[i]:<12.4f} {support[i]:<10}")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n{'='*70}")
    print("CONFUSION MATRIX")
    print(f"{'='*70}")
    print(f"              Predicted")
    print(f"              {' '.join([f'{name:8s}' for name in target_names])}")
    for i, label in enumerate(target_names):
        values = ' '.join([f'{cm[i][j]:8d}' for j in range(len(target_names))])
        print(f"Actual {label:8s} {values}")
    
    # Calculate log loss (confidence calibration indicator)
    logloss = log_loss(y_test, y_pred_proba)
    print(f"\n{'='*70}")
    print("CONFIDENCE CALIBRATION")
    print(f"{'='*70}")
    print(f"Log Loss: {logloss:.4f}")
    print("(Lower is better - indicates better calibrated confidence scores)")
    
    return {
        'accuracy': accuracy,
        'precision': precision.tolist(),
        'recall': recall.tolist(),
        'f1_score': f1.tolist(),
        'support': support.tolist(),
        'confusion_matrix': cm.tolist(),
        'log_loss': logloss,
        'classification_report': report_dict
    }

def evaluate_confidence_distribution(model, X_test, y_test, encoders):
    """
    Analyze confidence score distribution.
    """
    print(f"\n{'='*70}")
    print("CONFIDENCE SCORE DISTRIBUTION ANALYSIS")
    print(f"{'='*70}")
    
    y_pred_proba = model.predict_proba(X_test)
    y_pred = model.predict(X_test)
    
    # Get max confidence for each prediction
    max_confidence = np.max(y_pred_proba, axis=1)
    
    print(f"\nConfidence Statistics:")
    print(f"  Mean confidence: {np.mean(max_confidence):.4f}")
    print(f"  Median confidence: {np.median(max_confidence):.4f}")
    print(f"  Min confidence: {np.min(max_confidence):.4f}")
    print(f"  Max confidence: {np.max(max_confidence):.4f}")
    print(f"  Std deviation: {np.std(max_confidence):.4f}")
    
    # Confidence distribution by bins
    bins = [0.0, 0.5, 0.7, 0.8, 0.9, 1.0]
    bin_labels = ['0.0-0.5', '0.5-0.7', '0.7-0.8', '0.8-0.9', '0.9-1.0']
    
    print(f"\n{'='*70}")
    print("CONFIDENCE DISTRIBUTION BY BINS")
    print(f"{'='*70}")
    print(f"{'Confidence Range':<20} {'Count':<10} {'Percentage':<12}")
    print("-" * 70)
    
    for i in range(len(bins)-1):
        mask = (max_confidence >= bins[i]) & (max_confidence < bins[i+1])
        if i == len(bins)-2:  # Last bin includes 1.0
            mask = (max_confidence >= bins[i]) & (max_confidence <= bins[i+1])
        count = np.sum(mask)
        percentage = (count / len(max_confidence)) * 100
        print(f"{bin_labels[i]:<20} {count:<10} {percentage:>6.2f}%")
    
    # Accuracy by confidence level
    print(f"\n{'='*70}")
    print("ACCURACY BY CONFIDENCE LEVEL")
    print(f"{'='*70}")
    print(f"{'Confidence Range':<20} {'Accuracy':<12} {'Sample Count':<15}")
    print("-" * 70)
    
    for i in range(len(bins)-1):
        mask = (max_confidence >= bins[i]) & (max_confidence < bins[i+1])
        if i == len(bins)-2:
            mask = (max_confidence >= bins[i]) & (max_confidence <= bins[i+1])
        
        if np.sum(mask) > 0:
            acc = accuracy_score(y_test[mask], y_pred[mask])
            print(f"{bin_labels[i]:<20} {acc:<12.4f} {np.sum(mask):<15}")
    
    return {
        'mean_confidence': float(np.mean(max_confidence)),
        'median_confidence': float(np.median(max_confidence)),
        'min_confidence': float(np.min(max_confidence)),
        'max_confidence': float(np.max(max_confidence)),
        'std_confidence': float(np.std(max_confidence))
    }

def evaluate_feature_importance(model, encoders):
    """
    Analyze feature importance for explainability.
    """
    print(f"\n{'='*70}")
    print("FEATURE IMPORTANCE ANALYSIS (Explainability)")
    print(f"{'='*70}")
    
    feature_names = ['claim_type', 'damage_amount', 'injury_involved', 'risk_factor']
    feature_importance = model.feature_importances_
    
    # Sort by importance
    importance_pairs = sorted(zip(feature_names, feature_importance), key=lambda x: x[1], reverse=True)
    
    print(f"\n{'Feature':<20} {'Importance':<12} {'Relative %':<12}")
    print("-" * 70)
    
    total_importance = sum(feature_importance)
    for name, importance in importance_pairs:
        relative_pct = (importance / total_importance) * 100
        print(f"{name:<20} {importance:<12.4f} {relative_pct:>6.2f}%")
    
    print(f"\n{'='*70}")
    print("FEATURE IMPORTANCE INTERPRETATION")
    print(f"{'='*70}")
    print("Higher importance = Greater influence on advisory predictions")
    print("This helps humans understand which factors drive the model's suggestions")
    
    return dict(zip(feature_names, feature_importance.tolist()))

def evaluate_uncertainty_quantification(model, X_test, encoders):
    """
    Evaluate uncertainty quantification quality.
    """
    print(f"\n{'='*70}")
    print("UNCERTAINTY QUANTIFICATION ASSESSMENT")
    print(f"{'='*70}")
    
    y_pred_proba = model.predict_proba(X_test)
    
    # Calculate entropy as uncertainty measure
    # Higher entropy = More uncertain
    epsilon = 1e-10  # Avoid log(0)
    entropy = -np.sum(y_pred_proba * np.log(y_pred_proba + epsilon), axis=1)
    max_entropy = np.log(y_pred_proba.shape[1])  # Max entropy for uniform distribution
    normalized_entropy = entropy / max_entropy
    
    print(f"\nEntropy-based Uncertainty Statistics:")
    print(f"  Mean entropy: {np.mean(entropy):.4f}")
    print(f"  Mean normalized entropy: {np.mean(normalized_entropy):.4f}")
    print(f"  (0.0 = certain, 1.0 = maximum uncertainty)")
    
    # Classify uncertainty levels
    low_uncertainty = np.sum(normalized_entropy < 0.3)
    medium_uncertainty = np.sum((normalized_entropy >= 0.3) & (normalized_entropy < 0.6))
    high_uncertainty = np.sum(normalized_entropy >= 0.6)
    
    print(f"\n{'='*70}")
    print("UNCERTAINTY LEVEL DISTRIBUTION")
    print(f"{'='*70}")
    print(f"Low uncertainty (<0.3):     {low_uncertainty:5d} ({low_uncertainty/len(entropy)*100:>5.1f}%)")
    print(f"Medium uncertainty (0.3-0.6): {medium_uncertainty:5d} ({medium_uncertainty/len(entropy)*100:>5.1f}%)")
    print(f"High uncertainty (≥0.6):     {high_uncertainty:5d} ({high_uncertainty/len(entropy)*100:>5.1f}%)")
    
    print(f"\n{'='*70}")
    print("GOVERNANCE NOTE: Uncertainty Quantification")
    print(f"{'='*70}")
    print("⚠ High uncertainty predictions should receive EXTRA human scrutiny")
    print("⚠ Human reviewers should prioritize cases with uncertainty ≥ 0.6")
    print("⚠ All predictions require human confirmation regardless of confidence")
    
    return {
        'mean_entropy': float(np.mean(entropy)),
        'mean_normalized_entropy': float(np.mean(normalized_entropy)),
        'low_uncertainty_count': int(low_uncertainty),
        'medium_uncertainty_count': int(medium_uncertainty),
        'high_uncertainty_count': int(high_uncertainty)
    }

def governance_compliance_check():
    """
    Verify model complies with governance constraints.
    """
    print(f"\n{'='*70}")
    print("GOVERNANCE COMPLIANCE VERIFICATION")
    print(f"{'='*70}")
    
    # Load metadata
    with open('model_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    checks = []
    
    # Check 1: Model type
    model_type = metadata.get('model_type', '')
    is_classical = 'XGBoost' in model_type or 'Random Forest' in model_type or 'Logistic' in model_type
    checks.append(('Classical ML model (no neural networks)', is_classical))
    
    # Check 2: Advisory status
    is_advisory = metadata.get('governance_status', '').upper().find('ADVISORY') >= 0
    checks.append(('Advisory-only system (no autonomous decisions)', is_advisory))
    
    # Check 3: Human review required
    human_required = metadata.get('human_review_required', False)
    checks.append(('Human review required', human_required))
    
    # Check 4: Correct features
    features = metadata.get('features', [])
    correct_features = set(features) == {'claim_type', 'damage_amount', 'injury_involved', 'risk_factor'}
    checks.append(('Only allowed features used (4 features)', correct_features))
    
    # Check 5: Frozen decision boundaries present
    has_boundaries = 'decision_boundaries' in metadata
    checks.append(('Decision boundaries documented', has_boundaries))
    
    # Print results
    all_passed = True
    for check_name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}  {check_name}")
        if not passed:
            all_passed = False
    
    print(f"\n{'='*70}")
    if all_passed:
        print("✓ ALL GOVERNANCE CHECKS PASSED")
    else:
        print("✗ GOVERNANCE VIOLATIONS DETECTED - REVIEW REQUIRED")
    print(f"{'='*70}")
    
    return all_passed

def save_evaluation_report(metrics):
    """
    Save comprehensive evaluation report.
    """
    print(f"\n{'='*70}")
    print("SAVING EVALUATION REPORT")
    print(f"{'='*70}")
    
    with open('evaluation_report.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("✓ Evaluation report saved to: evaluation_report.json")

def main():
    """
    Main evaluation pipeline.
    """
    print("\n" + "="*70)
    print("INSURANCE DECISION SUPPORT MODEL - EVALUATION PIPELINE")
    print("="*70)
    print("Governance Mode: ADVISORY (Human-in-the-Loop Required)")
    print("Purpose: Evaluate model performance and compliance")
    print("="*70 + "\n")
    
    # Load model
    print("Loading trained model...")
    model = joblib.load('model.pkl')
    print("✓ Model loaded successfully\n")
    
    # Load test data
    X_test, y_test, encoders = load_test_data()
    
    # Evaluate classification performance
    classification_metrics = evaluate_classification_performance(model, X_test, y_test, encoders)
    
    # Evaluate confidence distribution
    confidence_metrics = evaluate_confidence_distribution(model, X_test, y_test, encoders)
    
    # Evaluate feature importance
    feature_importance = evaluate_feature_importance(model, encoders)
    
    # Evaluate uncertainty quantification
    uncertainty_metrics = evaluate_uncertainty_quantification(model, X_test, encoders)
    
    # Governance compliance check
    governance_passed = governance_compliance_check()
    
    # Compile all metrics
    evaluation_report = {
        'evaluation_date': pd.Timestamp.now().isoformat(),
        'model_file': 'model.pkl',
        'test_samples': len(X_test),
        'classification_metrics': classification_metrics,
        'confidence_metrics': confidence_metrics,
        'feature_importance': feature_importance,
        'uncertainty_metrics': uncertainty_metrics,
        'governance_compliance': governance_passed
    }
    
    # Save report
    save_evaluation_report(evaluation_report)
    
    print(f"\n{'='*70}")
    print("EVALUATION COMPLETE")
    print(f"{'='*70}")
    print(f"✓ Test accuracy: {classification_metrics['accuracy']*100:.2f}%")
    print(f"✓ Mean confidence: {confidence_metrics['mean_confidence']:.4f}")
    print(f"✓ Governance compliance: {'PASSED' if governance_passed else 'FAILED'}")
    print(f"✓ Report saved: evaluation_report.json")
    print(f"\n{'='*70}")
    print("GOVERNANCE REMINDER")
    print(f"{'='*70}")
    print("⚠ This model produces ADVISORY outputs only")
    print("⚠ Human confirmation is MANDATORY for all decisions")
    print("⚠ High uncertainty cases require EXTRA human scrutiny")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
