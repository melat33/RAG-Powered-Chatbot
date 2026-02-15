"""Chunk ALL your real complaints"""
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .task2_config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNKS_PATH

def chunk_all_complaints(df):
    """Split ALL complaints into chunks"""
    print(f"\n🔪 Chunking {len(df):,} complaints...")
    
    # Print columns for debugging
    print(f"📋 Available columns: {df.columns.tolist()}")
    
    # Find the narrative column - try common names
    narrative_col = None
    for col in df.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['narrative', 'complaint', 'text', 'cleaned']):
            narrative_col = col
            break
    
    if not narrative_col:
        # If no obvious narrative column, use the first text column
        for col in df.columns:
            if df[col].dtype == 'object' and len(str(df[col].iloc[0])) > 100:
                narrative_col = col
                break
    
    if not narrative_col:
        narrative_col = df.columns[0]  # Fallback to first column
        print(f"⚠️ No narrative column found, using: '{narrative_col}'")
    else:
        print(f"📝 Using narrative column: '{narrative_col}'")
    
    # Find product column - DON'T assume 'Product_Category'
    product_col = None
    for col in df.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['product', 'category']):
            product_col = col
            break
    
    if not product_col:
        product_col = df.columns[0]  # Fallback
        print(f"⚠️ No product column found, using: '{product_col}'")
    else:
        print(f"🏷️ Using product column: '{product_col}'")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = []
    total_rows = len(df)
    
    for idx, row in df.iterrows():
        # Get text safely
        text = str(row[narrative_col]) if pd.notna(row[narrative_col]) else ""
        if len(text) < 10:
            continue
            
        text_chunks = splitter.split_text(text)
        
        for i, chunk in enumerate(text_chunks):
            chunks.append({
                'chunk_id': len(chunks),
                'complaint_id': idx,
                'product': str(row[product_col]) if pd.notna(row[product_col]) else 'Unknown',
                'chunk_index': i,
                'total_chunks': len(text_chunks),
                'chunk_text': chunk,
                'chunk_length': len(chunk)
            })
        
        # Progress update
        if (idx + 1) % 25000 == 0:
            print(f"  Processed {idx+1:,}/{total_rows:,} complaints ({((idx+1)/total_rows*100):.1f}%)")
    
    chunks_df = pd.DataFrame(chunks)
    print(f"\n✅ Created {len(chunks_df):,} chunks from {len(df):,} complaints")
    print(f"📊 Avg chunks per complaint: {len(chunks_df)/len(df):.2f}")
    
    # Show sample of product distribution
    print(f"\n📊 Product distribution in chunks:")
    print(chunks_df['product'].value_counts().head())
    
    # Save
    chunks_df.to_parquet(CHUNKS_PATH)
    print(f"💾 Saved: {CHUNKS_PATH}")
    
    return chunks_df