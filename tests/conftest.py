"""Pytest configuration and fixtures"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Create dummy data for testing if needed
import pytest
import pandas as pd
import os

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame({
        'Complaint ID': [1, 2, 3, 4, 5],
        'Consumer complaint narrative': [
            'Credit card fraud complaint',
            'Mortgage application delayed',
            'Unauthorized bank transfer',
            'Hidden fees on loan',
            'Poor customer service'
        ],
        'Product': ['Credit Card', 'Mortgage', 'Money Transfer', 'Personal Loan', 'Credit Card'],
        'Product_Category': ['Credit Card', 'Mortgage', 'Money Transfer', 'Personal Loan', 'Credit Card'],
        'Issue': ['Fraud', 'Delay', 'Unauthorized', 'Fees', 'Service']
    })

@pytest.fixture
def sample_chunks():
    """Create sample chunks for testing"""
    return pd.DataFrame({
        'chunk_id': range(10),
        'complaint_id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
        'product': ['Credit Card'] * 10,
        'chunk_text': ['Sample chunk text'] * 10,
        'chunk_length': [50] * 10
    })