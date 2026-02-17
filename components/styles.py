"""
Custom CSS styling for the dashboard
"""
import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling"""
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        
        /* Header */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem 2.5rem;
            border-radius: 20px;
            margin: 1rem 0 2rem 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-content { display: flex; align-items: center; gap: 1.5rem; }
        .header-icon { font-size: 3rem; }
        .main-title { font-size: 2rem; font-weight: 800; color: white; }
        .subtitle { color: rgba(255,255,255,0.9); font-size: 1rem; }
        .header-badge { display: flex; gap: 0.5rem; }
        .badge {
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1rem;
            border-radius: 30px;
            color: white;
            font-weight: 500;
            backdrop-filter: blur(10px);
        }
        
        /* Cards */
        .metric-card {
            background: white;
            padding: 1.2rem;
            border-radius: 15px;
            text-align: center;
            border: 1px solid #eef2f6;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #667eea;
            line-height: 1.2;
        }
        .metric-label {
            color: #64748b;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Result Cards */
        .result-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid #eef2f6;
            box-shadow: 0 8px 20px rgba(0,0,0,0.02);
            transition: all 0.2s;
        }
        .result-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(102,126,234,0.1);
            border-color: #667eea40;
        }
        .result-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }
        .result-number {
            font-weight: 700;
            color: #94a3b8;
        }
        .confidence-high { color: #10b981; font-weight: 600; }
        .confidence-medium { color: #f59e0b; font-weight: 600; }
        .confidence-low { color: #ef4444; font-weight: 600; }
        .result-text {
            color: #1e293b;
            line-height: 1.6;
            margin: 1rem 0;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 12px;
        }
        
        /* Tags */
        .result-tags { display: flex; gap: 0.5rem; margin-top: 1rem; }
        .tag {
            padding: 0.4rem 1rem;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        .product { background: #e0f2fe; color: #0369a1; }
        .issue { background: #fee2e2; color: #b91c1c; }
        .company { background: #f3e8ff; color: #6b21a8; }
        .state { background: #d1fae5; color: #065f46; }
        
        /* Tips Card */
        .tips-card {
            background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
            border: 1px solid #667eea30;
            border-radius: 16px;
            padding: 1.5rem;
        }
        .example-box {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #475569;
            border: 1px solid #eef2f6;
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 4rem;
            background: #f8fafc;
            border-radius: 20px;
            border: 2px dashed #e2e8f0;
            margin: 2rem 0;
        }
        .empty-icon { font-size: 4rem; margin-bottom: 1rem; }
        
        /* Sidebar */
        .sidebar-card {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #eef2f6;
            margin: 0.5rem 0;
        }
        .history-item {
            background: #f8fafc;
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        .history-query { font-weight: 500; color: #1e293b; }
        .history-meta { font-size: 0.75rem; color: #94a3b8; margin-top: 0.2rem; }
    </style>
    """, unsafe_allow_html=True)