# Model Card: Insurance Claims Decision Support System

**Model Version**: 1.0.0  
**Last Updated**: 2026-01-04  
**Model Type**: Classical Machine Learning (XGBoost Classifier)  
**Governance Status**: ADVISORY ONLY - Human-in-the-Loop Required  

---

## Model Description

### Overview
This model is a **classical machine learning classifier** designed to provide **advisory suggestions** for insurance claim severity assessment. It uses XGBoost (gradient boosting decision trees) to analyze claim characteristics and suggest severity levels.

**CRITICAL: This is NOT an autonomous decision-making system.** All outputs are advisory suggestions that require mandatory human review and confirmation.

### Architecture
- **Algorithm**: XGBoost Classifier (tree-based gradient boosting)
- **Type**: Classical ML (NOT neural networks, NOT deep learning, NOT LLMs)
- **Training**: Supervised learning on synthetic insurance claims data
- **Output**: Three-class classification (Low/Medium/High severity) with confidence scores

### Model Characteristics
- **Deterministic**: Same inputs always produce same outputs
- **Explainable**: Feature importance and rule signals provided for every prediction
- **Transparent**: All decision logic is open source and auditable
- **Non-autonomous**: Cannot make binding decisions without human confirmation

---

## Intended Use

### Primary Use Cases
✅ **Educational demonstration** of AI governance principles  
✅ **Proof-of-concept** for governed decision support systems  
✅ **Training tool** for insurance professionals learning about AI assistance  
✅ **Research platform** for studying human-in-the-loop AI systems  
✅ **Compliance review** demonstrations for regulatory stakeholders  

### Target Audience
- AI governance researchers and practitioners
- Insurance industry evaluators and trainers
- Regulatory compliance officers
- Responsible AI designers
- Educational institutions

### Appropriate Contexts
- Demonstration environments with synthetic data
- Educational workshops and training sessions
- Prototype testing for governance frameworks
- Academic research on AI decision support

---

## Non-Intended Use

### ❌ DO NOT USE FOR:
- **Production insurance claims processing** - This is a demonstration system only
- **Real financial decisions** - Not validated for real-world claims
- **Autonomous decision-making** - Human oversight is mandatory
- **Processing real customer data** - Designed for synthetic data only
- **Regulatory compliance** without human review - No regulatory approval obtained
- **Replacing human insurance adjusters** - Designed to assist, not replace
- **High-stakes decisions** without expert review
- **Any application** where model errors could cause harm

### Why These Uses Are Prohibited
1. **No Real-World Validation**: Trained only on synthetic data
2. **No Regulatory Approval**: Not certified for insurance operations
3. **Simplified Rules**: Real insurance claims are far more complex
4. **Demonstration Quality**: Built for education, not production
5. **No Liability Coverage**: No guarantees or warranties provided

---

## Training Data

### Dataset Information
- **Source**: BDR-AI/insurance_decision_boundaries_v1 (Hugging Face Datasets)
- **Type**: Synthetic/demonstration data
- **Purpose**: Educational model training only
- **Size**: [Varies - check model_metadata.json for specific training run]

### Data Characteristics
- **Features**: 4 input features (claim_type, damage_amount, injury_involved, risk_factor)
- **Target**: 3 severity levels (Low, Medium, High)
- **Distribution**: Balanced across severity classes
- **Quality**: Synthetic data generated based on simplified rules

### Data Limitations
⚠ **NOT REAL-WORLD DATA**: This dataset is synthetic and does not represent actual insurance claims  
⚠ **SIMPLIFIED**: Real insurance claims involve hundreds of factors, not just 4  
⚠ **NO BIAS TESTING**: Synthetic data may not reflect real-world demographic patterns  
⚠ **FROZEN BOUNDARIES**: Decision thresholds are fixed and may not match real insurance practices  

---

## Model Performance

### Evaluation Metrics
Performance metrics are available in `evaluation_report.json` after running `evaluate.py`.

**Typical Performance** (on synthetic test data):
- **Accuracy**: ~85-95% (varies by training run)
- **Precision/Recall**: Balanced across severity classes
- **Confidence Calibration**: Assessed via log loss metric
- **Uncertainty Quantification**: Entropy-based uncertainty scores provided

### Performance Interpretation
✓ **High accuracy on synthetic data** - Model learns the simplified rules effectively  
⚠ **Unknown real-world performance** - Not tested on actual insurance claims  
⚠ **Overconfidence risk** - Synthetic data may lead to higher confidence than warranted  

### Confidence Scores
- Model provides confidence scores (0.0-1.0) for each prediction
- Higher confidence does NOT eliminate need for human review
- Low confidence predictions require extra scrutiny
- Uncertainty quantification helps prioritize human attention

---

## Limitations

