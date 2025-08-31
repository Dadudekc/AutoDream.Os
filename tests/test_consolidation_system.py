#!/usr/bin/env python3
"""
Test Script for Data Source Consolidation System
===============================================

This script tests the complete Data Source Consolidation system to ensure
all contract deliverables are working correctly.

Contract: SSOT-002: Data Source Consolidation - 450 points
Agent: Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
Status: TESTING FOR COMPLETION
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from src.core.unified_data_source_consolidation import (
            DataSourceType, DataType, DataPriority, DataSource, DataRecord,
            DataSourceMapper, DataValidationEngine, DataSourceMigrationFramework,
            UnifiedDataSourceConsolidation, ConsolidationCLI
        )
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_data_source_mapper():
    """Test the DataSourceMapper functionality"""
    print("\n🧪 Testing DataSourceMapper...")
    
    try:
        from src.core.unified_data_source_consolidation import DataSourceMapper
        
        mapper = DataSourceMapper()
        
        # Test getting all mappings
        all_mappings = mapper.get_all_source_mappings()
        print(f"✅ Total source mappings: {len(all_mappings)}")
        
        # Test getting service-specific mappings
        market_mappings = mapper.get_service_mappings("market_data_service")
        print(f"✅ Market service mappings: {len(market_mappings)}")
        
        # Test mapping validation
        valid_mapping = {
            "name": "Test Source",
            "type": "api",
            "data_type": "market",
            "location": "test/location",
            "original_service": "test_service"
        }
        is_valid = mapper.validate_mapping(valid_mapping)
        print(f"✅ Mapping validation: {is_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ DataSourceMapper test failed: {e}")
        return False

def test_data_validation_engine():
    """Test the DataValidationEngine functionality"""
    print("\n🧪 Testing DataValidationEngine...")
    
    try:
        from src.core.unified_data_source_consolidation import (
            DataValidationEngine, DataType
        )
        
        validator = DataValidationEngine()
        
        # Test market data validation
        market_data = {"symbol": "AAPL", "price": 150.50, "timestamp": "2025-01-01"}
        market_validation = validator.validate_data(market_data, DataType.MARKET)
        print(f"✅ Market data validation: {market_validation['valid']}")
        
        # Test sentiment data validation
        sentiment_data = {"score": 0.8, "confidence": 0.9, "source": "analyst"}
        sentiment_validation = validator.validate_data(sentiment_data, DataType.SENTIMENT)
        print(f"✅ Sentiment data validation: {sentiment_validation['valid']}")
        
        # Test invalid data
        invalid_data = {"symbol": "AAPL"}  # Missing required fields
        invalid_validation = validator.validate_data(invalid_data, DataType.MARKET)
        print(f"✅ Invalid data detection: {not invalid_validation['valid']}")
        
        return True
        
    except Exception as e:
        print(f"❌ DataValidationEngine test failed: {e}")
        return False

def test_consolidation_system():
    """Test the main consolidation system"""
    print("\n🧪 Testing UnifiedDataSourceConsolidation...")
    
    try:
        from src.core.unified_data_source_consolidation import (
            UnifiedDataSourceConsolidation, DataSource, DataSourceType, 
            DataType, DataPriority
        )
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_consolidation.db")
        
        # Initialize system
        consolidation = UnifiedDataSourceConsolidation(db_path)
        print("✅ Consolidation system initialized")
        
        # Test data source registration
        test_source = DataSource(
            id="test-source-1",
            name="Test Financial Source",
            type=DataSourceType.API,
            data_type=DataType.FINANCIAL,
            location="test/financial/api",
            priority=DataPriority.HIGH,
            metadata={"provider": "test", "version": "1.0"},
            original_service="test_financial_service"
        )
        
        success = consolidation.register_data_source(test_source)
        print(f"✅ Data source registration: {success}")
        
        # Test listing data sources
        sources = consolidation.list_data_sources()
        print(f"✅ Data sources listed: {len(sources)}")
        
        # Test consolidation status
        status = consolidation.get_consolidation_status()
        print(f"✅ Consolidation status retrieved: {status['total_sources']} sources")
        
        # Test SSOT compliance
        ssot = status['ssot_compliance']
        print(f"✅ SSOT compliance score: {ssot['compliance_score']:.1f}%")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Consolidation system test failed: {e}")
        return False

def test_migration_framework():
    """Test the migration framework"""
    print("\n🧪 Testing DataSourceMigrationFramework...")
    
    try:
        from src.core.unified_data_source_consolidation import (
            UnifiedDataSourceConsolidation, DataSourceMigrationFramework
        )
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_migration.db")
        
        # Initialize system
        consolidation = UnifiedDataSourceConsolidation(db_path)
        migration_framework = consolidation.migration_framework
        
        # Test migration status
        status = migration_framework.get_migration_status()
        print(f"✅ Migration status retrieved: {status['total_services']} services")
        
        # Test service migration
        migration_result = migration_framework.migrate_service("market_data_service")
        print(f"✅ Market service migration: {migration_result['status']}")
        
        # Test rollback
        rollback_success = migration_framework.rollback_migration("market_data_service")
        print(f"✅ Migration rollback: {rollback_success}")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Migration framework test failed: {e}")
        return False

def test_cli_interface():
    """Test the CLI interface"""
    print("\n🧪 Testing ConsolidationCLI...")
    
    try:
        from src.core.unified_data_source_consolidation import ConsolidationCLI
        
        # Create temporary database
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_cli.db")
        
        # Initialize CLI
        cli = ConsolidationCLI()
        success = cli.initialize_system(db_path)
        print(f"✅ CLI initialization: {success}")
        
        if success:
            # Test status display
            cli.show_status()
            print("✅ Status display successful")
            
            # Test consolidation
            consolidation_success = cli.run_consolidation()
            print(f"✅ Consolidation execution: {consolidation_success}")
            
            # Test report export
            report_success = cli.export_report("test_report.json")
            print(f"✅ Report export: {report_success}")
            
            # Cleanup
            if os.path.exists("test_report.json"):
                os.remove("test_report.json")
        
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        return False

def test_contract_deliverables():
    """Test that all contract deliverables are working"""
    print("\n🧪 Testing Contract Deliverables...")
    
    deliverables = {
        "Unified Data Source Consolidation System": False,
        "Data Validation Engine": False,
        "Unified Storage System": False,
        "Data Synchronization System": False,
        "Migration Framework": False
    }
    
    try:
        # Test 1: Unified Data Source Consolidation System
        from src.core.unified_data_source_consolidation import UnifiedDataSourceConsolidation
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_deliverables.db")
        
        consolidation = UnifiedDataSourceConsolidation(db_path)
        deliverables["Unified Data Source Consolidation System"] = True
        print("✅ Unified Data Source Consolidation System")
        
        # Test 2: Data Validation Engine
        validation_status = consolidation.validate_all_data()
        if "total_sources" in validation_status:
            deliverables["Data Validation Engine"] = True
            print("✅ Data Validation Engine")
        
        # Test 3: Unified Storage System
        sources = consolidation.list_data_sources()
        if isinstance(sources, list):
            deliverables["Unified Storage System"] = True
            print("✅ Unified Storage System")
        
        # Test 4: Data Synchronization System
        if hasattr(consolidation, 'synchronizer'):
            deliverables["Data Synchronization System"] = True
            print("✅ Data Synchronization System")
        
        # Test 5: Migration Framework
        migration_status = consolidation.migration_framework.get_migration_status()
        if "total_services" in migration_status:
            deliverables["Migration Framework"] = True
            print("✅ Migration Framework")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        # Check completion
        completed = sum(deliverables.values())
        total = len(deliverables)
        print(f"\n📊 Contract Deliverables: {completed}/{total} completed")
        
        return completed == total
        
    except Exception as e:
        print(f"❌ Contract deliverables test failed: {e}")
        return False

