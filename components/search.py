"""
Search input and processing component
"""
import streamlit as st
import time
from datetime import datetime

def render_search_section():
    """Render the search input section"""
    
    st.markdown("### 🔍 Semantic Search")
    
    # Search input with suggestions
    query = st.text_input(
        "Search",
        placeholder="e.g., 'What are common credit card complaints?' or 'mortgage problems'",
        value=st.session_state.get('quick_query', ''),
        key="search_input",
        label_visibility="collapsed"
    )
    
    # Clear quick query after use
    if 'quick_query' in st.session_state:
        del st.session_state.quick_query
    
    # Search button row
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Process search
    if search_clicked or st.session_state.get('search_triggered', False):
        if query:
            if not st.session_state.get('db_connected', False):
                st.error("⚠️ Please connect to database first")
                return
            
            with st.spinner("🔍 Searching knowledge base..."):
                # Animated progress
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.005)
                    progress.progress(i + 1)
                progress.empty()
                
                # Execute search
                start = time.time()
                results = st.session_state.db.search(query, n_results=5)
                search_time = time.time() - start
                
                if results:
                    results['time'] = search_time
                    st.session_state.search_results = results
                    
                    # Update history
                    st.session_state.query_history.append({
                        "query": query,
                        "time": search_time,
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                    
                    # Update stats
                    st.session_state.total_searches = st.session_state.get('total_searches', 0) + 1
                    total = st.session_state.total_searches
                    current_avg = st.session_state.get('avg_time', 0)
                    st.session_state.avg_time = (current_avg * (total-1) + search_time) / total
                    
                    st.session_state.search_triggered = False
                    st.rerun()