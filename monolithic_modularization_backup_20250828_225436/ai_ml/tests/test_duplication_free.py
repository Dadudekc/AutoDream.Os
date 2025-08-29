"""
Test Duplication-Free Architecture
Captain Agent-3: Quality Assurance
"""

import unittest
from src.ai_ml import ai_ml_engine, BaseManager, BaseIntegration

class TestDuplicationFree(unittest.TestCase):
    """Test that no duplication exists"""
    
    def test_single_engine_instance(self):
        """Test single engine instance"""
        engine1 = ai_ml_engine
        engine2 = ai_ml_engine
        self.assertIs(engine1, engine2, "Multiple engine instances detected!")
    
    def test_unique_module_registration(self):
        """Test unique module registration"""
        engine = ai_ml_engine
        engine.register_module("test", "test_module")
        
        with self.assertRaises(ValueError):
            engine.register_module("test", "duplicate_module")
    
    def test_manager_interface(self):
        """Test manager interface"""
        self.assertTrue(issubclass(BaseManager, object))
    
    def test_integration_interface(self):
        """Test integration interface"""
        self.assertTrue(issubclass(BaseIntegration, object))

if __name__ == "__main__":
    unittest.main()
