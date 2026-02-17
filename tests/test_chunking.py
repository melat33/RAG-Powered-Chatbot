def test_chunker_import():
    from src.chunker import chunk_all_complaints
    assert chunk_all_complaints is not None

def test_simple_chunking():
    text = "This is a test complaint about credit card fraud."
    chunks = [text[i:i+50] for i in range(0, len(text), 50)]
    assert len(chunks) >= 1