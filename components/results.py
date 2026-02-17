"""
Results display component with cards and visualizations
"""
import streamlit as st
import pandas as pd
import plotly.express as px

def render_results():
    """Render search results with cards and analytics"""
    
    if not st.session_state.get('search_results'):
        # Empty state
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔍</div>
            <h3>Ready to Search</h3>
            <p>Enter a query above to analyze financial complaints</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    results = st.session_state.search_results
    
    # Metrics row
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['count']}</div>
            <div class="metric-label">Results Found</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{results['time']:.2f}s</div>
            <div class="metric-label">Search Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Calculate average relevance
    if results['distances']:
        avg_rel = 100 - (sum(results['distances']) / len(results['distances']) * 100)
    else:
        avg_rel = 0
    
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_rel:.0f}%</div>
            <div class="metric-label">Avg Relevance</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Product distribution
    products = {}
    for meta in results['metadatas']:
        if meta and 'product' in meta:
            products[meta['product']] = products.get(meta['product'], 0) + 1
    
    with cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(products)}</div>
            <div class="metric-label">Products</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Results cards
    st.markdown(f"### 📋 Results for: '{results['query']}'")
    
    for i, (doc, meta, dist) in enumerate(zip(
        results['documents'],
        results['metadatas'],
        results['distances']
    )):
        relevance = 100 - (dist * 100)
        confidence_class = "high" if relevance > 70 else "medium" if relevance > 40 else "low"
        
        st.markdown(f"""
        <div class="result-card">
            <div class="result-header">
                <span class="result-number">#{i+1}</span>
                <span class="confidence-{confidence_class}">{relevance:.1f}% match</span>
            </div>
            <div class="result-text">{doc}</div>
            <div class="result-tags">
        """, unsafe_allow_html=True)
        
        # Tags
        cols = st.columns(4)
        if meta:
            with cols[0]:
                st.markdown(f'<span class="tag product">📊 {meta.get("product", "N/A")}</span>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f'<span class="tag issue">⚠️ {meta.get("issue", "General")}</span>', unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f'<span class="tag company">🏢 {meta.get("company", "Unknown")}</span>', unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f'<span class="tag state">📍 {meta.get("state", "N/A")}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)