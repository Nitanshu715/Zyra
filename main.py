"""
Zyra - AI Personalized Career and Skills Advisor
Main Application Orchestrator & Dashboard
"""
import streamlit as st
import os
import json
import base64
from datetime import datetime
from auth_landing import login_page, init_session_state, load_user_data, save_user_data
from chat_interface import render_chat_interface
from profile_manager import render_profile_manager
from sidebar_components import render_external_resources_grid

def get_logo_base64():
    try:
        if os.path.exists("logo.png"):
            with open("logo.png", "rb") as f:
                logo_data = f.read()
                return base64.b64encode(logo_data).decode()
        return None
    except:
        return None

def render_app_footer():
    st.markdown("""
    <div style="text-align: center; padding: 2.5rem 0 1rem 0; color: #64748b; font-size: 0.84rem; border-top: 1px solid rgba(255, 255, 255, 0.06); margin-top: 2rem;">
        Made by 
        <a href="https://www.linkedin.com/in/nitanshu-tak-89a1ba289/" target="_blank" style="color: #a5b4fc; text-decoration: none; font-weight: 700; transition: color 0.2s ease;">Nitanshu Tak</a> 
        & 
        <a href="https://www.linkedin.com/in/khushkushwaha45/" target="_blank" style="color: #f472b6; text-decoration: none; font-weight: 700; transition: color 0.2s ease;">Khushi Kushwaha</a>
        <div style="font-size: 0.74rem; color: #475569; margin-top: 4px;">Zyra AI © 2026 • Intelligent Career Strategy Engine</div>
    </div>
    """, unsafe_allow_html=True)

