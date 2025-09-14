"""
Simple test for Constitution RAG system functionality
"""

import sys
sys.path.append('.')

from constitution_chat.core.constitution_db import ConstitutionDatabase

def test_constitution_db():
    """Test the Constitution Database"""
    print("Testing Constitution Database...")
    
    # Test database initialization
    db = ConstitutionDatabase()
    print("✓ Database initialized")
    
    # Test vectorstore loading
    vectorstore = db.get_vectorstore()
    print("✓ Vectorstore loaded")
    
    # Test search functionality
    results = db.search_similar("fundamental rights", k=3)
    print(f"✓ Search returned {len(results)} results")
    
    for i, doc in enumerate(results[:2]):  # Show first 2 results
        print(f"   Result {i+1}: {doc.page_content[:100]}...")
    
    return True

if __name__ == "__main__":
    try:
        test_constitution_db()
        print("\n✅ Constitution Database test passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()