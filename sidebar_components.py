"""
Clean Navigation Bar Components for Zyra AI Career Advisor
Simple navigation with external links and basic functionality
"""
import streamlit as st
import time
from datetime import datetime
from auth_landing import save_users, load_users

def load_sidebar_css():
    """Clean CSS for Navigationbar"""
    st.markdown("""
    <style>
    .sidebar-logo {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 30px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nav-section {
        margin: 20px 0;
        padding: 15px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .nav-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
        margin-bottom: 15px;
        opacity: 0.9;
    }
    
    .user-info {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        color: white;
        text-align: center;
    }
    
    .user-name {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .user-stats {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .external-link {
        display: block;
        width: 100%;
        padding: 10px 15px;
        margin: 5px 0;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        text-decoration: none;
        border-radius: 8px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .external-link:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        text-decoration: none;
        color: white;
    }
    
    .chat-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        font-size: 0.9rem;
    }
    
    .chat-item:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        width: 100% !important;
        margin: 5px 0 !important;
        padding: 10px 15px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar(user_data, users):
    """Render clean sidebar with navigation"""
    load_sidebar_css()
    
    with st.sidebar:
        # Logo
        st.markdown('<div class="sidebar-logo">Zyra</div>', unsafe_allow_html=True)
        
        # User Info
        st.markdown(f'''
        <div class="user-info">
            <div class="user-name">{user_data["profile"]["name"]}</div>
            <div class="user-stats">
                Level {user_data.get("level", 1)} • {user_data.get("xp", 0)} XP
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Navigation Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">Navigation</div>', unsafe_allow_html=True)
        
        # Navigation buttons
        if st.button("Chat", key="nav_chat"):
            st.session_state.current_page = 'chat'
            st.rerun()
            
        if st.button("Profile", key="nav_profile"):
            st.session_state.current_page = 'profile'
            st.rerun()
            
        if st.button("Analytics", key="nav_analytics"):
            st.session_state.current_page = 'analytics'
            st.rerun()
            
        if st.button("Career", key="nav_career"):
            st.session_state.current_page = 'career'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # External Links Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">External Tools</div>', unsafe_allow_html=True)
        
        # Resume Review Link
        st.markdown('''
        <a href="https://resumeworded.com/" target="_blank" class="external-link">
            Resume Review
        </a>
        ''', unsafe_allow_html=True)
        
        # LinkedIn Link
        st.markdown('''
        <a href="https://linkedin.com/" target="_blank" class="external-link">
            LinkedIn
        </a>
        ''', unsafe_allow_html=True)
        
        # GitHub Link
        st.markdown('''
        <a href="https://github.com/" target="_blank" class="external-link">
            GitHub
        </a>
        ''', unsafe_allow_html=True)
        
        # Job Search Link
        st.markdown('''
        <a href="https://naukri.com/" target="_blank" class="external-link">
            Job Search
        </a>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Previous Chats Section
        if user_data.get('chat_history'):
            st.markdown('<div class="nav-section">', unsafe_allow_html=True)
            st.markdown('<div class="nav-title">Recent Chats</div>', unsafe_allow_html=True)
            
            # Get unique chat topics (first message from user in each conversation)
            user_messages = [msg for msg in user_data['chat_history'] if msg['sender'] == 'user']
            recent_chats = user_messages[-5:]  # Last 5 user messages
            
            for i, chat in enumerate(reversed(recent_chats)):
                chat_preview = chat['content'][:30] + "..." if len(chat['content']) > 30 else chat['content']
                st.markdown(f'''
                <div class="chat-item" title="{chat['content']}">
                    💬 {chat_preview}
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Stats Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">Quick Stats</div>', unsafe_allow_html=True)
        
        total_chats = len(user_data.get('chat_history', []))
        badges_count = len(user_data.get('badges', []))
        
        st.markdown(f'''
        <div style="color: white; font-size: 0.9rem; line-height: 1.6;">
            <div>Total Conversations: {total_chats}</div>
            <div>Badges Earned: {badges_count}</div>
            <div>Current Level: {user_data.get('level', 1)}</div>
            <div>Experience Points: {user_data.get('xp', 0)}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Settings Section
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">Settings</div>', unsafe_allow_html=True)
        
        # Clear chat history
        if st.button("🗑️ Clear All Chats", key="clear_all"):
            if st.session_state.get('confirm_clear'):
                user_data['chat_history'] = []
                users[st.session_state.username] = user_data
                save_users(users)
                st.session_state.confirm_clear = False
                st.success("All chats cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm deletion!")
        
        # Export data
        if st.button("Export Data", key="export_data"):
            export_user_data(user_data)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Logout Section
        st.markdown("---")
        if st.button("Logout", key="logout", type="primary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = 'chat'
            st.success("Logged out successfully!")
            time.sleep(1)
            st.rerun()

def export_user_data(user_data):
    """Export user data as downloadable file"""
    import json
    
    # Prepare export data
    export_data = {
        'profile': user_data.get('profile', {}),
        'chat_history': user_data.get('chat_history', []),
        'stats': {
            'level': user_data.get('level', 1),
            'xp': user_data.get('xp', 0),
            'badges': user_data.get('badges', [])
        },
        'export_date': datetime.now().isoformat()
    }
    
    # Convert to JSON
    json_data = json.dumps(export_data, indent=2, ensure_ascii=False, default=str)
    
    st.download_button(
        label="📥 Download Your Data",
        data=json_data,
        file_name=f"zyra_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"

    )
