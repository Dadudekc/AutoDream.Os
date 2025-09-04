#!/usr/bin/env python3
"""
Diagnose Vector Database Issues
"""


def diagnose_vector_database():
    """Diagnose vector database functionality."""
    
    # Create database instance
    db = create_vector_database('simple', db_path='simple_vector_db')
    
    get_logger(__name__).info('🔍 VECTOR DATABASE DIAGNOSTIC')
    get_logger(__name__).info('=' * 50)
    
    # Check if we can get a specific document
    docs = db.list_documents()
    get_logger(__name__).info(f'📊 Total documents: {len(docs)}')
    
    if docs:
        # Try to get the first document
        first_doc_id = docs[0]
        get_logger(__name__).info(f'🔍 Testing document retrieval for: {first_doc_id[:16]}...')
        
        doc = db.get_document(first_doc_id)
        if doc:
            get_logger(__name__).info('✅ Document retrieval works')
            get_logger(__name__).info(f'   Content length: {len(doc["content"])}')
            get_logger(__name__).info(f'   Content preview: {doc["content"][:100]}...')
            
            # Test search with content from the document
            content_words = doc['content'].split()[:5]  # First 5 words
            test_query = ' '.join(content_words)
            get_logger(__name__).info(f'\n🔍 Testing search with: "{test_query}"')
            
            results = db.search(test_query, limit=1)
            get_logger(__name__).info(f'   Search results: {len(results)}')
            
            if results:
                get_logger(__name__).info('✅ Search functionality works')
                get_logger(__name__).info(f'   First result score: {results[0].get("score", 0)}')
            else:
                get_logger(__name__).info('❌ Search functionality not working')
                get_logger(__name__).info('   This suggests an index issue')
                
                # Check the internal index
                get_logger(__name__).info('\n🔍 Checking internal index...')
                if get_unified_validator().validate_hasattr(db, 'index'):
                    get_logger(__name__).info(f'   Index size: {len(db.index)}')
                    get_logger(__name__).info(f'   Document frequencies: {len(db.doc_frequencies)}')
                    get_logger(__name__).info(f'   Total docs: {db.total_docs}')
                    
                    # Show some index entries
                    if db.index:
                        sample_terms = list(db.index.keys())[:5]
                        get_logger(__name__).info(f'   Sample terms: {sample_terms}')
        else:
            get_logger(__name__).info('❌ Document retrieval failed')
    else:
        get_logger(__name__).info('❌ No documents found')

if __name__ == "__main__":
    diagnose_vector_database()
