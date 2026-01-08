"""
Data Loader Utility for Insurance Synthetic Datasets

This module provides helper functions to load and process the synthetic insurance datasets.
"""

import pandas as pd
import os
from typing import Optional, List


class InsuranceDataLoader:
    """Utility class for loading and processing insurance datasets."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Directory containing the CSV files
        """
        self.data_dir = data_dir
        self.claims_file = os.path.join(data_dir, "claims_data.csv")
        self.policies_file = os.path.join(data_dir, "policies_data.csv")
        self.fraud_file = os.path.join(data_dir, "fraud_indicators.csv")
    
    def load_claims(self, claim_types: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Load claims data with optional filtering.
        
        Args:
            claim_types: Optional list of claim types to filter
            
        Returns:
            DataFrame containing claims data
        """
        df = pd.read_csv(self.claims_file)
        df['claim_date'] = pd.to_datetime(df['claim_date'])
        
        if claim_types:
            df = df[df['claim_type'].isin(claim_types)]
        
        return df
    
    def load_policies(self, policy_types: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Load policies data with optional filtering.
        
        Args:
            policy_types: Optional list of policy types to filter
            
        Returns:
            DataFrame containing policies data
        """
        df = pd.read_csv(self.policies_file)
        df['policy_start_date'] = pd.to_datetime(df['policy_start_date'])
        df['policy_end_date'] = pd.to_datetime(df['policy_end_date'])
        
        if policy_types:
            df = df[df['policy_type'].isin(policy_types)]
        
        return df
    
    def load_fraud_indicators(self, risk_levels: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Load fraud indicators with optional filtering.
        
        Args:
            risk_levels: Optional list of risk levels to filter
            
        Returns:
            DataFrame containing fraud indicators
        """
        df = pd.read_csv(self.fraud_file)
        df['detection_date'] = pd.to_datetime(df['detection_date'])
        
        if risk_levels:
            df = df[df['risk_level'].isin(risk_levels)]
        
        return df
    
    def get_claims_summary(self) -> dict:
        """
        Get summary statistics for claims data.
        
        Returns:
            Dictionary containing summary statistics
        """
        df = self.load_claims()
        
        return {
            'total_claims': len(df),
            'total_amount': df['claim_amount'].sum(),
            'avg_amount': df['claim_amount'].mean(),
            'settled_claims': (df['claim_status'] == 'Settled').sum(),
            'pending_claims': (df['claim_status'] == 'In Progress').sum(),
            'avg_settlement_days': df[df['days_to_settle'] > 0]['days_to_settle'].mean()
        }
    
    def get_policy_summary(self) -> dict:
        """
        Get summary statistics for policies data.
        
        Returns:
            Dictionary containing summary statistics
        """
        df = self.load_policies()
        
        return {
            'total_policies': len(df),
            'total_premium': df['premium_amount'].sum(),
            'avg_premium': df['premium_amount'].mean(),
            'total_coverage': df['coverage_amount'].sum(),
            'avg_risk_score': df['risk_score'].mean(),
            'auto_policies': (df['policy_type'] == 'Auto').sum(),
            'home_policies': (df['policy_type'] == 'Home').sum()
        }
    
    def merge_claims_with_policies(self) -> pd.DataFrame:
        """
        Merge claims data with policies data.
        
        Returns:
            DataFrame with merged claims and policies
        """
        claims = self.load_claims()
        policies = self.load_policies()
        
        merged = claims.merge(policies, on='policy_id', how='left')
        return merged
    
    def get_high_risk_claims(self, threshold: float = 0.4) -> pd.DataFrame:
        """
        Get claims associated with high-risk policies.
        
        Args:
            threshold: Risk score threshold (default 0.4)
            
        Returns:
            DataFrame containing high-risk claims
        """
        merged = self.merge_claims_with_policies()
        high_risk = merged[merged['risk_score'] >= threshold]
        return high_risk


# Example usage
if __name__ == "__main__":
    loader = InsuranceDataLoader()
    
    # Load all claims
    claims = loader.load_claims()
    print(f"Loaded {len(claims)} claims")
    
    # Get summary
    summary = loader.get_claims_summary()
    print(f"\nClaims Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Load high-risk claims
    high_risk = loader.get_high_risk_claims()
    print(f"\nHigh-risk claims: {len(high_risk)}")
