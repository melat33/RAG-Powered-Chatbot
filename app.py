"""
🏆 Financial Complaints Intelligence Dashboard
Main entry point for the Streamlit application
"""
import streamlit as st
from components.sidebar import render_sidebar
from components.search import render_search_section
from components.results import render_results
from components.styles import apply_custom_css
from database.client import DatabaseClient
from utils.helpers import init_session_state

# Page configuration
st.set_page_config(
    page_title="FinInsight - Complaint Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

# Initialize session state
init_session_state()

# Header
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <div class="header-icon">🏦</div>
        <div>
            <div class="main-title">FinInsight Intelligence</div>
            <div class="subtitle">AI-Powered Financial Complaint Analysis Platform</div>
        </div>
    </div>
    <div class="header-badge">
        <span class="badge">v2.0</span>
        <span class="badge">Enterprise</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize database client
if "db" not in st.session_state:
    st.session_state.db = DatabaseClient()

# Render sidebar
render_sidebar()

# Main content area
col1, col2 = st.columns([3.5, 1])

with col1:
    render_search_section()
    render_results()

with col2:
    st.markdown("### 💡 Pro Tips")
    with st.container():
        st.markdown("""
        <div class="tips-card">
            <h4>🎯 Search Strategies</h4>
            <ul>
                <li>🔍 Be specific about products</li>
                <li>📝 Mention exact issues</li>
                <li>💰 Use financial keywords</li>
                <li>🔄 Try multiple variations</li>
            </ul>
            <div class="example-box">
                <strong>Examples:</strong><br>
                • "credit card unauthorized charges"<br>
                • "mortgage application delays"<br>
                • "hidden bank fees complaints"<br>
                • "loan rejection reasons"
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Analytics mini-dashboard
    if st.session_state.get('total_searches', 0) > 0:
        st.markdown("### 📊 Today's Activity")
        cols = st.columns(2)
        cols[0].metric("Searches", st.session_state.total_searches)
        cols[1].metric("Avg. Time", f"{st.session_state.avg_time:.2f}s")