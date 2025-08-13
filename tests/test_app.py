"""
Basic tests for HolySheet application
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_app_imports():
    """Test that the main app module can be imported"""
    try:
        import app
        assert hasattr(app, 'HolySheetApp')
        assert hasattr(app, 'main')
    except ImportError as e:
        pytest.fail(f"Failed to import app module: {e}")


def test_holysheet_class():
    """Test HolySheetApp class instantiation"""
    try:
        import app
        holy_app = app.HolySheetApp()
        assert holy_app.claude is None
        assert holy_app.sheets_service is None
    except Exception as e:
        pytest.fail(f"Failed to instantiate HolySheetApp: {e}")


def test_extract_sheet_id():
    """Test Google Sheets ID extraction"""
    import app
    holy_app = app.HolySheetApp()
    
    # Test with full URL
    url = "https://docs.google.com/spreadsheets/d/1ABC123xyz/edit#gid=0"
    sheet_id = holy_app.extract_sheet_id(url)
    assert sheet_id == "1ABC123xyz"
    
    # Test with just ID
    direct_id = "1XYZ789abc"
    sheet_id = holy_app.extract_sheet_id(direct_id)
    assert sheet_id == "1XYZ789abc"


def test_required_packages():
    """Test that all required packages can be imported"""
    required_packages = [
        'streamlit',
        'anthropic', 
        'pandas',
        'googleapiclient',
        'google.oauth2'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            pytest.fail(f"Required package {package} not available")


if __name__ == "__main__":
    pytest.main([__file__])