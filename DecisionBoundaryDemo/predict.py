"""
Make Advisory Predictions with Explainability
=============================================

GOVERNANCE CONSTRAINTS:
- Advisory system only (NO autonomous decisions)
- Human-in-the-loop is MANDATORY
- All outputs are NON-BINDING suggestions
- Full explainability required (confidence, feature importance, rule signals)

Purpose: Generate advisory predictions with complete transparency
"""

import numpy as np
import joblib
import json
import yaml
from datetime import datetime

# FROZEN DECISION BOUNDARIES - DO NOT MODIFY (from decision_spec.yaml)
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

def load_model_artifacts():
    """
    Load trained model and encoders.
    """
    model = joblib.load('model.pkl')
    encoders = joblib.load('encoders.pkl')
    
    with open('model_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    return model, encoders, metadata

def generate_rule_signals(claim_type, damage_amount, injury_involved, risk_factor):
    """
    Generate human-readable rule signals based on frozen decision boundaries.
    
    This provides transparent explanation of which rules are triggered.
    """
    signals = []
    
    # Damage threshold signals
    if damage_amount < DECISION_BOUNDARIES['damage_thresholds']['low']:
        signals.append(f"✓ Low damage (<${DECISION_BOUNDARIES['damage_thresholds']['low']:,}): ${damage_amount:,.2f}")
    elif damage_amount < DECISION_BOUNDARIES['damage_thresholds']['medium']:
        signals.append(f"⚠ Medium damage (${DECISION_BOUNDARIES['damage_thresholds']['low']:,}-${DECISION_BOUNDARIES['damage_thresholds']['medium']:,}): ${damage_amount:,.2f}")
    elif damage_amount < DECISION_BOUNDARIES['damage_thresholds']['high']:
        signals.append(f"⚠⚠ High damage (${DECISION_BOUNDARIES['damage_thresholds']['medium']:,}-${DECISION_BOUNDARIES['damage_thresholds']['high']:,}): ${damage_amount:,.2f}")
    else:
        signals.append(f"⚠⚠⚠ Very high damage (≥${DECISION_BOUNDARIES['damage_thresholds']['high']:,}): ${damage_amount:,.2f}")
    
    # Injury signal
    if injury_involved:
        signals.append(f"⚠ Injury involved (multiplier: {DECISION_BOUNDARIES['injury_multiplier']}x)")
    else:
        signals.append(f"✓ No injury involved")
    
    # Risk factor signal
    risk_weight = DECISION_BOUNDARIES['risk_weights'][risk_factor.lower()]
    if risk_factor.lower() == 'high':
        signals.append(f"⚠⚠ High risk factor (weight: {risk_weight}x)")
    elif risk_factor.lower() == 'medium':
        signals.append(f"⚠ Medium risk factor (weight: {risk_weight}x)")
    else:
        signals.append(f"✓ Low risk factor (weight: {risk_weight}x)")
    
    # Claim type signal
    if claim_type == "Liability":
        signals.append(f"⚠ Liability claim (additional multiplier applied)")
    else:
        signals.append(f"Claim type: {claim_type}")
    
    return signals

def calculate_uncertainty(prediction_proba):
    """
    Calculate prediction uncertainty using entropy.
    
    Returns:
        dict with uncertainty level and metrics
    """
    # Calculate entropy
    epsilon = 1e-10
    entropy = -np.sum(prediction_proba * np.log(prediction_proba + epsilon))
    max_entropy = np.log(len(prediction_proba))
    normalized_entropy = entropy / max_entropy
    
    # Determine uncertainty level
    if normalized_entropy < 0.3:
        level = "Low"
        interpretation = "Model is confident in this prediction"
    elif normalized_entropy < 0.6:
        level = "Medium"
        interpretation = "Model has moderate uncertainty - extra human scrutiny recommended"
    else:
        level = "High"
        interpretation = "Model is uncertain - REQUIRES careful human review"
    
    return {
        'level': level,
        'entropy': float(entropy),
        'normalized_entropy': float(normalized_entropy),
        'interpretation': interpretation,
        'confidence_distribution': {
            'Low': float(prediction_proba[0]),
            'Medium': float(prediction_proba[1]) if len(prediction_proba) > 1 else 0.0,
            'High': float(prediction_proba[2]) if len(prediction_proba) > 2 else 0.0
        }
    }

def get_feature_importance_for_prediction(model, feature_values):
    """
    Get feature importance specific to this prediction.
    
    Uses the model's global feature importance as a proxy.
    For tree-based models, this represents which features were most influential.
    """
    feature_names = ['claim_type', 'damage_amount', 'injury_involved', 'risk_factor']
    global_importance = model.feature_importances_
    
    # Create importance dictionary
    importance_dict = {}
    for name, importance, value in zip(feature_names, global_importance, feature_values):
        importance_dict[name] = {
            'importance_score': float(importance),
            'value': value,
            'relative_percentage': float(importance / np.sum(global_importance) * 100)
        }
    
    # Sort by importance
    sorted_features = sorted(importance_dict.items(), key=lambda x: x[1]['importance_score'], reverse=True)
    
    return dict(sorted_features)

def predict_claim(claim_type, damage_amount, injury_involved, risk_factor):
    """
    Make advisory prediction for insurance claim.
    
    Args:
        claim_type: str - "Auto", "Property", "Health", or "Liability"
        damage_amount: float - Damage amount in USD
        injury_involved: bool - Whether injury is involved
        risk_factor: str - "low", "medium", or "high"
    
    Returns:
        dict with complete advisory prediction and explainability
    """
    # Load model artifacts
    model, encoders, metadata = load_model_artifacts()
    
    # Validate inputs
    valid_claim_types = ['Auto', 'Property', 'Health', 'Liability']
    valid_risk_factors = ['low', 'medium', 'high']
    
    if claim_type not in valid_claim_types:
        raise ValueError(f"Invalid claim_type. Must be one of: {valid_claim_types}")
    
    if risk_factor not in valid_risk_factors:
        raise ValueError(f"Invalid risk_factor. Must be one of: {valid_risk_factors}")
    
    if damage_amount < 0:
        raise ValueError("damage_amount must be non-negative")
    
    # Encode inputs
    claim_type_encoded = encoders['claim_type'].transform([claim_type])[0]
    risk_factor_encoded = encoders['risk_factor'].transform([risk_factor])[0]
    injury_involved_encoded = int(injury_involved)
    
    # Create feature vector
    features = np.array([[
        claim_type_encoded,
        damage_amount,
        injury_involved_encoded,
        risk_factor_encoded
    ]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    prediction_proba = model.predict_proba(features)[0]
    
    # Get severity label
    severity = encoders['target'].inverse_transform([prediction])[0]
    confidence = float(np.max(prediction_proba))
    
    # Generate explainability artifacts
    rule_signals = generate_rule_signals(claim_type, damage_amount, injury_involved, risk_factor)
    uncertainty = calculate_uncertainty(prediction_proba)
    feature_importance = get_feature_importance_for_prediction(
        model, 
        [claim_type, damage_amount, injury_involved, risk_factor]
    )
    
    # Compile advisory output
    advisory_output = {
        # GOVERNANCE: All outputs clearly marked as ADVISORY
        'governance_status': '⚠ ADVISORY ONLY - HUMAN CONFIRMATION REQUIRED',
        'decision_authority': 'HUMAN (not machine)',
        'binding': False,
        'requires_human_review': True,
        
        # Model suggestion (NON-BINDING)
        'model_suggestion': f"{severity} Severity (Advisory)",
        'severity_level': severity,
        'confidence_score': confidence,
        
        # Input summary
        'input_summary': {
            'claim_type': claim_type,
            'damage_amount': f"${damage_amount:,.2f}",
            'injury_involved': 'Yes' if injury_involved else 'No',
            'risk_factor': risk_factor
        },
        
        # Explainability
        'rule_signals': rule_signals,
        'feature_importance': feature_importance,
        'uncertainty_assessment': uncertainty,
        
        # Prediction metadata
        'prediction_metadata': {
            'model_type': metadata['model_type'],
            'model_architecture': metadata['model_architecture'],
            'prediction_timestamp': datetime.now().isoformat(),
            'dataset_source': metadata['dataset']
        },
        
        # Governance reminders
        'governance_reminders': [
            '⚠ This is an ADVISORY suggestion only',
            '⚠ Human decision-maker has FULL AUTHORITY to accept or override',
            '⚠ Human must independently evaluate the claim',
            '⚠ Human must document rationale for final decision',
            '⚠ All decisions must be logged in audit trail'
        ],
        
        # Decision boundaries reference
        'decision_boundaries_reference': DECISION_BOUNDARIES
    }
    
    return advisory_output

def format_advisory_output(output):
    """
    Format advisory output for human-readable display.
    """
    print("\n" + "="*70)
    print("INSURANCE CLAIM ADVISORY PREDICTION")
    print("="*70)
    print(f"\n{output['governance_status']}")
    print(f"Decision Authority: {output['decision_authority']}")
    print(f"Binding: {output['binding']}")
    
    print(f"\n{'='*70}")
    print("INPUT SUMMARY")
    print(f"{'='*70}")
    for key, value in output['input_summary'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n{'='*70}")
    print("MODEL ADVISORY SUGGESTION (Non-Binding)")
    print(f"{'='*70}")
    print(f"  Suggested Severity: {output['model_suggestion']}")
    print(f"  Model Confidence: {output['confidence_score']:.4f} ({output['confidence_score']*100:.2f}%)")
    
    print(f"\n{'='*70}")
    print("RULE SIGNALS (Transparent Decision Factors)")
    print(f"{'='*70}")
    for signal in output['rule_signals']:
        print(f"  {signal}")
    
    print(f"\n{'='*70}")
    print("FEATURE IMPORTANCE (What Influenced This Suggestion)")
    print(f"{'='*70}")
    for feature, details in output['feature_importance'].items():
        print(f"  {feature}: {details['relative_percentage']:.1f}% importance")
    
    print(f"\n{'='*70}")
    print("UNCERTAINTY ASSESSMENT")
    print(f"{'='*70}")
    uncertainty = output['uncertainty_assessment']
    print(f"  Uncertainty Level: {uncertainty['level']}")
    print(f"  Normalized Entropy: {uncertainty['normalized_entropy']:.4f}")
    print(f"  Interpretation: {uncertainty['interpretation']}")
    
    print(f"\n  Confidence Distribution:")
    for severity, prob in uncertainty['confidence_distribution'].items():
        print(f"    {severity}: {prob:.4f} ({prob*100:.2f}%)")
    
    print(f"\n{'='*70}")
    print("GOVERNANCE REMINDERS")
    print(f"{'='*70}")
    for reminder in output['governance_reminders']:
        print(f"  {reminder}")
    
    print(f"\n{'='*70}\n")

def main():
    """
    Example usage with sample claims.
    """
    print("\n" + "="*70)
    print("ADVISORY PREDICTION SYSTEM - DEMONSTRATION")
    print("="*70)
    print("Model Type: Classical ML (XGBoost)")
    print("Governance: Human-in-the-Loop Required")
    print("="*70 + "\n")
    
    # Example 1: Low severity claim
    print("\n" + "="*70)
    print("EXAMPLE 1: Low Damage Auto Claim")
    print("="*70)
    output1 = predict_claim(
        claim_type="Auto",
        damage_amount=2500.0,
        injury_involved=False,
        risk_factor="low"
    )
    format_advisory_output(output1)
    
    # Example 2: High severity claim
    print("\n" + "="*70)
    print("EXAMPLE 2: High Damage Liability Claim with Injury")
    print("="*70)
    output2 = predict_claim(
        claim_type="Liability",
        damage_amount=75000.0,
        injury_involved=True,
        risk_factor="high"
    )
    format_advisory_output(output2)
    
    # Example 3: Medium severity claim
    print("\n" + "="*70)
    print("EXAMPLE 3: Medium Damage Property Claim")
    print("="*70)
    output3 = predict_claim(
        claim_type="Property",
        damage_amount=12000.0,
        injury_involved=False,
        risk_factor="medium"
    )
    format_advisory_output(output3)
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nTo use this module in your code:")
    print("  from predict import predict_claim")
    print("  result = predict_claim('Auto', 5000.0, False, 'low')")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
