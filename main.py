"""
Redesigned Zyra AI Career Advisor
Modern UI with clean top navigation and streamlined layout
"""
import streamlit as st
from auth_landing import login_page, init_session_state, load_user_data
from chat_interface import render_chat_interface
from profile_manager import render_profile_manager
import os
import base64


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Zyra - AI Career Advisor", 
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    init_session_state()
    
    # Initialize externals modal state
    if 'show_externals' not in st.session_state:
        st.session_state.show_externals = False
    
    # Route to appropriate page
    if not st.session_state.logged_in:
        login_page()
    else:
        main_dashboard()

def main_dashboard():
    """Main dashboard with clean unified layout"""
    user_data = load_user_data(st.session_state.username)
    
    if not user_data:
        st.error("User data not found. Please login again.")
        st.session_state.logged_in = False
        st.rerun()
        return
    
    # Update user activity
    from datetime import datetime
    user_data['last_active'] = datetime.now().isoformat()
    
    # Render unified top navigation with welcome
    render_unified_header(user_data)
    
    # Render externals modal if open (before main content)
    if st.session_state.get('show_externals', False):
        render_externals_modal()
    
    # Main content area
    render_main_content(user_data)
    
    # Render floating logout button
    render_floating_logout()
    
    # Save updated user data
    from auth_landing import save_user_data
    save_user_data(st.session_state.username, user_data)

