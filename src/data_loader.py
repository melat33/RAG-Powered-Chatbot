"""Data loading utilities for large datasets"""
import pandas as pd
import numpy as np
import os
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

def load_complaints_data(filepath: str, sample_size: Optional[int] = None) -> pd.DataFrame:
    """
    Load complaints data efficiently with memory optimization
    
    Args:
        filepath: Path to CSV file
        sample_size: Optional sample size for quick loading
        
    Returns:
        DataFrame with complaints data
    """
    logger.info(f"Loading data from {filepath}")
    
    # Optimized data types for memory efficiency
    dtype_strategy = {
        'Complaint ID': 'str',
        'Date received': 'str',
        'Product': 'category',
        'Sub-product': 'category',
        'Issue': 'category',
        'Sub-issue': 'category',
        'Company': 'category',
        'State': 'category',
        'ZIP code': 'str',
        'Tags': 'category',
        'Consumer consent provided?': 'category',
        'Submitted via': 'category',
        'Company response to consumer': 'category',
        'Timely response?': 'category',
        'Consumer disputed?': 'category',
        'Consumer complaint narrative': 'object'
    }
    
    try:
        if sample_size:
            # Load sample for quick analysis
            df = pd.read_csv(
                filepath,
                dtype=dtype_strategy,
                parse_dates=['Date received'],
                infer_datetime_format=True,
                nrows=sample_size
            )
            logger.info(f"Loaded sample of {len(df):,} records")
        else:
            # Load full dataset in chunks
            chunks = []
            chunk_size = 50000
            
            for i, chunk in enumerate(pd.read_csv(
                filepath,
                dtype=dtype_strategy,
                parse_dates=['Date received'],
                infer_datetime_format=True,
                chunksize=chunk_size
            )):
                chunks.append(chunk)
                if (i + 1) % 10 == 0:
                    logger.info(f"Loaded chunk {i+1}: {(i+1)*chunk_size:,} records")
            
            df = pd.concat(chunks, ignore_index=True)
            logger.info(f"Loaded full dataset: {len(df):,} records")
        
        # Add product mapping for business focus
        df = _map_products(df)
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def _map_products(df: pd.DataFrame) -> pd.DataFrame:
    """Map raw product names to business categories"""
    product_mapping = {
        'Credit card': 'Credit Card',
        'Credit card or prepaid card': 'Credit Card',
        'Prepaid card': 'Credit Card',
        'Payday loan, title loan, or personal loan': 'Personal Loan',
        'Consumer Loan': 'Personal Loan',
        'Vehicle loan or lease': 'Personal Loan',
        'Bank account or service': 'Savings Account',
        'Checking or savings account': 'Savings Account',
        'Savings account': 'Savings Account',
        'Money transfer, virtual currency, or money service': 'Money Transfer',
        'Virtual currency': 'Money Transfer',
        'Mortgage': 'Mortgage',
        'Student loan': 'Student Loan',
        'Debt collection': 'Debt Collection',
        'Credit reporting, credit repair services, or other personal consumer reports': 'Credit Reporting'
    }
    
    df['Product_Category'] = df['Product'].map(product_mapping).fillna('Other')
    return df

def create_business_df(df: pd.DataFrame) -> pd.DataFrame:
    """Filter to business-relevant products"""
    business_products = ['Credit Card', 'Personal Loan', 'Savings Account', 'Money Transfer']
    business_df = df[df['Product_Category'].isin(business_products)].copy()
    logger.info(f"Created business dataset: {len(business_df):,} records")
    return business_df

def create_viable_df(df: pd.DataFrame) -> pd.DataFrame:
    """Filter to complaints with narratives"""
    viable_df = df[df['Consumer complaint narrative'].notna()].copy()
    viable_df['Narrative_Length_Chars'] = viable_df['Consumer complaint narrative'].str.len()
    viable_df['Narrative_Length_Words'] = viable_df['Consumer complaint narrative'].str.split().str.len()
    
    logger.info(f"Created viable dataset: {len(viable_df):,} records with narratives")
    return viable_df