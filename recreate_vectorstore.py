#!/usr/bin/env python3
"""Script to recreate the vectorstore with proper embeddings."""

import sys
import os
import shutil
sys.path.append('.')

from constitution_chat.core.constitution_db import ConstitutionDatabase

def recreate_vectorstore():
    """Recreate the vectorstore to eliminate deprecated warnings."""
    print("Recreating vectorstore with proper embeddings...")
    
    # Initialize database
    db = ConstitutionDatabase()
    
    # Remove old vectorstore if it exists
    vectorstore_path = "vectorstore/constitution_faiss"
    if os.path.exists(vectorstore_path):
        print(f"Removing old vectorstore at {vectorstore_path}")
        shutil.rmtree(vectorstore_path)
    
    # Create new vectorstore
    print("Creating new vectorstore with real embeddings...")
    vectorstore = db.create_vectorstore(force_recreate=True)
    
    print("✅ Vectorstore recreated successfully!")
    
    # Test search
    test_query = "fundamental rights freedom"
    results = db.search_similar(test_query, k=2)
    print(f"✅ Test search returned {len(results)} results")
    
    for i, doc in enumerate(results):
        preview = doc.page_content[:100].replace('\n', ' ')
        print(f"   Result {i+1}: {preview}...")

if __name__ == "__main__":
    recreate_vectorstore()