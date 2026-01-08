import gradio as gr
import pandas as pd
import os

# Load datasets
data_dir = "data"

def load_claims_data():
    df = pd.read_csv(os.path.join(data_dir, "claims_data.csv"))
    return df

def load_policies_data():
    df = pd.read_csv(os.path.join(data_dir, "policies_data.csv"))
    return df

def load_fraud_indicators():
    df = pd.read_csv(os.path.join(data_dir, "fraud_indicators.csv"))
    return df

def get_dataset_stats(dataset_name):
    if dataset_name == "Claims Data":
        df = load_claims_data()
        stats = f"""
        **Dataset: Claims Data**
        
        - Total Records: {len(df)}
        - Columns: {', '.join(df.columns.tolist())}
        - Claim Types: {df['claim_type'].nunique()}
        - Total Claim Amount: ${df['claim_amount'].sum():,.2f}
        - Average Claim Amount: ${df['claim_amount'].mean():,.2f}
        - Settlement Rate: {(df['claim_status'] == 'Settled').sum() / len(df) * 100:.1f}%
        """
        return stats, df
    elif dataset_name == "Policies Data":
        df = load_policies_data()
        stats = f"""
        **Dataset: Policies Data**
        
        - Total Records: {len(df)}
        - Columns: {', '.join(df.columns.tolist())}
        - Policy Types: {df['policy_type'].nunique()}
        - Total Premium Revenue: ${df['premium_amount'].sum():,.2f}
        - Average Premium: ${df['premium_amount'].mean():,.2f}
        - Total Coverage: ${df['coverage_amount'].sum():,.2f}
        """
        return stats, df
    elif dataset_name == "Fraud Indicators":
        df = load_fraud_indicators()
        stats = f"""
        **Dataset: Fraud Indicators**
        
        - Total Records: {len(df)}
        - Columns: {', '.join(df.columns.tolist())}
        - High Risk Indicators: {(df['risk_level'] == 'High').sum()}
        - Medium Risk Indicators: {(df['risk_level'] == 'Medium').sum()}
        - Low Risk Indicators: {(df['risk_level'] == 'Low').sum()}
        - Flagged Cases: {(df['verified_status'] == 'Flagged').sum()}
        """
        return stats, df
    else:
        return "Please select a dataset", pd.DataFrame()

def filter_claims(claim_type, status):
    df = load_claims_data()
    if claim_type != "All":
        df = df[df['claim_type'] == claim_type]
    if status != "All":
        df = df[df['claim_status'] == status]
    return df

def search_policy(policy_id):
    df = load_policies_data()
    if policy_id:
        result = df[df['policy_id'].str.contains(policy_id, case=False, na=False)]
        if len(result) > 0:
            return result
        else:
            return pd.DataFrame({"Message": ["No policy found with that ID"]})
    return df

# Create Gradio interface
with gr.Blocks(title="Insurance Datasets - Synthetic Data Explorer") as demo:
    gr.Markdown("""
    # 🏥 Insurance Synthetic Datasets Explorer
    
    **Explore synthetic insurance data for testing and development purposes.**
    
    ⚠️ **DISCLAIMER**: All data is synthetic and for demonstration purposes only. 
    No real insurance policies, claims, or personal information is included.
    """)
    
    with gr.Tab("📊 Dataset Overview"):
        gr.Markdown("### Select a dataset to view statistics and preview")
        dataset_selector = gr.Radio(
            choices=["Claims Data", "Policies Data", "Fraud Indicators"],
            label="Choose Dataset",
            value="Claims Data"
        )
        stats_output = gr.Markdown()
        data_output = gr.Dataframe()
        
        dataset_selector.change(
            fn=get_dataset_stats,
            inputs=[dataset_selector],
            outputs=[stats_output, data_output]
        )
        
        # Load initial data
        demo.load(
            fn=get_dataset_stats,
            inputs=[dataset_selector],
            outputs=[stats_output, data_output]
        )
    
    with gr.Tab("🔍 Claims Explorer"):
        gr.Markdown("### Filter and explore claims data")
        with gr.Row():
            claim_type_filter = gr.Dropdown(
                choices=["All", "Auto Collision", "Auto Theft", "Auto Vandalism", 
                        "Home Fire", "Home Water Damage", "Home Burglary", "Home Storm Damage"],
                label="Claim Type",
                value="All"
            )
            status_filter = gr.Dropdown(
                choices=["All", "Settled", "In Progress"],
                label="Claim Status",
                value="All"
            )
        filter_btn = gr.Button("Apply Filters")
        claims_output = gr.Dataframe()
        
        filter_btn.click(
            fn=filter_claims,
            inputs=[claim_type_filter, status_filter],
            outputs=[claims_output]
        )
    
    with gr.Tab("📋 Policy Lookup"):
        gr.Markdown("### Search for policies by ID")
        policy_search = gr.Textbox(label="Policy ID (e.g., POL-A-1001)", placeholder="Enter policy ID...")
        search_btn = gr.Button("Search")
        policy_output = gr.Dataframe()
        
        search_btn.click(
            fn=search_policy,
            inputs=[policy_search],
            outputs=[policy_output]
        )
    
    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        ## About This Dataset
        
        This repository contains **synthetic insurance datasets** designed for:
        - Testing insurance AI/ML models
        - Developing claims processing systems
        - Training fraud detection algorithms
        - Educational purposes
        
        ### Datasets Included:
        
        1. **Claims Data** (`claims_data.csv`)
           - Synthetic insurance claims with various types (Auto, Home)
           - Includes claim amounts, settlement info, and severity levels
        
        2. **Policies Data** (`policies_data.csv`)
           - Synthetic insurance policies
           - Contains premium amounts, coverage limits, and risk scores
        
        3. **Fraud Indicators** (`fraud_indicators.csv`)
           - Synthetic fraud detection flags
           - Risk levels and verification statuses
        
        ### Compliance & Safety:
        - ✅ All data is 100% synthetic
        - ✅ No real insurer names or policies
        - ✅ No actual personal information
        - ✅ No actuarial formulas or pricing models
        - ✅ Advisory use only
        
        ### Usage:
        Download the CSV files from the `data/` directory and use them in your projects.
        """)

if __name__ == "__main__":
    demo.launch()
