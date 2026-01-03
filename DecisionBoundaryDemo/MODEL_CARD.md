# Model Card: Insurance Claims Decision Model

## Model Description

This is a **rule-based, deterministic decision model** for insurance claims processing. It is NOT a machine learning model and does NOT use neural networks, statistical learning, or trained parameters.

**Architecture**: Deterministic rule engine with governance constraints  
**Type**: Advisory system (non-autonomous)  
**Version**: 1.0.0  
**Last Updated**: January 2026

## Intended Use

### Primary Use Case
Demonstration of AI governance principles in insurance claims decision-making, specifically:
- Human-in-the-loop enforcement
- Decision boundary transparency
- Audit trail generation
- Capability governance
- Explainable decision logic

### Target Audience
- AI governance researchers
- Insurance technology evaluators
- Regulatory compliance teams
- Technical reviewers assessing governed AI systems

### Appropriate Contexts
- Educational demonstrations
- Governance framework evaluation
- Technical architecture review
- Proof-of-concept for regulated AI

## Non-Intended Use

**This system is NOT intended for:**

- Production insurance claims processing
- Real financial decisions
- Autonomous decision-making without human oversight
- Replacement of human claims adjusters
- Legal or binding determinations
- Processing real customer data
- High-stakes or safety-critical applications

**Why Not Production-Ready:**
- Uses synthetic data only
- Simplified decision rules
- No regulatory approval
- No real-world validation
- Demonstration-grade only

## Model Architecture

### Decision Logic
```
Input -> Dataset Validation -> Capability Governance -> Rule Engine -> Human Confirmation -> Decision
```

### Components
1. **Dataset Loader**: Validates input against known decision boundaries
2. **Capability Governance**: Enforces constraints from AI_CAPABILITY_DICTIONARY.yaml
3. **Advisory Model**: Generates non-binding suggestions with confidence scores
4. **Decision Engine**: Single decision function (make_decision) - the ONLY path to decisions
5. **Human-in-the-Loop**: Mandatory human confirmation with rationale
6. **Audit Trail**: Immutable logging of all decisions

### Deterministic Behavior
- Same inputs -> Same outputs (100% reproducible)
- No randomness
- No learning or adaptation
- No model training

## Training Data

**N/A** - This is not a trained model.

The system uses a **synthetic dataset** (`insurance_decision_boundaries_v1`) containing:
- 50 pre-defined decision scenarios
- Synthetic claim data (not real customers)
- Known decision boundaries for testing

See the dataset card for full details on data limitations and biases.

## Evaluation

**N/A** - Traditional ML evaluation does not apply.

### Validation Approach
- Deterministic rule verification
- Governance constraint testing
- Human-in-the-loop enforcement checks
- Audit trail completeness validation

## Limitations

### Technical Limitations
1. **Simplified Rules**: Real insurance claims require far more complex logic
2. **Limited Scenarios**: Only 50 decision boundaries covered
3. **No Learning**: Cannot adapt to new patterns or edge cases
4. **Synthetic Data Only**: Not validated on real claims
5. **No Integration**: Standalone demo, not integrated with real systems

### Governance Limitations
1. **Demo-Grade Only**: Not hardened for production security
2. **No Regulatory Approval**: Not certified for real insurance use
3. **No SLA**: No performance or availability guarantees
4. **Limited Audit**: Audit trail is local only, not enterprise-grade

### Bias and Fairness
- Synthetic data may not reflect real-world demographic distributions
- Decision rules are simplified and may not capture fairness considerations
- No fairness testing or bias mitigation has been performed
- Not suitable for decisions affecting real people

## Human-in-the-Loop Requirement

**MANDATORY**: This system enforces human-in-the-loop for ALL decisions.

### Enforcement Mechanism
- No decision can be finalized without `human_confirms=True`
- Human must provide `human_override_reason` (non-empty, non-whitespace)
- System blocks autonomous operation
- All human confirmations are logged in audit trail

### Human Role
- Review model suggestion
- Assess confidence and explanation
- Provide independent judgment
- Document rationale for decision

## Ethical Considerations

### Transparency
- All decision logic is open source
- Explanations provided for every decision
- Governance constraints are explicit
- Audit trail is complete and accessible

### Accountability
- Human decision-maker is identified in audit trail
- Rationale is required and logged
- Decision ownership is clear

### Safety
- System cannot operate autonomously
- Fail-safe defaults (reject on error)
- Explicit capability constraints

## Technical Specifications

**Language**: Python 3.11+  
**Framework**: Gradio 6.2.0  
**Dependencies**: See requirements.txt  
**License**: Apache 2.0  
**Repository**: https://huggingface.co/spaces/BDR-AI/DecisionBoundaryDemo

## Contact

**Maintainer**: BDR-AI  
**Purpose**: AI Governance Demonstration  
**Feedback**: Via Hugging Face Space discussions

## Version History

- **v1.0.0** (January 2026): Initial release with 7-layer governance enforcement

## Citation

If referencing this governance demonstration:

```
BDR-AI (2026). Insurance Claims Decision Boundary Demo: 
A Governed AI System with Human-in-the-Loop Enforcement.
Hugging Face Spaces. https://huggingface.co/spaces/BDR-AI/DecisionBoundaryDemo
```

---

**Disclaimer**: This is a demonstration system for AI governance education and technical evaluation. It is not approved, certified, or intended for production use in insurance claims processing or any real-world decision-making.