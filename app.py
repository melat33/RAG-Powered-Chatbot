import streamlit as st
from modules.database import VectorDatabase
from modules.search import SearchManager
from modules.ui_components import UIComponents
import time

# Constants (no magic numbers)
CONFIG = {
    "VECTOR_STORE_PATH": "notebooks/vector_store_1768244751",
    "COLLECTION_NAME": "financial_complaints",
    "SEARCH_RESULTS_COUNT": 5,
    "RECENT_SEARCHES_LIMIT": 5,
    "HISTORY_MAX_ENTRIES": 50
}

# Initialize session state properly
def init_session_state():
    if "search_manager" not in st.session_state:
        st.session_state.search_manager = SearchManager()
    if "db_client" not in st.session_state:
        st.session_state.db_client = VectorDatabase(CONFIG["VECTOR_STORE_PATH"])
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "last_processed_query" not in st.session_state:
        st.session_state.last_processed_query = None

def main():
    # Initialize session state
    init_session_state()
    
    # Page config
    st.set_page_config(
        page_title="Financial Complaints Analyzer",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS (keep your existing CSS)
    # ... [Your CSS code here] ...
    
    try:
        # Connect to database
        if not st.session_state.db_client.connect():
            st.error("Failed to connect to database. Please check if the vector store exists.")
            st.stop()
        
        # Rest of your main function code here
        # ... [Your main app logic] ...
        
    except ConnectionError as e:
        st.error(f"Database connection error: {str(e)}")
        display_fallback_ui()
    except ValueError as e:
        st.error(f"Data validation error: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        display_error_ui(e)

def display_fallback_ui():
    """Display fallback UI when database is unavailable"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🔧</div>
        <h3>Database Unavailable</h3>
        <p>Please check if the vector store exists at: notebooks/vector_store_1768244751</p>
    </div>
    """, unsafe_allow_html=True)

def display_error_ui(error):
    """Display error UI with troubleshooting tips"""
    with st.expander("🛠️ Technical Details"):
        st.code(f"Error type: {type(error).__name__}\nError message: {str(error)}")
    
    st.markdown("### Troubleshooting Steps:")
    st.markdown("""
    1. **Verify vector store location**
    2. **Check collection name**
    3. **Restart the application**
    """)

if __name__ == "__main__":
    main()