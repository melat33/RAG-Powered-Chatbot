"""
Sidebar component with database controls and history
"""
import streamlit as st
from datetime import datetime

def render_sidebar():
    """Render the sidebar with database controls and history"""
    
    with st.sidebar:
        st.markdown("### 🔧 System Control")
        
        # Database connection card
        with st.container():
            st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
            
            if not st.session_state.get('db_connected', False):
                if st.button("🚀 Initialize Database", type="primary", use_container_width=True):
                    with st.spinner("Connecting to vector store..."):
                        success, message, stats = st.session_state.db.connect()
                        if success:
                            st.session_state.db_connected = True
                            st.session_state.db_stats = stats
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            else:
                st.success("✅ Database Active")
                
                # Stats display
                stats = st.session_state.get('db_stats', {})
                cols = st.columns(2)
                cols[0].metric("Documents", f"{stats.get('count', 0):,}")
                cols[1].metric("Dimension", stats.get('dimension', 384))
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        # Quick search templates
        quick_searches = [
            ("💳 Credit Card Fraud", "unauthorized credit card charges fraud"),
            ("🏠 Mortgage Delays", "mortgage application processing delayed"),
            ("💰 Hidden Bank Fees", "unexpected fees charges checking account"),
            ("📄 Loan Issues", "personal loan rejection credit score"),
            ("💸 Payment Problems", "payment processing failed errors")
        ]
        
        for emoji, query in quick_searches:
            if st.button(f"{emoji}", key=f"quick_{query[:10]}", use_container_width=True):
                st.session_state.quick_query = query
                st.session_state.search_triggered = True
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📝 Recent Activity")
        
        # Search history
        if st.session_state.query_history:
            for item in reversed(st.session_state.query_history[-5:]):
                with st.container():
                    st.markdown(f"""
                    <div class="history-item">
                        <div class="history-query">🔍 {item['query'][:25]}...</div>
                        <div class="history-meta">⏱️ {item['time']:.2f}s • 📅 {item['timestamp']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.query_history = []
                st.session_state.search_results = None
                st.rerun()
        else:
            st.caption("No searches yet")