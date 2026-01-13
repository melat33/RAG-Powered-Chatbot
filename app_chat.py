# app_chat.py - Conversational Chat Interface
import streamlit as st
import chromadb
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Financial Complaints Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat interface
st.markdown("""
<style>
    /* Main container */
    .main-container {
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header */
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .chat-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .chat-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.2rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-message {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    /* Message header */
    .message-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    /* Source cards */
    .source-card {
        background: white;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .source-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .source-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    
    .source-tag {
        background: #e9ecef;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        color: #495057;
    }
    
    /* Confidence badge */
    .confidence-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .confidence-high { background: #10b98120; color: #10b981; }
    .confidence-medium { background: #f59e0b20; color: #f59e0b; }
    .confidence-low { background: #ef444420; color: #ef4444; }
    
    /* Chat input */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 15px 20px;
        font-size: 16px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
        margin-top: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Stats cards */
    .stats-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
    
    .stats-value {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stats-label {
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar */
    .sidebar-section {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "conversation_stats" not in st.session_state:
    st.session_state.conversation_stats = {
        "total_messages": 0,
        "user_messages": 0,
        "assistant_messages": 0,
        "avg_confidence": 0,
        "last_query_time": None
    }

if "vector_store_connected" not in st.session_state:
    st.session_state.vector_store_connected = False

# Initialize ChromaDB
def initialize_vector_store():
    try:
        client = chromadb.PersistentClient(path="notebooks/vector_store_1768244751")
        collection = client.get_collection("financial_complaints")
        st.session_state.vector_store_connected = True
        return collection
    except Exception as e:
        st.session_state.vector_store_connected = False
        return None

# Mock RAG function (replace with your actual RAG pipeline)
def get_rag_response(query, collection):
    """Get response from RAG system"""
    if not collection:
        return "I'm sorry, I cannot connect to the complaints database at the moment.", []
    
    try:
        # Query the vector store
        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )
        
        # Process results
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        # Generate response
        response = f"I found {len(documents)} relevant complaints about '{query}'.\n\n"
        
        if documents:
            response += "Here are the key insights:\n"
            for i, doc in enumerate(documents[:3]):
                response += f"\n**{i+1}. {doc[:150]}...**"
            
            response += "\n\nBased on these complaints, I recommend reviewing customer service processes "
            response += "and ensuring proper communication channels."
        
        # Prepare sources
        sources = []
        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            sources.append({
                "id": i + 1,
                "text": doc[:200] + "..." if len(doc) > 200 else doc,
                "product": meta.get('product_category', 'Unknown') if meta else 'Unknown',
                "issue": meta.get('issue', 'General') if meta else 'General',
                "company": meta.get('company', 'Unknown') if meta else 'Unknown'
            })
        
        return response, sources
    
    except Exception as e:
        return f"Error processing query: {str(e)}", []

# Calculate confidence level
def get_confidence_level(distance):
    if distance < 0.3:
        return "HIGH", "confidence-high"
    elif distance < 0.6:
        return "MEDIUM", "confidence-medium"
    else:
        return "LOW", "confidence-low"

# Header
st.markdown("""
<div class="chat-header">
    <div class="chat-title">💬 Financial Complaints Chat Assistant</div>
    <div class="chat-subtitle">Ask questions about financial complaints - Get AI-powered insights with sources</div>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([3, 1])

with col1:
    # Chat container
    st.markdown("### 💬 Conversation")
    
    # Clear chat button
    col_btn1, col_btn2 = st.columns([1, 6])
    with col_btn1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_stats = {
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "avg_confidence": 0,
                "last_query_time": None
            }
            st.rerun()
    
    # Chat display
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">💬</div>
            <h3 style="color: #475569;">Start a conversation</h3>
            <p style="color: #64748b;">Ask questions about financial complaints to get AI-powered insights.</p>
            <div style="background: #f8fafc; padding: 1rem; border-radius: 10px; margin-top: 2rem;">
                <p><strong>💡 Try asking:</strong></p>
                <ul style="text-align: left; display: inline-block;">
                    <li>What are common credit card complaints?</li>
                    <li>Tell me about mortgage application issues</li>
                    <li>What customer service problems exist?</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-header">
                    <span>👤 You</span>
                    <span>{message.get("timestamp", "")}</span>
                </div>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Assistant message
            confidence_html = ""
            if message.get("confidence"):
                conf_level, conf_class = get_confidence_level(1 - (message["confidence"] / 100))
                confidence_html = f'<span class="confidence-badge {conf_class}">{conf_level} ({message["confidence"]:.0f}%)</span>'
            
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-header">
                    <span>🤖 Assistant {confidence_html}</span>
                    <span>{message.get("timestamp", "")}</span>
                </div>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Display sources if available
            if message.get("sources"):
                with st.expander(f"📚 View Sources ({len(message['sources'])})"):
                    for source in message["sources"]:
                        st.markdown(f"""
                        <div class="source-card">
                            <div class="source-header">
                                <span>Source #{source['id']}</span>
                                <span style="color: #667eea;">{source['company']}</span>
                            </div>
                            <p>{source['text']}</p>
                            <div class="source-tags">
                                <span class="source-tag">📊 {source['product']}</span>
                                <span class="source-tag">⚠️ {source['issue']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    query = st.chat_input("Ask about financial complaints...")
    
    if query:
        # Add user message
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user",
            "content": query,
            "timestamp": timestamp
        })
        
        # Update stats
        st.session_state.conversation_stats["total_messages"] += 1
        st.session_state.conversation_stats["user_messages"] += 1
        st.session_state.conversation_stats["last_query_time"] = timestamp
        
        # Get collection
        collection = initialize_vector_store()
        
        # Show thinking indicator
        with st.spinner("🤔 Analyzing complaints..."):
            # Get response from RAG
            response, sources = get_rag_response(query, collection)
            
            # Calculate mock confidence
            import random
            confidence = random.uniform(60, 95)
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "sources": sources,
                "confidence": confidence,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # Update stats
            st.session_state.conversation_stats["total_messages"] += 1
            st.session_state.conversation_stats["assistant_messages"] += 1
            st.session_state.conversation_stats["avg_confidence"] = (
                (st.session_state.conversation_stats["avg_confidence"] * 
                 (st.session_state.conversation_stats["assistant_messages"] - 1) + confidence) /
                st.session_state.conversation_stats["assistant_messages"]
            )
        
        st.rerun()

with col2:
    # Sidebar
    st.markdown("### 📊 Dashboard")
    
    # Connection status
    status_color = "#10b981" if st.session_state.vector_store_connected else "#ef4444"
    status_text = "Connected" if st.session_state.vector_store_connected else "Not Connected"
    
    st.markdown(f"""
    <div class="sidebar-section">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="width: 10px; height: 10px; background: {status_color}; border-radius: 50%; margin-right: 0.5rem;"></div>
            <strong>Database Status: {status_text}</strong>
        </div>
        <div style="font-size: 0.9rem; color: #666;">
            Complaints database for AI analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Conversation stats
    stats = st.session_state.conversation_stats
    
    st.markdown("""
    <div class="sidebar-section">
        <h4 style="margin-top: 0;">📈 Conversation Stats</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
            <div class="stats-card">
                <div class="stats-value">{total}</div>
                <div class="stats-label">Total Msgs</div>
            </div>
            <div class="stats-card">
                <div class="stats-value">{user}</div>
                <div class="stats-label">Your Msgs</div>
            </div>
            <div class="stats-card">
                <div class="stats-value">{assistant}</div>
                <div class="stats-label">AI Msgs</div>
            </div>
            <div class="stats-card">
                <div class="stats-value">{confidence:.0f}%</div>
                <div class="stats-label">Avg Confidence</div>
            </div>
        </div>
    </div>
    """.format(
        total=stats["total_messages"],
        user=stats["user_messages"],
        assistant=stats["assistant_messages"],
        confidence=stats["avg_confidence"]
    ), unsafe_allow_html=True)
    
    # Quick questions
    st.markdown("""
    <div class="sidebar-section">
        <h4 style="margin-top: 0;">⚡ Quick Questions</h4>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
    """, unsafe_allow_html=True)
    
    quick_questions = [
        ("💳 Credit card fees", "What are common complaints about credit card fees?"),
        ("🏠 Mortgage delays", "What mortgage processing delays do customers report?"),
        ("💰 Loan issues", "What problems do people have with personal loans?"),
        ("👥 Customer service", "What customer service issues are most frequent?"),
        ("💸 Unauthorized charges", "How do customers report unauthorized transactions?"),
        ("📄 Billing errors", "What billing errors do customers complain about?")
    ]
    
    for icon, question in quick_questions:
        if st.button(f"{icon} {question[:30]}...", key=f"quick_{question}", use_container_width=True):
            # Simulate user input
            st.session_state.messages.append({
                "role": "user",
                "content": question,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tips
    st.markdown("""
    <div class="sidebar-section">
        <h4 style="margin-top: 0;">💡 Tips</h4>
        <div style="font-size: 0.9rem; color: #666;">
            <p>• Ask specific questions</p>
            <p>• Mention financial products</p>
            <p>• Request source evidence</p>
            <p>• Click sources for details</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem; padding: 1rem;">
    Financial Complaints Chat Assistant • Turn-by-turn conversation with source citations • 
    <a href="app_final_clean.py" style="color: #667eea; text-decoration: none;">Switch to Search Interface</a>
</div>
""", unsafe_allow_html=True)