def render_unified_header(user_data):
    """Render clean unified header with navigation and welcome"""
    st.markdown("""
    <style>
    .unified-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        border-radius: 0 0 25px 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        position: relative;
    }
    .welcome-section {
        flex: 1;
    }
    .welcome-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.5rem 0;
    }
    .welcome-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0;
    }
    .logo-container {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        z-index: 10;
    }
    .logo-image {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.6), 
                    0 0 60px rgba(102, 126, 234, 0.4),
                    0 0 90px rgba(102, 126, 234, 0.2);
        animation: logoGlow 3s ease-in-out infinite alternate;
        transition: all 0.3s ease;
    }
    .logo-image:hover {
        transform: scale(1.1);
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.8), 
                    0 0 80px rgba(102, 126, 234, 0.6),
                    0 0 120px rgba(102, 126, 234, 0.4);
    }
    @keyframes logoGlow {
        0% {
            box-shadow: 0 0 30px rgba(102, 126, 234, 0.6), 
                        0 0 60px rgba(102, 126, 234, 0.4),
                        0 0 90px rgba(102, 126, 234, 0.2);
        }
        100% {
            box-shadow: 0 0 40px rgba(102, 126, 234, 0.8), 
                        0 0 80px rgba(102, 126, 234, 0.6),
                        0 0 120px rgba(102, 126, 234, 0.4);
        }
    }
    .user-profile {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(102, 126, 234, 0.1);
        padding: 0.75rem 1.25rem;
        border-radius: 18px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    .user-profile:hover {
        background: rgba(102, 126, 234, 0.15);
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    .user-avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 1.3rem;
    }
    .user-info {
        display: flex;
        flex-direction: column;
    }
    .user-name {
        font-weight: 600;
        color: #2d3748;
        margin: 0;
        font-size: 1.1rem;
    }
    .user-level {
        font-size: 0.85rem;
        color: #718096;
        margin: 0;
    }
    /* Fixed hover effects for buttons - removed harsh shadow */
    .stButton > button {
        background: transparent !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        color: #4a5568 !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.25rem !important;
        margin: 0 0.5rem !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border-color: transparent !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4) !important;
    }
    .stButton > button:focus {
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4) !important;
        outline: none !important;
    }
    /* Remove default streamlit button focus ring */
    .stButton > button:focus:not(:focus-visible) {
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4) !important;
    }
    /* Enhanced floating logout button with glow */
    .floating-logout-btn {
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        z-index: 1000 !important;
        background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 65px !important;
        height: 65px !important;
        font-size: 1.6rem !important;
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.6), 0 4px 20px rgba(220, 38, 38, 0.4) !important;
        transition: all 0.3s ease !important;
        padding: 0 !important;
        margin: 0 !important;
        animation: floatingGlow 3s ease-in-out infinite !important;
        cursor: pointer !important;
    }
    @keyframes floatingGlow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(220, 38, 38, 0.6), 0 4px 20px rgba(220, 38, 38, 0.4);
            transform: translateY(0);
        }
        50% {
            box-shadow: 0 0 30px rgba(220, 38, 38, 0.8), 0 8px 25px rgba(220, 38, 38, 0.5);
            transform: translateY(-2px);
        }
    }
        .grid-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* 4 columns */
    gap: 20px; /* space between cards */
    padding: 20px;
    }

    .card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .floating-logout-btn:hover {
        transform: translateY(-5px) scale(1.1) !important;
        box-shadow: 0 0 40px rgba(220, 38, 38, 0.9), 0 10px 30px rgba(220, 38, 38, 0.6) !important;
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: white !important;
        animation: none !important;
    }
    /* Externals modal styles */
    .externals-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(5px);
    }
    .externals-content {
        background: white;
        border-radius: 25px;
        padding: 2rem;
        max-width: 900px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        position: relative;
    }
    .externals-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .externals-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .externals-subtitle {
        color: #64748b;
        font-size: 1.1rem;
    }
    .external-cards-grid {
    display: grid;
    grid-template-columns: repeat(4, 220px); /* 4 cards in each row */
    grid-template-rows: repeat(2, auto);    /* 2 rows */
    gap: 1.5rem;
    margin-top: 2rem;
    justify-content: center; /* center the whole grid */
    align-items: start;
}
    .external-card {
    width: 220px;
    min-height: 200px;
    background: #fff;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    box-shadow: 0 2px 12px rgba(0,0,0,0.09);
    border: 1.5px solid #f3f4f6;
}


    .external-card:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 10px 32px rgba(102, 126, 234, 0.13);
        border-color: #a5b4fc;
    }
    .external-card-img-row {
        width: 100%;
        height: 120px;
        overflow: hidden;
        border-radius: 18px 18px 0 0;
        display: block;
        background: #f3f4f6;
        position: relative;
    }
    .external-card-img-row img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 18px 18px 0 0;
        background: #fff;
        display: block;
    }
    .external-card-title-row {
        font-size: 1.1rem;
        font-weight: 600;
        color: #212529;
        margin: 1rem 1rem 1rem 1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    /* Circle container */
.logo-circle {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden; /* keeps image inside circle */
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 20px rgba(76, 175, 80, 0.8),
                0 0 40px rgba(76, 175, 80, 0.6),
                0 0 60px rgba(76, 175, 80, 0.4);
}

/* Image fills the circle */
.logo-circle img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* crop edges, fills circle */
}

    
    /* force all images inside logo container */
.logo-image img,
.stImage img {
    width: 100% !important;   /* fills circle */
    height: 100% !important;
    object-fit: cover !important; /* zooms to fill instead of leaving gaps */
}
    </style>
    """, unsafe_allow_html=True)
    
    # Unified header HTML
    current_page = st.session_state.get('current_page', 'chatroom')
    user_initial = user_data['profile']['name'][0].upper() if user_data['profile']['name'] else 'U'
    user_name = user_data['profile']['name']
    
    st.markdown(f"""
    <div class="unified-header">
        <div class="header-container">
            <div class="welcome-section">
                <div class="welcome-title">Welcome to Zyra! 👋</div>
                <div class="welcome-subtitle">Hi, {user_name}! Ready to map your future?</div>
            </div>
            <div class="user-profile">
                <div class="user-avatar">{user_initial}</div>
                <div class="user-info">
                    <div class="user-name">{user_data['profile']['name']}</div>
                    <div class="user-level">Level {user_data.get('level', 1)} • {user_data.get('xp', 0)} XP</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons in a single row - replaced logout with externals
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    
    with col1:
        if st.button("Chatroom", key="nav_chatroom"):
            st.session_state.current_page = 'chatroom'
            st.rerun()
    
    with col2:
        if st.button("Chat History", key="nav_history"):
            st.session_state.current_page = 'history'
            st.rerun()
    
    with col3:
        if st.button("Profile", key="nav_profile"):
            st.session_state.current_page = 'profile'
            st.rerun()
    
    with col4:
        if st.button("Analytics", key="nav_analytics"):
            st.session_state.current_page = 'analytics'
            st.rerun()
    
    with col5:
        if st.button("Career", key="nav_career"):
            st.session_state.current_page = 'career'
            st.rerun()
    
    with col6:
        if st.button("Externals", key="nav_externals"):
            st.session_state.show_externals = True
            st.rerun()

def render_floating_logout():
    """Render floating logout button in bottom right with enhanced glow"""
    logout_js = """
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000;">
        <button class="floating-logout-btn" onclick="logoutUser()" title="Logout">
            🚪
        </button>
    </div>
    <script>
    function logoutUser() {
        const logoutBtn = document.querySelector('button[data-testid="logout-btn"]');
        if (logoutBtn) {
            logoutBtn.click();
        }
    }
    </script>
    """

def render_floating_logout():
    """Render floating logout button in bottom right with enhanced glow"""
    logout_js = """
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000;">
        <button class="floating-logout-btn" onclick="logoutUser()" title="Logout">
            🚪
        </button>
    </div>
    <script>
    function logoutUser() {
        const logoutBtn = document.querySelector('button[data-testid="logout-btn"]');
        if (logoutBtn) {
            logoutBtn.click();
        }
    }
    </script>
    """
def get_image_base64(image_path):
    """Load image and convert to base64"""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                img_data = f.read()
            return base64.b64encode(img_data).decode()
        return None
    except:
        return None

def render_externals_modal():
    """Render externals modal with compact 4x2 card grid, less spacing"""
    external_tools = [
        {"name": "Resume Review", "url": "https://resumeworded.com/", "img": "resume.jpg"},
        {"name": "LinkedIn", "url": "https://linkedin.com/", "img": "linkedin.png"},
        {"name": "GitHub", "url": "https://github.com/", "img": "github.jpg"},
        {"name": "Job Search", "url": "https://naukri.com/", "img": "naukri.png"},
        {"name": "YouTube", "url": "https://youtube.com/", "img": "youtube.jpg"},
        {"name": "Canva", "url": "https://canva.com/", "img": "canva.jpg"},
        {"name": "GeeksforGeeks", "url": "https://geeksforgeeks.org/", "img": "gfg.png"},
        {"name": "Miro Sticky Notes", "url": "https://miro.com/online-sticky-notes/", "img": "notes.jpg"}
    ]

    # Close button row - push further right
    col1, col2, col3, col4 = st.columns([10, 1, 0.3, 0.7])
    with col4:
        if st.button("❌", key="close_externals_btn", help="Close"):
            st.session_state.show_externals = False
            st.rerun()

    idx = 0
    total = len(external_tools)

    # Grid
    for _row in range(2):  # 2 rows
        cols = st.columns([1, 1, 1, 1], gap="small")
        for c in range(4):
            with cols[c]:
                if idx < total:
                    tool = external_tools[idx]
                    
                    # Get image as base64
                    img_path = os.path.join("photos", tool['img'])
                    img_b64 = get_image_base64(img_path)
                    
                    if img_b64:
                        img_html = f'<img src="data:image/jpeg;base64,{img_b64}" alt="{tool["name"]}" style="width:100%;height:100%;object-fit:cover;display:block;">'
                    else:
                        # Fallback gradient if image not found
                        img_html = f'<div style="width:100%;height:100%;background:linear-gradient(135deg, #667eea, #764ba2);display:flex;align-items:center;justify-content:center;color:white;font-size:24px;">📱</div>'
                    
                    card_html = f"""
                    <a href="{tool['url']}" target="_blank" style="text-decoration:none;">
                      <div style="
                        width:100%;
                        min-height:200px;
                        border-radius:10px;
                        background:#fff;
                        border:1px solid #ddd;
                        box-shadow:0 4px 10px rgba(0,0,0,0.05);
                        overflow:hidden;
                        margin:4px 2px 14px 2px;
                      ">
                        <div style="height:210px;width:100%;background:#f3f4f6;overflow:hidden;">
                          {img_html}
                        </div>
                        <div style="padding:8px 8px;font-weight:600;font-size:14px;color:#111;text-align:center;">
                          {tool['name']}
                        </div>
                      </div>
                    </a>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                idx += 1

    # Close the grid
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
def render_main_content(user_data):
    current_page = st.session_state.get('current_page', 'chatroom')
    if current_page == 'chatroom':
        render_chat_interface(user_data)
    elif current_page == 'history':
        render_chat_history_page(user_data)
    elif current_page == 'profile':
        render_profile_manager(user_data)
    elif current_page == 'analytics':
        render_analytics_page(user_data)
    elif current_page == 'career':
        render_career_page(user_data)
    else:
        render_chat_interface(user_data)

def render_chat_history_page(user_data):
    st.markdown("""
    <style>
    .history-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
    }
    .history-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    .history-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .conversation-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    .conversation-preview {
        color: #4a5568;
        font-size: 0.95rem;
        margin: 0.5rem 0;
        line-height: 1.5;
    }
    .conversation-time {
        color: #718096;
        font-size: 0.85rem;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    st.markdown('''
    <div class="history-header">
        <div class="history-title">Your Chat History</div>
        <p style="color: #64748b; font-size: 1.1rem;">Review your previous conversations with Zyra</p>
    </div>
    ''', unsafe_allow_html=True)
    chat_history = user_data.get('chat_history', [])
    if not chat_history:
        st.info("No chat history yet. Start a conversation in the Chatroom to see your history here!")
        if st.button("Go to Chatroom", type="primary"):
            st.session_state.current_page = 'chatroom'
            st.rerun()
    else:
        conversations = []
        current_conversation = []
        for message in chat_history:
            current_conversation.append(message)
            if message['sender'] == 'bot' and len(current_conversation) >= 2:
                conversations.append(current_conversation.copy())
                current_conversation = []
        for i, conversation in enumerate(reversed(conversations)):
            if len(conversation) >= 2:
                user_msg = conversation[0] if conversation[0]['sender'] == 'user' else conversation[1]
                bot_msg = conversation[1] if conversation[1]['sender'] == 'bot' else conversation[0]
                with st.expander(f"Conversation {len(conversations)-i}: {user_msg['content'][:60]}..."):
                    st.markdown(f'''
                    <div class="conversation-card">
                        <strong>You:</strong>
                        <div class="conversation-preview">{user_msg['content']}</div>
                        <br>
                        <strong>Zyra:</strong>
                        <div class="conversation-preview">{bot_msg['content']}</div>
                        <div class="conversation-time">
                            {format_timestamp(user_msg.get('timestamp', ''))}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Clear All History", type="secondary"):
                user_data['chat_history'] = []
                from auth_landing import save_user_data
                save_user_data(st.session_state.username, user_data)
                st.success("Chat history cleared!")
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def format_timestamp(timestamp_str):
    try:
        if timestamp_str:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime('%B %d, %Y at %I:%M %p')
        return 'Recently'
    except:
        return 'Recently'

def render_analytics_page(user_data):
    st.markdown("""
    <style>
    .analytics-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    .analytics-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    .analytics-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        color: #718096;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="analytics-container">', unsafe_allow_html=True)
    st.markdown('''
    <div class="analytics-header">
        <h1 class="analytics-title">Your Analytics</h1>
        <p style="color: #718096; font-size: 1.1rem;">Track your career development journey</p>
    </div>
    ''', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(user_data.get('chat_history', []))}</div>
            <div class="metric-label">Total Conversations</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{user_data.get('level', 1)}</div>
            <div class="metric-label">Current Level</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{len(user_data.get('badges', []))}</div>
            <div class="metric-label">Badges Earned</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_career_page(user_data):
    st.markdown("""
    <style>
    .career-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    .career-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    .career-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .career-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    .career-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .career-card:hover {
        transform: translateY(-5px);
    }
    .career-card h3 {
        color: #2d3748;
        margin-bottom: 1rem;
    }
    .salary-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="career-container">', unsafe_allow_html=True)
    st.markdown('''
    <div class="career-header">
        <h1 class="career-title">Career Guidance</h1>
        <p style="color: #718096; font-size: 1.1rem;">Explore trending career paths and opportunities</p>
    </div>
    ''', unsafe_allow_html=True)
    careers = [
        {
            "title": "Software Development",
            "salary": "₹4-15 LPA",
            "skills": "Python, JavaScript, React, SQL",
            "growth": "Very High"
        },
        {
            "title": "Data Science",
            "salary": "₹6-20 LPA", 
            "skills": "Python, SQL, Machine Learning, Statistics",
            "growth": "Extremely High"
        },
        {
            "title": "Cloud Engineering",
            "salary": "₹5-18 LPA",
            "skills": "AWS, Docker, Kubernetes, Linux",
            "growth": "High"
        },
        {
            "title": "Product Management",
            "salary": "₹8-25 LPA",
            "skills": "Strategy, Analytics, Communication",
            "growth": "Very High"
        }
    ]
    col1, col2 = st.columns(2)
    for i, career in enumerate(careers):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f'''
            <div class="career-card">
                <h3>{career["title"]}</h3>
                <div class="salary-badge">{career["salary"]}</div>
                <p><strong>Skills:</strong> {career["skills"]}</p>
                <p><strong>Growth:</strong> {career["growth"]}</p>
            </div>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <h3 style="color: #4a5568; margin-bottom: 1rem;">Get Personalized Career Advice</h3>
        <p style="color: #718096;">Ask me about specific career paths, skills to learn, or job market trends!</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💬 Start Chat", type="primary", key="go_to_chat"):
        st.session_state.current_page = 'chatroom'
        st.rerun()

if __name__ == "__main__":
    main()
