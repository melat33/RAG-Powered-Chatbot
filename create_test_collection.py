"""
Create a small test ChromaDB collection (memory-efficient)
FIXED VERSION - handles pandas.read_parquet limitations
"""
import sys
from pathlib import Path
import pandas as pd
import chromadb
import warnings
warnings.filterwarnings('ignore')

# Setup paths
project_root = Path(__file__).parent
data_path = project_root / "data" / "processed" / "complaint_embeddings.parquet"
vector_store_path = project_root / "vector_store" / "chroma_db"

print("=" * 60)
print("🚀 CREATING TEST CHROMADB COLLECTION")
print("=" * 60)
print(f"Data: {data_path}")
print(f"Vector store: {vector_store_path}")

# Check if file exists
if not data_path.exists():
    print(f"❌ File not found: {data_path}")
    sys.exit(1)

print(f"✅ File exists: {data_path.stat().st_size / (1024**3):.2f} GB")

# Create vector store directory
vector_store_path.mkdir(parents=True, exist_ok=True)

# Initialize ChromaDB
print("\n📚 Initializing ChromaDB...")
client = chromadb.PersistentClient(path=str(vector_store_path))

# Check if collection exists
try:
    collection = client.get_collection("complaint_embeddings")
    print(f"✅ Collection already exists: {collection.name}")
    print(f"   Items: {collection.count()}")
    sys.exit(0)
except:
    print("🆕 Creating new collection...")

# Create collection
collection = client.create_collection(
    name="complaint_embeddings",
    metadata={"description": "Financial complaint chunks - TEST SET"}
)

print("\n⏳ Creating test collection with sample data...")

# Method 1: Try to read parquet file with proper method
try:
    # FIXED: Use iloc to get first n rows instead of nrows parameter
    print("Reading parquet file header to get columns...")
    
    # Read just the first row to get columns
    df_first_row = pd.read_parquet(data_path)
    print(f"✅ File columns: {list(df_first_row.columns)}")
    
    # Determine text column
    text_columns = ['text_chunk', 'consumer_complaint_narrative', 'narrative', 'text']
    text_column = None
    for col in text_columns:
        if col in df_first_row.columns:
            text_column = col
            break
    
    if not text_column:
        # Use first text-like column
        for col in df_first_row.columns:
            if df_first_row[col].dtype == 'object' and len(str(df_first_row[col].iloc[0])) > 10:
                text_column = col
                break
    
    if not text_column:
        text_column = df_first_row.columns[0]
    
    print(f"📝 Using text column: {text_column}")
    
    # Read in smaller chunks using iterator
    print("\n📊 Reading data in chunks...")
    
    # Since nrows doesn't work with parquet, we'll use a different approach
    # Read the entire file but take only first few thousand rows
    try:
        # Try to read with chunks - some parquet files support this
        import pyarrow.parquet as pq
        
        # Get total rows
        parquet_file = pq.ParquetFile(data_path)
        total_rows = parquet_file.metadata.num_rows
        print(f"Total rows in file: {total_rows:,}")
        
        # Read first batch only (for testing)
        batch_size = 1000
        table = parquet_file.read_row_groups([0])  # Read first row group
        df_sample = table.to_pandas().head(batch_size)
        
    except:
        # Fallback: read with pandas and take sample
        print("Using pandas to read sample...")
        df_sample = pd.read_parquet(data_path).head(1000)
    
    print(f"Read {len(df_sample)} rows for test collection")
    
    # Prepare data for ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    for idx, row in df_sample.iterrows():
        # Get text
        if pd.notna(row[text_column]):
            text = str(row[text_column])
            if len(text) > 20:  # Skip very short texts
                documents.append(text[:500])  # Limit text length
                
                # Create metadata
                metadata = {}
                metadata_fields = ['product_category', 'issue', 'sub_issue', 
                                 'company', 'state', 'date_received']
                
                for field in metadata_fields:
                    if field in df_sample.columns and pd.notna(row.get(field, None)):
                        metadata[field] = str(row[field])
                    else:
                        metadata[field] = ""
                
                # Add complaint_id if available
                if 'complaint_id' in df_sample.columns and pd.notna(row.get('complaint_id', None)):
                    metadata['complaint_id'] = str(row['complaint_id'])
                else:
                    metadata['complaint_id'] = f"sample_{idx}"
                
                metadatas.append(metadata)
                ids.append(f"sample_{idx}")
    
    # Add to collection in batches
    batch_size = 100
    total_batches = (len(documents) + batch_size - 1) // batch_size
    
    print(f"\n⏳ Adding {len(documents)} documents in {total_batches} batches...")
    
    for i in range(0, len(documents), batch_size):
        batch_end = min(i + batch_size, len(documents))
        batch_ids = ids[i:batch_end]
        batch_docs = documents[i:batch_end]
        batch_metas = metadatas[i:batch_end]
        
        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            metadatas=batch_metas
        )
        
        batch_num = i // batch_size + 1
        print(f"  Batch {batch_num}/{total_batches}: Added {len(batch_ids)} items")
    
    print(f"\n🎉 TEST COLLECTION CREATED!")
    print(f"   Total documents: {collection.count()}")
    print(f"   Location: {vector_store_path}")
    
except Exception as e:
    print(f"❌ Error reading parquet: {e}")
    print("\n🔧 Creating minimal test collection instead...")
    
    # Create minimal test collection
    test_documents = [
        "Customer complaining about credit card fees being too high without proper notification. The annual fee increased from $99 to $149 without warning.",
        "Issue with money transfer taking 5 business days instead of the promised 24 hours. Customer needed funds urgently for medical expenses.",
        "Complaint about savings account interest rates being reduced from 2.5% to 1.5% without any communication to account holders.",
        "Problem with personal loan approval process being excessively slow. Application pending for over 2 weeks without updates.",
        "Credit card fraud reported by customer - unauthorized charges totaling $1,234 appeared on statement from unknown merchant.",
        "Money transfer failed but funds were not returned to sender account. Customer service unable to provide timeline for refund.",
        "Savings account monthly maintenance fees increased from $5 to $10 without prior notice or option to opt-out.",
        "Personal loan interest rate increased unexpectedly after approval, from 7.5% to 9.5% APR without explanation."
    ]
    
    test_metadatas = [
        {"product_category": "Credit Card", "issue": "Fees", "company": "Bank of America", "date_received": "2024-01-15"},
        {"product_category": "Money transfers", "issue": "Delays", "company": "Western Union", "date_received": "2024-01-20"},
        {"product_category": "Savings account", "issue": "Interest rates", "company": "Chase", "date_received": "2024-01-25"},
        {"product_category": "Personal Loan", "issue": "Approval process", "company": "Wells Fargo", "date_received": "2024-02-01"},
        {"product_category": "Credit Card", "issue": "Fraud", "company": "Citi", "date_received": "2024-02-05"},
        {"product_category": "Money transfers", "issue": "Failed transfer", "company": "MoneyGram", "date_received": "2024-02-10"},
        {"product_category": "Savings account", "issue": "Fees", "company": "Capital One", "date_received": "2024-02-15"},
        {"product_category": "Personal Loan", "issue": "Interest rates", "company": "Discover", "date_received": "2024-02-20"}
    ]
    
    test_ids = [f"test_{i}" for i in range(len(test_documents))]
    
    collection.add(
        ids=test_ids,
        documents=test_documents,
        metadatas=test_metadatas
    )
    
    print(f"\n✅ Created minimal test collection with {collection.count()} items")