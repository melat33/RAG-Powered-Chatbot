"""
Configuration for RAG Complaint Chatbot
"""
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store" / "chroma_db"
EMBEDDINGS_PATH = DATA_DIR / "complaint_embeddings.parquet"

# Model configurations - CHANGED to smaller model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "distilgpt2"  # Very small, CPU-friendly model

# RAG parameters
RETRIEVAL_K = 5
SIMILARITY_THRESHOLD = 0.7

# Product categories
PRODUCT_CATEGORIES = [
    "Credit Card",
    "Personal Loan", 
    "Savings account",
    "Money transfers"
]

def print_config():
    """Print current configuration"""
    print("📋 RAG Configuration:")
    print(f"   Project Root: {PROJECT_ROOT}")
    print(f"   Vector Store: {VECTOR_STORE_DIR}")
    print(f"   Embedding Model: {EMBEDDING_MODEL}")
    print(f"   LLM Model: {LLM_MODEL} (CPU-friendly)")
    print(f"   Retrieval K: {RETRIEVAL_K}")
    print("✓ Configuration loaded")