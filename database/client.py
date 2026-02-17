"""
Database client for ChromaDB operations
"""
import chromadb
from chromadb.utils import embedding_functions
import os
from typing import Dict, Optional, Tuple

class DatabaseClient:
    """ChromaDB client wrapper"""
    
    def __init__(self, path: str = "vector_store"):
        self.path = path
        self.client = None
        self.collection = None
        self.embedding_fn = None
    
    def connect(self) -> Tuple[bool, str, Dict]:
        """Connect to database"""
        try:
            os.makedirs(self.path, exist_ok=True)
            
            # Initialize client
            self.client = chromadb.PersistentClient(path=self.path)
            
            # Setup embeddings
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(
                    name="financial_complaints",
                    embedding_function=self.embedding_fn
                )
            except:
                self.collection = self.client.create_collection(
                    name="financial_complaints",
                    embedding_function=self.embedding_fn
                )
                self._load_sample_data()
            
            count = self.collection.count()
            return True, f"✅ Connected with {count:,} documents", {
                "count": count,
                "dimension": 384,
                "status": "ready"
            }
            
        except Exception as e:
            return False, f"❌ Connection failed: {str(e)}", {}
    
    def search(self, query: str, n_results: int = 5) -> Optional[Dict]:
        """Search for similar documents"""
        if not self.collection:
            return None
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            return {
                "documents": results['documents'][0],
                "metadatas": results['metadatas'][0],
                "distances": results['distances'][0],
                "query": query,
                "count": len(results['documents'][0])
            }
        except Exception as e:
            return None
    
    def _load_sample_data(self):
        """Load sample data (same as before)"""
        # Copy your sample data loading logic here
        pass