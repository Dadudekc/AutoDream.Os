#!/usr/bin/env python3
"""Test coordinate validation system"""

from src.core.coordinate_loader import CoordinateLoader

def test_coordinate_validation():
    """Test the coordinate validation system"""
    try:
        loader = CoordinateLoader()
        loader.load()
        report = loader.validate_all()
        
        print('📊 Coordinate Validation Results:')
        for line in report.to_lines():
            print(f'  {line}')
        
        status = "PASS" if report.is_all_ok() else "ISSUES FOUND"
        print(f'\n✅ Overall status: {status}')
        
        return report.is_all_ok()
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == "__main__":
    test_coordinate_validation()
