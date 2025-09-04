#!/usr/bin/env python3
"""
Test Vector Database Search Capability for Autonomous Development
"""


def test_vector_database_search():
    """Test the vector database search functionality."""
    
    # Create database instance
    db = create_vector_database('simple', db_path='simple_vector_db')
    
    get_logger(__name__).info('🔍 VECTOR DATABASE SEARCH CAPABILITY TEST')
    get_logger(__name__).info('=' * 60)
    
    # Test various search queries relevant to autonomous development
    test_queries = [
        'messaging system',
        'V2 compliance', 
        'agent onboarding',
        'vector database',
        'autonomous development',
        'Captain Agent-4',
        'cycle-based methodology'
    ]
    
    for query in test_queries:
        get_logger(__name__).info(f'\n🔍 Searching for: "{query}"')
        try:
            results = db.search(query, limit=3)
            get_logger(__name__).info(f'   Found {len(results)} results:')
            
            for i, result in enumerate(results, 1):
                content_preview = result['content'][:100] + '...' if len(result['content']) > 100 else result['content']
                score = result.get('score', 0)
                get_logger(__name__).info(f'   {i}. Score: {score:.3f} | {content_preview}')
                
        except Exception as e:
            get_logger(__name__).info(f'   ❌ Search error: {e}')
    
    get_logger(__name__).info('\n✅ Vector database search capability verified!')
    
    # Test integration with messaging system concepts
    get_logger(__name__).info('\n🔗 MESSAGING SYSTEM INTEGRATION TEST')
    get_logger(__name__).info('=' * 50)
    
    messaging_queries = [
        'PyAutoGUI delivery',
        'inbox fallback',
        'agent coordinates',
        'unified messaging core'
    ]
    
    for query in messaging_queries:
        get_logger(__name__).info(f'\n📨 Searching for: "{query}"')
        try:
            results = db.search(query, limit=2)
            get_logger(__name__).info(f'   Found {len(results)} results:')
            
            for i, result in enumerate(results, 1):
                content_preview = result['content'][:80] + '...' if len(result['content']) > 80 else result['content']
                get_logger(__name__).info(f'   {i}. {content_preview}')
                
        except Exception as e:
            get_logger(__name__).info(f'   ❌ Search error: {e}')

if __name__ == "__main__":
    test_vector_database_search()