def load_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        box-sizing: border-box;
    }

    .stApp {
        background: #07090e !important;
        background-image: 
            radial-gradient(at 15% 15%, rgba(99, 102, 241, 0.18) 0px, transparent 45%),
            radial-gradient(at 85% 15%, rgba(236, 72, 153, 0.12) 0px, transparent 45%),
            radial-gradient(at 50% 90%, rgba(6, 182, 212, 0.12) 0px, transparent 50%) !important;
        background-attachment: fixed !important;
        color: #f8fafc;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 95% !important;
        width: 95% !important;
    }

    [data-testid="stBottom"],
    .stBottomBlockContainer,
    footer,
    header,
    #MainMenu {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stBottom"] > div {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stChatInput"] {
        background: rgba(15, 23, 42, 0.94) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(25px) !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important;
        padding: 4px 6px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
        font-size: 0.96rem !important;
        background: transparent !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
    }

    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
    }

    /* Top Brand Bar */
    .top-header-bar {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 0.85rem 1.75rem;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .brand-section {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-logo-frame {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #4f46e5, #db2777);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border: 1.5px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
    }

    .brand-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 60%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin: 0;
        line-height: 1.1;
    }

    .user-profile-badge {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(11, 17, 32, 0.85);
        padding: 6px 16px 6px 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .user-avatar-circle {
        width: 32px;
        height: 32px;
        border-radius: 10px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        font-weight: 800;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.4);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 0.9rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
        white-space: nowrap !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6) !important;
    }

    .stButton > button[kind="secondary"] {
        background: rgba(18, 24, 38, 0.85) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(30, 41, 59, 0.95) !important;
        color: #ffffff !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px);
    }

    /* Modern Banner Card */
    .glass-card-panel {
        background: rgba(15, 20, 32, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.75rem 2rem;
        backdrop-filter: blur(25px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        margin-bottom: 1.5rem;
    }

    .panel-header-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: #f8fafc;
        margin: 0 0 0.3rem 0;
    }

    .panel-header-desc {
        color: #94a3b8;
        font-size: 0.92rem;
        margin: 0;
    }

    /* Dynamic Metrics Cards */
    .metric-card-glow {
        background: rgba(15, 20, 32, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 1.6rem 1.4rem;
        text-align: center;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card-glow::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4f46e5, #ec4899);
        opacity: 0.8;
    }

    .metric-card-glow:hover {
        border-color: rgba(99, 102, 241, 0.45);
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), 0 0 20px rgba(99, 102, 241, 0.2);
    }

    .metric-val-lead {
        font-family: 'Outfit', sans-serif;
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }

    .metric-label-lead {
        color: #94a3b8;
        font-size: 0.88rem;
        font-weight: 600;
    }

    /* Skill Item Meter */
    .skill-stat-card {
        background: rgba(11, 17, 32, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }

    .skill-stat-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Zyra - AI Career Advisor", 
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    init_session_state()
    load_global_css()

    if not st.session_state.logged_in:
        login_page()
    else:
        main_dashboard()

def main_dashboard():
    user_data = load_user_data(st.session_state.username)
    if not user_data:
        st.error("Session expired. Please log in again.")
        st.session_state.logged_in = False
        st.rerun()
        return

    user_data['last_active'] = datetime.now().isoformat()
    
    render_header_and_navigation(user_data)
    
    curr_tab = st.session_state.get('current_page', 'chatroom')
    
    if curr_tab == 'chatroom':
        render_chat_interface(user_data)
    elif curr_tab == 'history':
        render_chat_history_view(user_data)
    elif curr_tab == 'profile':
        render_profile_manager(user_data)
    elif curr_tab == 'analytics':
        render_analytics_view(user_data)
    elif curr_tab == 'career':
        render_career_explorer_view(user_data)
    elif curr_tab == 'externals':
        render_externals_view(user_data)
    else:
        render_chat_interface(user_data)

    render_app_footer()
    save_user_data(st.session_state.username, user_data)

def render_header_and_navigation(user_data):
    logo_b64 = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:100%;height:100%;object-fit:cover;" alt="Zyra">' if logo_b64 else '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/></svg>'
    
    profile = user_data.get('profile', {})
    name = profile.get('name', st.session_state.username)
    initial = name[0].upper() if name else 'U'
    level = user_data.get('level', 1)
    xp = user_data.get('xp', 0)

    st.markdown(f"""
    <div class="top-header-bar">
        <div class="brand-section">
            <div class="brand-logo-frame">{logo_html}</div>
            <div>
                <h1 class="brand-title">Zyra AI</h1>
                <div style="font-size: 0.74rem; color: #94a3b8; font-weight: 500;">Career & Skills Advisor</div>
            </div>
        </div>
        <div class="user-profile-badge">
            <div class="user-avatar-circle">{initial}</div>
            <div>
                <div style="font-weight: 700; font-size: 0.84rem; color: #f8fafc;">{name}</div>
                <div style="font-size: 0.72rem; color: #a5b4fc; font-weight: 600;">Level {level} • {xp} XP</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.2, 1.1, 1.3, 1.1, 1.3, 1.1, 0.9])
    current = st.session_state.get('current_page', 'chatroom')

    with col1:
        if st.button("Advisor", key="nav_chat", type="primary" if current == 'chatroom' else "secondary", use_container_width=True):
            st.session_state.current_page = 'chatroom'
            st.rerun()
            
    with col2:
        if st.button("History", key="nav_history", type="primary" if current == 'history' else "secondary", use_container_width=True):
            st.session_state.current_page = 'history'
            st.rerun()
            
    with col3:
        if st.button("Profile & Radar", key="nav_profile", type="primary" if current == 'profile' else "secondary", use_container_width=True):
            st.session_state.current_page = 'profile'
            st.rerun()
            
    with col4:
        if st.button("Analytics", key="nav_analytics", type="primary" if current == 'analytics' else "secondary", use_container_width=True):
            st.session_state.current_page = 'analytics'
            st.rerun()

    with col5:
        if st.button("Career Paths", key="nav_career", type="primary" if current == 'career' else "secondary", use_container_width=True):
            st.session_state.current_page = 'career'
            st.rerun()
            
    with col6:
        if st.button("Resources", key="nav_externals", type="primary" if current == 'externals' else "secondary", use_container_width=True):
            st.session_state.current_page = 'externals'
            st.rerun()

    with col7:
        if st.button("Logout", key="nav_logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = 'chatroom'
            st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

def render_chat_history_view(user_data):
    chat_history = user_data.get('chat_history', [])
    
    st.markdown("""
    <div class="glass-card-panel">
        <h2 class="panel-header-title">Conversation Archive</h2>
        <p class="panel-header-desc">Search and review all your previous career consultations with Zyra.</p>
    </div>
    """, unsafe_allow_html=True)

    if not chat_history:
        st.markdown("""
        <div style="background: rgba(15, 20, 32, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 3.5rem 2rem; text-align: center; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);">
            <div style="width: 60px; height: 60px; margin: 0 auto 1.25rem auto; border-radius: 18px; background: rgba(99, 102, 241, 0.12); border: 1.5px solid rgba(99, 102, 241, 0.3); display: flex; align-items: center; justify-content: center; color: #818cf8;">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            </div>
            <h3 style="font-family: Outfit, sans-serif; font-size: 1.5rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.4rem;">
                No Prior Consultations Recorded
            </h3>
            <p style="color: #94a3b8; font-size: 0.95rem; max-width: 480px; margin: 0 auto 1.5rem auto; line-height: 1.5;">
                Start your first interactive session with Zyra to explore custom roadmaps, conduct mock interviews, or evaluate your resume.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        col_c1, col_c2, col_c3 = st.columns([1.5, 1, 1.5])
        with col_c2:
            if st.button("Start Consultation →", key="btn_start_history", type="primary", use_container_width=True):
                st.session_state.current_page = 'chatroom'
                st.rerun()
        return

    col_search, col_clear = st.columns([4, 1.2])
    with col_search:
        search_query = st.text_input("Search conversations...", placeholder="Search keywords (e.g. interview, python, salary)")
    with col_clear:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Clear History", type="secondary", use_container_width=True):
            user_data['chat_history'] = []
            save_user_data(st.session_state.username, user_data)
            st.success("History cleared.")
            st.rerun()

    conversations = []
    curr = []
    for msg in chat_history:
        curr.append(msg)
        if msg.get('sender') == 'bot' and len(curr) >= 2:
            conversations.append(curr)
            curr = []

    if curr:
        conversations.append(curr)

    filtered = [c for c in reversed(conversations) if not search_query or any(search_query.lower() in m.get('content', '').lower() for m in c)]

    if not filtered:
        st.warning(f"No conversations matched '{search_query}'.")
        return

    for idx, convo in enumerate(filtered):
        u_msg = next((m for m in convo if m.get('sender') == 'user'), None)
        b_msg = next((m for m in convo if m.get('sender') == 'bot'), None)
        
        preview = u_msg['content'][:75] + "..." if u_msg else "Career Consultation"
        ts = u_msg.get('timestamp', '') if u_msg else ''
        time_str = ""
        try:
            if ts:
                time_str = datetime.fromisoformat(ts).strftime("%b %d, %Y • %I:%M %p")
        except:
            time_str = "Recent"

        with st.expander(f"{preview}  —  {time_str}"):
            if u_msg:
                st.markdown(f"**You:**\n\n{u_msg['content']}")
            if b_msg:
                st.markdown(f"**Zyra:**\n\n{b_msg['content']}")

def render_analytics_view(user_data):
    st.markdown("""
    <div class="glass-card-panel">
        <h2 class="panel-header-title">Learning & Skill Analytics</h2>
        <p class="panel-header-desc">Track your mentoring momentum, technical skill progression, and career milestones.</p>
    </div>
    """, unsafe_allow_html=True)

    chat_count = len(user_data.get('chat_history', []))
    xp = user_data.get('xp', 0)
    level = user_data.get('level', 1)
    badges_count = len(user_data.get('badges', []))
    completed_goals = len(user_data.get('goals_tracking', {}).get('completed', []))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card-glow">
            <div class="metric-val-lead">{chat_count}</div>
            <div class="metric-label-lead">Total Consultations</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card-glow">
            <div class="metric-val-lead">Lvl {level}</div>
            <div class="metric-label-lead">{xp} Experience Points</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card-glow">
            <div class="metric-val-lead">{completed_goals}</div>
            <div class="metric-label-lead">Goals Completed</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card-glow">
            <div class="metric-val-lead">{badges_count}</div>
            <div class="metric-label-lead">Badges Earned</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    tech_skills = user_data.get('skills', {}).get('technical', {})
    if tech_skills:
        st.markdown("""
        <div style="background: rgba(15, 20, 32, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.75rem 2rem; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4); margin-bottom: 1.5rem;">
            <h3 style="font-family: Outfit, sans-serif; color: #f8fafc; font-size: 1.35rem; font-weight: 800; margin-bottom: 1.25rem;">
                Technical Skill Mastery Breakdown
            </h3>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        skills_list = list(tech_skills.items())
        for i, (sk, v) in enumerate(skills_list):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="skill-stat-card">
                    <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.92rem; color: #f1f5f9; margin-bottom: 0.5rem;">
                        <span>{sk}</span>
                        <span style="color: #818cf8; font-weight: 800;">{v}%</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.08); border-radius: 8px; height: 7px; overflow:hidden;">
                        <div style="background: linear-gradient(90deg, #4f46e5, #db2777); width: {v}%; height: 100%; border-radius: 8px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_career_explorer_view(user_data):
    st.markdown("""
    <div class="glass-card-panel">
        <h2 class="panel-header-title">Emerging Career Pathways</h2>
        <p class="panel-header-desc">Explore in-demand roles, Indian compensation benchmarks (₹ LPA), and skill roadmaps.</p>
    </div>
    """, unsafe_allow_html=True)

    careers = [
        {
            "role": "AI / ML Engineer",
            "salary": "₹8 - ₹28 LPA",
            "demand": "High Growth",
            "skills": ["Python", "PyTorch/TensorFlow", "LLMs & RAG", "Data Pipelines"],
            "desc": "Architect, fine-tune, and deploy predictive models and generative AI systems into production."
        },
        {
            "role": "Full-Stack Software Engineer",
            "salary": "₹7 - ₹22 LPA",
            "demand": "Very High",
            "skills": ["React/Next.js", "Node/Python/Go", "PostgreSQL", "Cloud Architecture"],
            "desc": "Build scalable web applications from interactive user experiences to distributed backend services."
        },
        {
            "role": "Data Scientist & Analytics Lead",
            "salary": "₹8 - ₹24 LPA",
            "demand": "In-Demand",
            "skills": ["Python", "SQL & BigQuery", "Statistical Modeling", "Machine Learning"],
            "desc": "Transform data into strategic intelligence, optimization models, and automated business decisions."
        },
        {
            "role": "Cloud & DevOps Architect",
            "salary": "₹9 - ₹26 LPA",
            "demand": "High Demand",
            "skills": ["AWS/GCP/Azure", "Docker & Kubernetes", "CI/CD", "Terraform"],
            "desc": "Design automated, resilient, and highly secure cloud infrastructure for modern enterprise systems."
        }
    ]

    c_col1, c_col2 = st.columns(2)
    for i, c in enumerate(careers):
        with c_col1 if i % 2 == 0 else c_col2:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 18px; padding: 1.5rem; margin-bottom: 1.25rem; backdrop-filter: blur(20px); box-shadow: 0 10px 30px rgba(0,0,0,0.35);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                    <h3 style="color: #f8fafc; font-size: 1.2rem; font-weight: 800; margin: 0;">{c['role']}</h3>
                    <span style="background: rgba(236, 72, 153, 0.18); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.3); padding: 3px 10px; border-radius: 10px; font-size: 0.75rem; font-weight: 700;">{c['demand']}</span>
                </div>
                <div style="color: #34d399; font-weight: 800; font-size: 1.05rem; margin-bottom: 0.75rem;">{c['salary']}</div>
                <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.5; margin-bottom: 1rem;">{c['desc']}</p>
                <div style="margin-bottom: 1rem;">
                    {"".join([f'<span style="display:inline-block; background:rgba(11,17,32,0.9); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:3px 10px; border-radius:8px; font-size:0.78rem; font-weight:500; margin:2px 4px 2px 0;">{sk}</span>' for sk in c['skills']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Generate Roadmap for {c['role']}", key=f"btn_ask_{i}", type="secondary", use_container_width=True):
                st.session_state.current_page = 'chatroom'
                user_data.setdefault('chat_history', []).append({
                    'sender': 'user',
                    'content': f"Can you give me a personalized roadmap to become a {c['role']} based on my current skills?",
                    'timestamp': datetime.now().isoformat()
                })
                from chat_interface import process_chat_message
                process_chat_message(f"Can you give me a personalized roadmap to become a {c['role']} based on my current skills?", user_data)
                st.rerun()

def render_externals_view(user_data):
    st.markdown("""
    <div class="glass-card-panel">
        <h2 class="panel-header-title">Career & Learning Resources</h2>
        <p class="panel-header-desc">Curated platforms for job search, AI resume reviews, coding practice, and design.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_external_resources_grid()

if __name__ == "__main__":
    main()
