"""Chunk ALL your real complaints"""
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .task2_config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNKS_PATH


def chunk_all_complaints(df):
    """Split ALL complaints into chunks"""
    print(f"\n🔪 Chunking {len(df):,} complaints...")
    print(f"📋 Available columns: {df.columns.tolist()}")

    # YOUR EXACT COLUMN NAMES from the data
    NARRATIVE_COL = "Consumer complaint narrative"  # ← THIS is the correct column!
    PRODUCT_COL = "Product_Category"  # Use the mapped category column
    ID_COL = "Complaint ID"

    print(f"📝 Using narrative column: '{NARRATIVE_COL}'")
    print(f"🏷️ Using product column: '{PRODUCT_COL}'")

    # Check if columns exist
    if NARRATIVE_COL not in df.columns:
        print(f"❌ ERROR: '{NARRATIVE_COL}' not found!")
        return pd.DataFrame()

    # Filter to rows with narratives
    df_valid = df[df[NARRATIVE_COL].notna()].copy()
    print(f"📊 Complaints with narratives: {len(df_valid):,}")

    if len(df_valid) == 0:
        print("❌ No narratives found!")
        return pd.DataFrame()

    # Initialize text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    total = len(df_valid)

    for idx, (original_idx, row) in enumerate(df_valid.iterrows()):
        text = str(row[NARRATIVE_COL])
        if len(text) < 10:  # Skip very short texts
            continue

        # Split into chunks
        text_chunks = splitter.split_text(text)

        for i, chunk in enumerate(text_chunks):
            chunks.append(
                {
                    "chunk_id": len(chunks),
                    "complaint_id": int(row[ID_COL])
                    if ID_COL in df.columns
                    else original_idx,
                    "product": str(row[PRODUCT_COL])
                    if PRODUCT_COL in df.columns
                    else "Unknown",
                    "chunk_index": i,
                    "total_chunks": len(text_chunks),
                    "chunk_text": chunk,
                    "chunk_length": len(chunk),
                }
            )

        # Progress update every 10,000 complaints
        if (idx + 1) % 10000 == 0:
            print(
                f"  Progress: {idx+1:,}/{total:,} complaints ({((idx+1)/total*100):.1f}%)"
            )

    # Create DataFrame
    chunks_df = pd.DataFrame(chunks)
    print(f"\n✅ Created {len(chunks_df):,} chunks from {total:,} complaints")

    if len(chunks_df) > 0:
        print(f"📊 Avg chunks per complaint: {len(chunks_df)/total:.2f}")
        print(f"\n📊 Product distribution in chunks:")
        print(chunks_df["product"].value_counts())

        # Save chunks
        chunks_df.to_parquet(CHUNKS_PATH)
        print(f"💾 Saved: {CHUNKS_PATH}")
    else:
        print("⚠️ No chunks created - check your narrative column")

    return chunks_df