### Technical Limitations
1. **Simplified Feature Set**: Only 4 input features (real claims need many more)
2. **Synthetic Training Data**: Not validated on real insurance claims
3. **Fixed Decision Boundaries**: Cannot adapt to changing insurance standards
4. **No Contextual Understanding**: Cannot consider claim narratives or special circumstances
5. **Limited Claim Types**: Only handles 4 predefined claim types
6. **No Temporal Factors**: Doesn't account for claim timing or seasonal patterns

### Governance Limitations
1. **No Autonomous Operation**: Must have human oversight for every prediction
2. **No Binding Authority**: All outputs are advisory suggestions only
3. **No Regulatory Approval**: Not certified by insurance regulators
4. **Demonstration Quality**: Not built to production standards
5. **No Safety Guarantees**: Errors and mistakes are expected

### Ethical Limitations
1. **Bias Unknown**: Not tested for fairness across demographic groups
2. **Explainability Gaps**: Feature importance doesn't capture all reasoning
3. **No Accountability**: Model cannot be held responsible for decisions
4. **Limited Transparency**: Internal tree structure can be complex
5. **No Appeal Process**: No mechanism for disputing model suggestions

### Operational Limitations
1. **Single Model**: No ensemble or backup systems
2. **No Online Learning**: Cannot improve from new data without retraining
3. **No A/B Testing**: Not designed for production experimentation
4. **Limited Monitoring**: Basic evaluation only, no production monitoring
5. **No SLA Guarantees**: Performance and availability not guaranteed

---

## Human-in-the-Loop Requirements

### MANDATORY Human Oversight
🔴 **CRITICAL**: This system CANNOT and MUST NOT operate without human supervision.

### Human Responsibilities
1. **Review Every Prediction**: Human must independently evaluate each claim
2. **Exercise Independent Judgment**: Do not blindly accept model suggestions
3. **Confirm or Override**: Human decides whether to accept or reject advisory
4. **Document Rationale**: Human must explain reasoning for final decision
5. **Maintain Audit Trail**: All decisions and rationales must be logged

### Enforcement Mechanisms
- System outputs clearly marked as "ADVISORY ONLY"
- No automatic actions taken based on model predictions
- Human confirmation required before any decision is finalized
- Override capability provided without restrictions
- All human decisions logged with timestamps and rationale

### Human Authority
✅ Human decision-maker has **FULL AUTHORITY** to:
- Accept model suggestions
- Override model suggestions
- Request additional information
- Escalate complex cases
- Apply contextual judgment

The model is a **tool to assist humans**, not a replacement for human expertise.

---

## Explainability and Transparency

### Explainability Features
1. **Feature Importance**: Shows which factors influenced each prediction
2. **Rule Signals**: Human-readable explanation of triggered decision rules
3. **Confidence Scores**: Quantifies model certainty for each prediction
4. **Uncertainty Assessment**: Identifies predictions requiring extra scrutiny
5. **Decision Boundaries**: Fixed thresholds documented and transparent

### Transparency Measures
- All code is open source and reviewable
- Decision logic based on documented rules (decision_spec.yaml)
- Model architecture is classical ML (not black-box deep learning)
- Training process fully documented
- Evaluation metrics publicly available

### Limitations of Explainability
- Feature importance is global, not always case-specific
- Tree ensemble decisions can be complex to trace
- Interactions between features may not be obvious
- Confidence scores can be miscalibrated
- Uncertainty measures are estimates, not guarantees

---

## Ethical Considerations

### Transparency Commitment
✓ **No Hidden Logic**: All decision rules are documented and accessible  
✓ **Explicit Uncertainty**: Model communicates when it's uncertain  
✓ **Human Authority**: Human judgment is preserved and required  
✓ **Open Source**: Code and methodology are publicly reviewable  

### Accountability Framework
✓ **Human Decision-Maker**: Identified in audit trail for every decision  
✓ **Rationale Required**: Human must document reasoning  
✓ **Clear Ownership**: Human owns the decision, not the model  
✓ **Audit Trail**: Complete record of all decisions maintained  

### Safety Measures
✓ **No Autonomous Operation**: System cannot act independently  
✓ **Fail-Safe Defaults**: Errors result in human review, not automatic rejection  
✓ **Explicit Constraints**: System capabilities clearly bounded  
✓ **Override Always Available**: Human can always override suggestions  

### Fairness Considerations
⚠ **Bias Testing Not Performed**: Model not evaluated for demographic fairness  
⚠ **Synthetic Data Only**: May not reflect real-world population distributions  
⚠ **Simplified Features**: May miss important fairness-relevant factors  
⚠ **Human Bias Possible**: Human decision-maker may introduce biases  

**Recommendation**: Any deployment should include fairness auditing and bias testing appropriate to the specific use case.

---

## Technical Specifications

