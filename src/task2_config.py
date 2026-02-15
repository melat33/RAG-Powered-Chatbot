"""Configuration for Task 2"""
from pathlib import Path

# Get the correct path to your data
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'filtered_complaints.csv'

# Verify path exists
if not DATA_PATH.exists():
    print(f"⚠️ Warning: {DATA_PATH} not found!")
    # Try alternative locations
    alt_paths = [
        BASE_DIR / 'data' / 'filtered_complaints.csv',
        BASE_DIR / 'filtered_complaints.csv',
        Path('../data/processed/filtered_complaints.csv')
    ]
    for alt in alt_paths:
        if alt.exists():
            DATA_PATH = alt
            print(f"✅ Found at: {DATA_PATH}")
            break

# Parameters
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
BATCH_SIZE = 1000
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

# Create directories
for d in ['data/chunks', 'embeddings', 'vector_store', 'reports']:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

# Paths for outputs
CHUNKS_PATH = BASE_DIR / 'data/chunks/all_chunks.parquet'
EMBEDDINGS_PATH = BASE_DIR / 'embeddings/all_embeddings.npy'
INDEX_PATH = BASE_DIR / 'vector_store/faiss_index.idx'
METADATA_PATH = BASE_DIR / 'vector_store/metadata.pkl'

print(f"✅ Config loaded - Data path: {DATA_PATH}")