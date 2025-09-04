from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
Fix Vector Database Encoding Issues and Ingest Documentation for Autonomous Development

This script addresses the character encoding issues in the existing vector database
and ensures proper ingestion of all project documentation for autonomous development.
"""

from ..core.unified_import_system import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_encoding_and_reingest():
    """Fix encoding issues and reingest all documentation."""
    
    get_logger(__name__).info("🚨 VECTOR DATABASE ENCODING FIX & DOCUMENTATION INGESTION")
    get_logger(__name__).info("=" * 70)
    
    # Create a fresh vector database instance
    
    # Use a new database path to avoid encoding issues
    fresh_db_path = "autonomous_dev_vector_db"
    db = create_vector_database("simple", db_path=fresh_db_path)
    
    get_logger(__name__).info(f"✅ Created fresh vector database at: {fresh_db_path}")
    
    # Find all documentation files
    documentation_files = find_documentation_files()
    get_logger(__name__).info(f"📋 Found {len(documentation_files)} documentation files to ingest")
    
    # Ingest documentation files
    ingested_count = 0
    failed_count = 0
    
    for file_path in documentation_files:
        try:
            # Read file content
            content = read_file_safely(file_path)
            if content:
                # Generate document ID
                doc_id = generate_document_id(file_path)
                
                # Determine document type
                doc_type = determine_document_type(file_path)
                
                # Create metadata
                metadata = {
                    'type': doc_type,
                    'file_path': str(file_path),
                    'file_size': len(content),
                    'ingested_at': datetime.now().isoformat(),
                    'word_count': len(content.split())
                }
                
                # Add to database
                success = db.add_document(doc_id, content, metadata)
                
                if success:
                    ingested_count += 1
                    if ingested_count % 50 == 0:
                        get_logger(__name__).info(f"   📄 Ingested {ingested_count} documents...")
                else:
                    failed_count += 1
                    get_logger(__name__).warning(f"Failed to ingest: {file_path}")
                    
        except Exception as e:
            failed_count += 1
            get_logger(__name__).error(f"Error ingesting {file_path}: {e}")
    
    get_logger(__name__).info(f"\n✅ INGESTION COMPLETE:")
    get_logger(__name__).info(f"   📄 Successfully ingested: {ingested_count} documents")
    get_logger(__name__).info(f"   ❌ Failed: {failed_count} documents")
    
    # Test search functionality
    test_search_functionality(db)
    
    return db

def find_documentation_files() -> List[Path]:
    """Find all documentation files in the project."""
    
    documentation_files = []
    skip_dirs = {'__pycache__', '.git', 'node_modules', '.pytest_cache', 'venv', 'env'}
    skip_files = {'.DS_Store', 'Thumbs.db'}
    
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file in skip_files:
                continue
                
            file_path = get_unified_utility().Path(root) / file
            
            # Include various documentation file types
            if file.endswith(('.md', '.py', '.js', '.ts', '.json', '.yml', '.yaml', '.txt')):
                # Skip very large files
                try:
                    if file_path.stat().st_size < 1024 * 1024:  # 1MB limit
                        documentation_files.append(file_path)
                except:
                    pass
    
    return documentation_files

def read_file_safely(file_path: Path) -> str:
    """Read file content with multiple encoding attempts."""
    
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                return content
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
    
    # If all encodings fail, try to read as binary and decode with errors='replace'
    try:
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8', errors='replace')
            return content
    except Exception:
        return ""

def generate_document_id(file_path: Path) -> str:
    """Generate a unique document ID."""
    return hashlib.md5(str(file_path).encode()).hexdigest()

def determine_document_type(file_path: Path) -> str:
    """Determine the type of document based on path and extension."""
    
    path_str = str(file_path).lower()
    
    if 'agent_workspaces' in path_str:
        return 'agent_communication'
    elif 'docs' in path_str:
        return 'documentation'
    elif 'src' in path_str:
        return 'source_code'
    elif 'config' in path_str:
        return 'configuration'
    elif 'scripts' in path_str:
        return 'script'
    elif 'tests' in path_str:
        return 'test'
    elif file_path.suffix == '.md':
        return 'markdown'
    elif file_path.suffix == '.py':
        return 'python'
    elif file_path.suffix in ['.js', '.ts']:
        return 'javascript'
    elif file_path.suffix in ['.yml', '.yaml']:
        return 'yaml'
    elif file_path.suffix == '.json':
        return 'json'
    else:
        return 'general'

def test_search_functionality(db):
    """Test the search functionality of the vector database."""
    
    get_logger(__name__).info("\n🔍 TESTING SEARCH FUNCTIONALITY")
    get_logger(__name__).info("=" * 50)
    
    test_queries = [
        'messaging system',
        'V2 compliance',
        'agent onboarding',
        'vector database',
        'autonomous development',
        'Captain Agent-4',
        'cycle-based methodology',
        'PyAutoGUI delivery'
    ]
    
    for query in test_queries:
        try:
            results = db.search(query, limit=2)
            get_logger(__name__).info(f"🔍 '{query}': {len(results)} results")
            
            if results:
                for i, result in enumerate(results, 1):
                    content_preview = result['content'][:80] + '...' if len(result['content']) > 80 else result['content']
                    score = result.get('score', 0)
                    get_logger(__name__).info(f"   {i}. Score: {score:.3f} | {content_preview}")
        except Exception as e:
            get_logger(__name__).info(f"❌ Search error for '{query}': {e}")
    
    get_logger(__name__).info("\n✅ Search functionality test complete!")


if __name__ == "__main__":
    main()
