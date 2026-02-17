"""Create FAISS vector store with ALL your data"""
import faiss
import pickle
import numpy as np
from .task2_config import INDEX_PATH, METADATA_PATH

def create_vectorstore(embeddings, chunks_df):
    """Build FAISS index from ALL embeddings"""
    print(f"\n🔧 Building FAISS index for {len(chunks_df):,} chunks...")
    
    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Create index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings.astype('float32'))
    
    # Prepare metadata for ALL chunks
    metadata = []
    for _, row in chunks_df.iterrows():
        metadata.append({
            'chunk_id': int(row['chunk_id']),
            'complaint_id': int(row['complaint_id']),
            'product': row['product'],
            'chunk_index': int(row['chunk_index']),
            'total_chunks': int(row['total_chunks']),
            'chunk_text_preview': row['chunk_text'][:200]
        })
    
    # Save
    faiss.write_index(index, str(INDEX_PATH))
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(metadata, f)
    
    # Size info
    index_size = INDEX_PATH.stat().st_size / 1024 / 1024
    meta_size = METADATA_PATH.stat().st_size / 1024 / 1024
    
    print(f"\n✅ FAISS index created:")
    print(f"  • Vectors: {index.ntotal:,}")
    print(f"  • Dimension: {dimension}")
    print(f"  • Index size: {index_size:.1f} MB")
    print(f"  • Metadata: {meta_size:.1f} MB")
    print(f"  • Location: {INDEX_PATH.parent}")
    
    return index, metadata

def search(query, model, index, metadata, k=3):
    """Test search on YOUR data"""
    q_emb = model.encode([query])
    faiss.normalize_L2(q_emb)
    scores, indices = index.search(q_emb.astype('float32'), k)
    
    print(f"\n🔍 Query: '{query}'")
    print("-" * 60)
    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < len(metadata):
            print(f"\n  {i+1}. Similarity: {score:.3f}")
            print(f"     Product: {metadata[idx]['product']}")
            print(f"     Text: {metadata[idx]['chunk_text_preview'][:150]}...")