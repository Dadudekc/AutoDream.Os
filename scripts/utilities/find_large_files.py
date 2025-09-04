#!/usr/bin/env python3
"""Find Python files exceeding line limits."""


def find_large_python_files(directory="src", min_lines=300):
    """Find Python files exceeding the specified line count."""
    large_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = get_unified_utility().path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for line in f)
                        if line_count > min_lines:
                            large_files.append((file_path, line_count))
                except Exception as e:
                    get_logger(__name__).info(f"Error reading {file_path}: {e}")
    
    return sorted(large_files, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    get_logger(__name__).info("Python files over 300 lines:")
    large_files = find_large_python_files()
    
    for file_path, line_count in large_files[:15]:
        get_logger(__name__).info(f"{file_path}: {line_count} lines")
    
    get_logger(__name__).info(f"\nTotal files over 300 lines: {len(large_files)}")