### Environment Requirements
- **Python Version**: 3.11 or higher
- **Dependencies**: See requirements.txt
  - scikit-learn >= 1.3.0
  - xgboost >= 2.0.0
  - pandas >= 2.0.0
  - numpy >= 1.24.0
  - shap >= 0.42.0
  - joblib >= 1.3.0

### Model Artifacts
- **Model File**: model.pkl (joblib serialized XGBoost model)
- **Encoders**: encoders.pkl (label encoders for categorical features)
- **Metadata**: model_metadata.json (training information and metrics)
- **Configuration**: decision_spec.yaml (frozen decision boundaries)

### Input Specification
```python
{
  'claim_type': str,        # "Auto", "Property", "Health", or "Liability"
  'damage_amount': float,   # USD amount (non-negative)
  'injury_involved': bool,  # True or False
  'risk_factor': str        # "low", "medium", or "high"
}
```

### Output Specification
```python
{
  'model_suggestion': str,           # e.g., "High Severity (Advisory)"
  'confidence_score': float,         # 0.0 to 1.0
  'feature_importance': dict,        # Feature contributions
  'rule_signals': list,              # Human-readable explanations
  'uncertainty_assessment': dict,    # Uncertainty level and metrics
  'governance_status': str,          # "ADVISORY ONLY"
  'requires_human_review': bool      # Always True
}
```

### Usage Example
```python
from predict import predict_claim

result = predict_claim(
    claim_type="Auto",
    damage_amount=15000.0,
    injury_involved=True,
    risk_factor="medium"
)

print(f"Advisory Suggestion: {result['model_suggestion']}")
print(f"Confidence: {result['confidence_score']:.2%}")
print(f"Human Review Required: {result['requires_human_review']}")
```

---

## Maintenance and Updates

### Version History
- **v1.0.0** (2026-01-04): Initial release
  - XGBoost classifier trained on synthetic dataset
  - Advisory-only governance framework
  - Human-in-the-loop enforcement
  - Feature importance and uncertainty quantification

### Update Policy
- Model frozen for demonstration purposes
- Retraining requires explicit approval
- Decision boundaries cannot be modified
- Governance constraints are immutable

### Contact and Support
This is a demonstration model for the BDR Agent Factory governance framework.  
For questions about governance principles or implementation:
- Review the decision_spec.yaml file
- Consult the QODER_EXECUTION_BRIEF.md
- Refer to project documentation

---

## Governance Compliance Summary

### ✅ Compliance Verified
- [x] Classical ML only (no LLMs, no neural networks)
- [x] Advisory-only outputs (no autonomous decisions)
- [x] Human review required for all predictions
- [x] Only allowed features used (4 features as specified)
- [x] Decision boundaries documented and frozen
- [x] Explainability artifacts generated
- [x] Uncertainty quantification provided
- [x] Audit trail support implemented
- [x] Override capability enabled
- [x] Limitations clearly documented

### Governance Framework
This model operates under the **BDR Agent Factory** governance framework:
- **No autonomous actions**: System cannot take actions without human approval
- **Transparency**: All logic is explainable and auditable
- **Human authority**: Human has final decision-making power
- **Accountability**: Human decision-maker is logged and responsible
- **Safety**: System designed with fail-safe constraints

---

## License and Disclaimer

### License
This model and associated code are provided for educational and research purposes.  
Suggested License: Apache 2.0 or MIT (specify as appropriate for your use case)

### Disclaimer
**THIS MODEL IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.**

⚠ **IMPORTANT DISCLAIMERS**:
1. **No Production Use**: This model is for demonstration and education only
2. **No Accuracy Guarantees**: Performance on real-world data is unknown
3. **No Regulatory Approval**: Not certified for insurance operations
4. **No Liability Coverage**: Use at your own risk
5. **Human Oversight Required**: Must not operate autonomously
6. **Synthetic Data Only**: Not validated on real insurance claims
7. **Educational Purpose**: Designed for learning, not production deployment

### Responsible Use
Users of this model are responsible for:
- Ensuring appropriate human oversight
- Complying with applicable regulations
- Conducting their own validation and testing
- Not deploying in high-stakes scenarios without proper safeguards
- Maintaining audit trails and accountability

---

## Conclusion

This model demonstrates how classical machine learning can be deployed under strict governance constraints to provide **advisory decision support** while preserving human authority and accountability.

**Key Takeaways**:
✓ Advisory suggestions, not autonomous decisions  
✓ Human-in-the-loop is mandatory  
✓ Transparency and explainability built-in  
✓ Clear documentation of limitations  
✓ Designed for education, not production  

**Remember**: This is a tool to **assist humans**, not replace them. The final decision authority always rests with qualified human professionals.

---

**Model Card Version**: 1.0.0  
**Last Reviewed**: 2026-01-04  
**Next Review**: Required before any production consideration (not currently approved)
