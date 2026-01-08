---
title: Insurance Datasets Synthetic
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 📈 Insurance Synthetic Datasets

## Overview

This repository provides **synthetic insurance datasets** for testing, development, and educational purposes. All data is completely synthetic and does not contain any real insurance policies, claims, or personal information.

## 📊 Datasets Included

### 1. Claims Data (`data/claims_data.csv`)
Synthetic insurance claims covering auto and home insurance types.

**Columns:**
- `claim_id`: Unique claim identifier
- `policy_id`: Associated policy ID
- `claim_date`: Date claim was filed
- `claim_type`: Type of claim (Auto Collision, Home Fire, etc.)
- `claim_amount`: Claimed amount in USD
- `claim_status`: Current status (Settled, In Progress)
- `settlement_amount`: Final settlement amount
- `days_to_settle`: Number of days to settle
- `claimant_age`: Age of claimant
- `incident_severity`: Severity level (Minor, Moderate, Severe)

**Sample Size:** 25 records

### 2. Policies Data (`data/policies_data.csv`)
Synthetic insurance policies for auto and home coverage.

**Columns:**
- `policy_id`: Unique policy identifier
- `policy_type`: Type of policy (Auto, Home)
- `policy_holder_name`: Synthetic policyholder name
- `policy_start_date`: Policy start date
- `policy_end_date`: Policy end date
- `premium_amount`: Annual premium in USD
- `coverage_amount`: Total coverage limit
- `deductible`: Deductible amount
- `policy_status`: Current status
- `risk_score`: Risk assessment score (0-1)

**Sample Size:** 25 records

### 3. Fraud Indicators (`data/fraud_indicators.csv`)
Synthetic fraud detection indicators for claims.

**Columns:**
- `indicator_id`: Unique indicator ID
- `claim_id`: Associated claim ID
- `indicator_type`: Type of fraud indicator
- `risk_level`: Risk level (Low, Medium, High)
- `indicator_description`: Description of the indicator
- `detection_date`: Date indicator was detected
- `verified_status`: Verification status

**Sample Size:** 15 records

## 🚀 Usage

### Interactive Explorer
Use the Gradio app to explore the datasets interactively:
- View dataset statistics
- Filter claims by type and status
- Search policies by ID
- Analyze fraud indicators

### Download & Use
Download the CSV files from the `data/` directory for use in your projects:

```python
import pandas as pd

# Load claims data
claims_df = pd.read_csv('data/claims_data.csv')

# Load policies data
policies_df = pd.read_csv('data/policies_data.csv')

# Load fraud indicators
fraud_df = pd.read_csv('data/fraud_indicators.csv')
```

## ⚠️ Disclaimer

This project models generic insurance concepts common in GCC markets. All datasets are synthetic and made-up for demonstration and research purposes. No proprietary pricing, underwriting rules, policy wording, or confidential logic was used. Outputs are illustrative only and require human review. Not to be used for any pricing, reserving, claim approval, or policy issuance.

## Human-In-The-Loop

No AI component here issues approvals, denials, or financial outcomes. All outputs require human verification and decision-making.

## ⚠️ Compliance & Safety

- ✅ **100% Synthetic Data**: All data is artificially generated
- ✅ **No Real Information**: No actual insurance policies or personal data
- ✅ **No Real Insurers**: No real insurance company names used
- ✅ **No Actuarial Formulas**: No proprietary pricing or risk models
- ✅ **Advisory Only**: All outputs are for demonstration purposes
- ✅ **No KYC Fields**: No sensitive personal identification data

## 🎯 Use Cases

- **AI/ML Model Training**: Train fraud detection or claims prediction models
- **System Testing**: Test insurance claims processing systems
- **Educational Projects**: Learn about insurance data structures
- **Prototype Development**: Build insurance tech prototypes
- **Data Analysis Practice**: Practice data analysis on realistic datasets

## 📝 License

MIT License - Free to use for any purpose

## 🔗 Related Repositories

Check out other insurance AI tools:
- fraud-triage-sandbox
- ifrs-claim-accrual-estimator
- doc-rag-compliance-assistant

## Technical Details

- **Format**: CSV files
- **License**: MIT
- **Data Source**: Fully synthetic, programmatically generated
- **Size**: Small sample datasets (15-25 records each)
- **Purpose**: Educational and testing only

---

**Built by Qoder for Vercept**
