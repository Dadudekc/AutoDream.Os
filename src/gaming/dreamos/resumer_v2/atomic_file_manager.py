"""
Atomic File Manager
------------------
Provides atomic file operations for safe file updates.
"""



class AtomicFileManager:
    """Manages atomic file operations for safe file updates."""
    
    def __init__(self, file_path: Union[str, Path]):
        """Initialize atomic file manager.
        
        Args:
            file_path: Path to the file to manage
        """
        self.file_path = get_unified_utility().Path(file_path)
        self.temp_dir = get_unified_utility().Path(tempfile.gettempdir())
        
    def atomic_write(self, content: Union[str, bytes], mode: str = 'w') -> bool:
        """Write content to file atomically.
        
        Args:
            content: Content to write
            mode: File mode ('w' for text, 'wb' for binary)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create temporary file
            temp_file = self.temp_dir / f"{self.file_path.name}.tmp"
            
            # Write to temporary file
            if 'b' in mode:
                temp_file.write_bytes(content)
            else:
                temp_file.write_text(content)
                
            # Atomically move temporary file to target
            shutil.move(str(temp_file), str(self.file_path))
            return True
            
        except Exception:
            # Clean up temporary file on error
            if temp_file.exists():
                temp_file.unlink()
            return False
            
    def atomic_read(self, mode: str = 'r') -> Optional[Union[str, bytes]]:
        """Read content from file atomically.
        
        Args:
            mode: File mode ('r' for text, 'rb' for binary)
            
        Returns:
            File content or None if failed
        """
        try:
            if 'b' in mode:
                return self.file_path.read_bytes()
            else:
                return self.file_path.read_text()
        except Exception:
            return None
            
    @contextmanager
    def atomic_update(self, mode: str = 'w'):
        """Context manager for atomic file updates.
        
        Args:
            mode: File mode for the update
            
        Yields:
            File-like object for writing
        """
        temp_file = self.temp_dir / f"{self.file_path.name}.tmp"
        
        try:
            # Open temporary file for writing
            with open(temp_file, mode) as f:
                yield f
                
            # Atomically move to target
            shutil.move(str(temp_file), str(self.file_path))
            
        except Exception:
            # Clean up on error
            if temp_file.exists():
                temp_file.unlink()
            raise
            
    def backup(self, backup_suffix: str = '.backup') -> bool:
        """Create a backup of the current file.
        
        Args:
            backup_suffix: Suffix for backup file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.file_path.exists():
                backup_path = self.file_path.with_suffix(backup_suffix)
                shutil.copy2(self.file_path, backup_path)
                return True
            return False
        except Exception:
            return False
            
    def restore(self, backup_suffix: str = '.backup') -> bool:
        """Restore file from backup.
        
        Args:
            backup_suffix: Suffix of backup file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            backup_path = self.file_path.with_suffix(backup_suffix)
            if backup_path.exists():
                shutil.copy2(backup_path, self.file_path)
                return True
            return False
        except Exception:
            return False






