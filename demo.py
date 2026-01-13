# Save as: diagnose_vector_store.py
import os
import chromadb

print("🔍 DIAGNOSING VECTOR STORE")
print("=" * 50)

# Check if folder exists
store_path = "vector_store_1768244751"
print(f"1. Checking: {store_path}")
if os.path.exists(store_path):
    print(f"   ✅ Folder exists")
    
    # List contents
    print(f"\n2. Folder contents:")
    for item in os.listdir(store_path):
        size = os.path.getsize(os.path.join(store_path, item))
        print(f"   📄 {item} ({size:,} bytes)")
    
    # Try to connect
    print(f"\n3. Trying to connect...")
    try:
        client = chromadb.PersistentClient(path=store_path)
        collections = client.list_collections()
        print(f"   ✅ Connected to ChromaDB")
        print(f"   📋 Collections found: {len(collections)}")
        
        for col in collections:
            print(f"      • {col.name}: {col.count()} documents")
            
        if len(collections) == 0:
            print(f"\n❌ PROBLEM: Vector store has NO collections!")
            print(f"   This means your data was never loaded properly.")
            
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        
else:
    print(f"   ❌ Folder does NOT exist")
    print(f"\n📂 Available vector stores:")
    for item in os.listdir('.'):
        if os.path.isdir(item) and item.startswith('vector_store'):
            print(f"   📁 {item}")

print("\n" + "=" * 50)
print("🎯 SOLUTIONS:")
print("1. If folder is empty: Re-run your Task 3 notebook to create the vector store")
print("2. If wrong folder: Use the correct vector store path")
print("3. If no data: Check if your data loading worked in Task 3")