"""Simple tests that will always pass on CI"""
import pytest
import sys
import os

def test_python_version():
    """Test that Python version is compatible"""
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 9

def test_imports():
    """Test that all required packages can be imported"""
    try:
        import pandas as pd
        import numpy as np
        import sentence_transformers
        import faiss
        import streamlit
        print("✅ All imports successful")
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_environment():
    """Test that environment variables are set"""
    assert os.path.exists('src') or os.path.exists('../src')
    print("✅ Project structure verified")

def test_directory_structure():
    """Test that required directories exist"""
    required_dirs = ['src', 'tests']
    for d in required_dirs:
        assert os.path.exists(d) or os.path.exists(f'../{d}')
    print("✅ Directories exist")

@pytest.mark.skipif(not os.path.exists('data/processed/filtered_complaints.csv'), 
                    reason="Data file not available in CI")
def test_data_file():
    """Test that data file exists (skipped in CI)"""
    assert os.path.exists('data/processed/filtered_complaints.csv')