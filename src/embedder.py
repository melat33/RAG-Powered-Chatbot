"""Generate embeddings for ALL your chunks"""
import numpy as np
import time
from sentence_transformers import SentenceTransformer
from .task2_config import EMBEDDING_MODEL, BATCH_SIZE, EMBEDDINGS_PATH


def generate_all_embeddings(chunks_df):
    """Create embeddings for ALL chunks"""
    print(f"\n🤖 Generating embeddings for {len(chunks_df):,} chunks...")

    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = chunks_df["chunk_text"].tolist()

    start = time.time()
    all_embeddings = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        batch_embeddings = model.encode(batch, show_progress_bar=False)
        all_embeddings.append(batch_embeddings)

        if (i // BATCH_SIZE + 1) % 10 == 0:
            processed = min(i + BATCH_SIZE, len(texts))
            pct = processed / len(texts) * 100
            elapsed = time.time() - start
            print(f"  {processed:,}/{len(texts):,} ({pct:.1f}%) - {elapsed/60:.1f} min")

    embeddings = np.vstack(all_embeddings)
    elapsed = time.time() - start

    print(f"\n✅ Embeddings created: {embeddings.shape}")
    print(f"⏱️  Time: {elapsed/60:.2f} minutes")
    print(f"⚡ Speed: {len(texts)/elapsed:.1f} chunks/sec")

    np.save(EMBEDDINGS_PATH, embeddings)
    print(f"💾 Saved: {EMBEDDINGS_PATH}")

    return embeddings, model
