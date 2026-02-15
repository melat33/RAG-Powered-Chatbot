<<<<<<< HEAD
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
=======
"""
Configuration settings for the RAG system
"""

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Retrieval settings
RETRIEVAL_K = 5
MIN_CONFIDENCE_SCORE = 30

# Vector store settings
VECTOR_STORE_DIR = "vector_store"
COLLECTION_NAME = "complaint_embeddings"

# Business intelligence settings
BUSINESS_CONTEXTS = {
    "urgent": ["urgent", "critical", "emergency", "immediate"],
    "trending": ["trend", "pattern", "increase", "decrease", "over time"],
    "comparative": ["compare", "vs", "versus", "difference", "better", "worse"],
    "root_cause": ["why", "reason", "cause", "root", "source"],
    "volume": ["many", "often", "frequent", "common", "typical"]
}

# Product categories mapping
PRODUCT_CATEGORIES = {
    "credit card": ["Credit card", "credit card", "Credit Card", "Credit-card"],
    "personal loan": ["Personal loan", "personal loan", "Personal Loan", "Personal-loan"],
    "savings account": ["Savings account", "savings account", "Savings Account", "Savings-account"],
    "money transfers": ["Money transfers", "money transfers", "Money Transfers", "Money-transfers"],
    "mortgage": ["Mortgage", "mortgage", "Home loan"],
    "checking account": ["Checking account", "checking account", "Checking Account", "Checking-account"]
}
>>>>>>> c0238a21703cf902bf6bbdae2af72d12eedc097a
