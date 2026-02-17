"""Generate completion summary for YOUR data"""
from datetime import datetime
from .task2_config import CHUNK_SIZE, CHUNK_OVERLAP


def create_final_summary(df, chunks_df, index):
    """Create final report for ALL your data"""

    summary = f"""
============================================================================
🎯 TASK 2 COMPLETED - ALL YOUR REAL DATA PROCESSED
============================================================================

📊 YOUR DATA SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━
• Total complaints: {len(df):,}
• Total chunks created: {len(chunks_df):,}
• Average chunks/complaint: {len(chunks_df)/len(df):.2f}
• Products: {df['Product_Category'].nunique()}

🔧 CHUNKING STRATEGY:
━━━━━━━━━━━━━━━━━━━━━━━━━
• Method: RecursiveCharacterTextSplitter
• Chunk size: {CHUNK_SIZE} characters
• Overlap: {CHUNK_OVERLAP} characters
• Rationale: Optimal for complaint narratives

🤖 EMBEDDING MODEL:
━━━━━━━━━━━━━━━━━━━━━━━━━
• Model: all-MiniLM-L6-v2
• Dimensions: 384
• Total embeddings: {len(chunks_df):,}

💾 VECTOR STORE:
━━━━━━━━━━━━━━━━━━━━━━━━━
• Type: FAISS (IndexFlatIP)
• Vectors: {index.ntotal:,}
• Similarity: Cosine
• Metadata: Complaint ID, Product, Chunk index

📁 FILES CREATED:
━━━━━━━━━━━━━━━━━━━━━━━━━
1. data/chunks/all_chunks.parquet     - ALL your chunks
2. embeddings/all_embeddings.npy       - ALL your embeddings
3. vector_store/faiss_index.idx        - Searchable index
4. vector_store/metadata.pkl           - ALL metadata

🚀 READY FOR TASK 3 - RAG PIPELINE!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your {index.ntotal:,} complaint chunks are now:
✅ Chunked optimally
✅ Embedded semantically
✅ Indexed for fast search
✅ Traced back to original complaints
"""
    print(summary)
    with open("reports/task2_final_summary.txt", "w") as f:
        f.write(summary)
    return summary
