"""Configuration settings for the project"""
from pathlib import Path
from types import SimpleNamespace

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'complaints.csv'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed'

# Product mapping
PRODUCT_MAPPING = {
    'Credit card': 'Credit Card',
    'Credit reporting': 'Credit Reporting',
    'Debt collection': 'Debt Collection',
    'Mortgage': 'Mortgage',
    'Student loan': 'Student Loan',
    'Vehicle loan': 'Vehicle Loan',
    'Payday loan': 'Payday Loan',
    'Personal loan': 'Personal Loan',
    'Bank account': 'Savings Account',
    'Money transfers': 'Money Transfer'
}

TARGET_PRODUCTS = ['Credit Card', 'Mortgage', 'Student Loan', 'Vehicle Loan', 'Payday Loan']

# Data types for memory optimization
DTYPE_STRATEGY = {
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

CHUNK_SIZE = 50000
MIN_WORDS = 5

# Create cfg object for backward compatibility
cfg = SimpleNamespace(
    PROJECT_ROOT=PROJECT_ROOT,
    RAW_DATA_PATH=RAW_DATA_PATH,
    PROCESSED_DATA_PATH=PROCESSED_DATA_PATH,
    PRODUCT_MAPPING=PRODUCT_MAPPING,
    TARGET_PRODUCTS=TARGET_PRODUCTS,
    DTYPE_STRATEGY=DTYPE_STRATEGY,
    CHUNK_SIZE=CHUNK_SIZE,
    MIN_WORDS=MIN_WORDS
)