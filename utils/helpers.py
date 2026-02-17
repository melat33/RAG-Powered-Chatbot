"""
Utility functions and helpers
"""
import streamlit as st

def init_session_state():
    """Initialize session state variables"""
    defaults = {
        'db_connected': False,
        'query_history': [],
        'search_results': None,
        'total_searches': 0,
        'avg_time': 0.0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value