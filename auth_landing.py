import streamlit as st
import json
import os
import hashlib
import time
import base64
from datetime import datetime

# ---- USER DATA PERSISTENCE ----
def get_user_filename(username):
    safe_username = "".join(c for c in username if c.isalnum() or c in ('_', '-')).lower()
    return f"user_{safe_username}.json"

def load_user_data(username):
    if not username:
        return None
    filename = get_user_filename(username)
    try:
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        return None

def save_user_data(username, user_data):
    if not username:
        return False
    filename = get_user_filename(username)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        st.error(f"Error saving user data: {e}")
        return False

def user_exists(username):
    filename = get_user_filename(username)
    return os.path.exists(filename)

def create_user_account(username, password):
    if user_exists(username):
        return False, "Username already exists. Please pick another."
    user_data = init_user_data(username)
    user_data['password'] = hash_password(password)
    if save_user_data(username, user_data):
        return True, "Account created successfully."
    else:
        return False, "Error creating account."

def verify_user_login(username, password):
    user_data = load_user_data(username)
    if user_data and user_data.get('password') == hash_password(password):
        return True, user_data
    return False, None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_user_data(username):
    return {
        'username': username,
        'password': '',
        'created_at': datetime.now().isoformat(),
        'profile': {
            'name': username.title(),
            'current_role': 'Student / Job Seeker',
            'experience_level': 'Beginner',
            'location': 'India',
            'education': 'Computer Science / Engineering',
            'preferred_work_type': 'Remote',
            'availability': 'Immediate',
            'bio': 'Passionate builder exploring tech roles and modern AI skills.',
            'goal': 'Become an AI / Software Engineer',
            'interests': ['Web Development', 'Artificial Intelligence', 'Cloud & DevOps'],
            'completion': 50
        },
        'skills': {
            'technical': {
                'Python': 75,
                'SQL': 65,
                'JavaScript': 60,
                'React': 45,
                'Machine Learning': 40,
                'Git': 70
            },
            'soft': {
                'Communication': 80,
                'Problem Solving': 80,
                'Teamwork': 85,
                'Leadership': 60,
                'Time Management': 70,
                'Adaptability': 80
            }
        },
        'goals_tracking': {
            'short_term': [
                {'goal': 'Master Python & DSA Problem Solving', 'created_date': datetime.now().isoformat()},
                {'goal': 'Build Full-Stack AI Portfolio App', 'created_date': datetime.now().isoformat()}
            ],
            'long_term': [
                {'goal': 'Land a ₹15+ LPA Tech Role', 'created_date': datetime.now().isoformat()}
            ],
            'completed': []
        },
        'chat_history': [],
        'xp': 100,
        'level': 1,
        'badges': ['New Member', 'First Step'],
        'streak': 1,
        'last_active': datetime.now().isoformat()
    }

def get_logo_base64():
    try:
        if os.path.exists("logo.png"):
            with open("logo.png", "rb") as f:
                logo_data = f.read()
                return base64.b64encode(logo_data).decode()
        return None
    except:
        return None

def load_auth_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800;900&display=swap');

    body, p, h1, h2, h3, h4, h5, h6, input, button {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #07090e !important;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.18) 0%, transparent 55%),
            radial-gradient(circle at 85% 70%, rgba(236, 72, 153, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 50% 90%, rgba(6, 182, 212, 0.12) 0%, transparent 50%) !important;
        background-attachment: fixed !important;
        color: #f8fafc;
    }

    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1050px !important;
        margin: 0 auto !important;
    }

    @keyframes coinSpin3D {
        0% { transform: perspective(1000px) rotateY(0deg) translateY(0px); }
        25% { transform: perspective(1000px) rotateY(90deg) translateY(-8px); }
        50% { transform: perspective(1000px) rotateY(180deg) translateY(0px); }
        75% { transform: perspective(1000px) rotateY(270deg) translateY(-8px); }
        100% { transform: perspective(1000px) rotateY(360deg) translateY(0px); }
    }

    @keyframes floatHero {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .mascot-hero-panel {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2.5rem 1.5rem;
        animation: floatHero 5s ease-in-out infinite;
    }

    .coin-3d-wrapper {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        border: 4px solid rgba(255, 255, 255, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        animation: coinSpin3D 8s linear infinite;
        overflow: hidden;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.5), 0 0 60px rgba(236, 72, 153, 0.3);
    }

    .coin-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
    }

    .welcome-lead {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        line-height: 1.15;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.75rem;
    }

    .welcome-desc {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.6;
        max-width: 380px;
        margin-bottom: 1.5rem;
    }

    .feature-tag-row {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 100%;
        max-width: 340px;
    }

    .feature-tag-item {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #cbd5e1;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: left;
    }

    /* Modern Glass Card */
    [data-testid="stForm"] {
        background: rgba(15, 20, 32, 0.85) !important;
        backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 2.2rem !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7), 0 0 30px rgba(99, 102, 241, 0.12) !important;
    }

    .form-heading-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        color: #f8fafc;
        margin-bottom: 0.3rem;
    }

    .form-heading-sub {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-bottom: 1.5rem;
    }

    /* Sleek Rounded Pill Switcher */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        width: 100% !important;
        gap: 6px !important;
        background: rgba(8, 12, 20, 0.9) !important;
        border-radius: 9999px !important;
        padding: 5px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin-bottom: 1.5rem !important;
    }

    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center !important;
        justify-content: center !important;
        background: transparent !important;
        border-radius: 9999px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 9px 0 !important;
        border: none !important;
        transition: all 0.25s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
    }

    /* Remove Ugly Instructions / "Press Enter to submit form" */
    [data-testid="InputInstructions"],
    .stTextInput [data-testid="InputInstructions"],
    .stPasswordInput [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* Deep Input Fixes */
    [data-baseweb="base-input"],
    [data-baseweb="input"] {
        background: rgba(9, 13, 22, 0.95) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
        transition: all 0.2s ease !important;
    }

    [data-baseweb="base-input"]:focus-within,
    [data-baseweb="input"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    }

    .stTextInput input,
    .stPasswordInput input {
        background: transparent !important;
        border: none !important;
        color: #f8fafc !important;
        font-size: 0.95rem !important;
        padding: 0.8rem 1rem !important;
        box-shadow: none !important;
    }

    .stTextInput input::placeholder,
    .stPasswordInput input::placeholder {
        color: #64748b !important;
    }

    /* Restore Material Icons for Password Eye Button */
    .stPasswordInput button {
        background: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
    }

    .stPasswordInput button span,
    .stPasswordInput [data-testid="stIconMaterial"] {
        font-family: "Material Icons", "Material Symbols Rounded", sans-serif !important;
    }

    .stTextInput label,
    .stPasswordInput label {
        color: #cbd5e1 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.35rem !important;
    }

    /* Buttons */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 0.75rem 1.25rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        white-space: nowrap !important;
    }

    .stButton > button *,
    div[data-testid="stFormSubmitButton"] > button * {
        white-space: nowrap !important;
    }

    button[kind="primaryFormSubmit"],
    button[kind="primary"],
    button[data-testid="baseButton-primaryFormSubmit"],
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        background-color: #4f46e5 !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
    }

    button[kind="primaryFormSubmit"] *,
    button[kind="primary"] *,
    button[data-testid="baseButton-primaryFormSubmit"] *,
    button[data-testid="baseButton-primary"] * {
        color: #ffffff !important;
    }

    button[kind="primaryFormSubmit"]:hover,
    button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6) !important;
    }

    button[kind="secondaryFormSubmit"],
    button[kind="secondary"],
    button[data-testid="baseButton-secondaryFormSubmit"],
    button[data-testid="baseButton-secondary"],
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]):not([kind="primaryFormSubmit"]) {
        background: #1e293b !important;
        background-color: #1e293b !important;
        border: 1.5px solid #38bdf8 !important;
        color: #38bdf8 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }

    button[kind="secondaryFormSubmit"] *,
    button[kind="secondary"] *,
    button[data-testid="baseButton-secondaryFormSubmit"] *,
    button[data-testid="baseButton-secondary"] *,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]):not([kind="primaryFormSubmit"]) * {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
    }

    button[kind="secondaryFormSubmit"]:hover,
    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondaryFormSubmit"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]):not([kind="primaryFormSubmit"]):hover {
        background: #0f172a !important;
        background-color: #0f172a !important;
        border-color: #7dd3fc !important;
        color: #7dd3fc !important;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.35) !important;
    }

    button[kind="secondaryFormSubmit"]:hover *,
    button[kind="secondary"]:hover *,
    button[data-testid="baseButton-secondaryFormSubmit"]:hover *,
    button[data-testid="baseButton-secondary"]:hover *,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]):not([kind="primaryFormSubmit"]):hover * {
        color: #7dd3fc !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def login_page():
    load_auth_css()
    logo_b64 = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="coin-img" alt="Zyra">' if logo_b64 else '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>'

    col_hero, col_form = st.columns([1.1, 1.1], gap="large")

    with col_hero:
        st.markdown(f"""
        <div class="mascot-hero-panel">
            <div class="coin-3d-wrapper">
                {logo_html}
            </div>
            <h1 class="welcome-lead">Hello, Explorer</h1>
            <p class="welcome-desc">
                I am Zyra — your personalized AI career companion. Let's map your future, bridge skill gaps, and accelerate your tech career.
            </p>
            <div class="feature-tag-row">
                <div class="feature-tag-item">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
                    <span>Targeted Career Roadmaps</span>
                </div>
                <div class="feature-tag-item">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>
                    <span>Live Skill Gap & Radar Analytics</span>
                </div>
                <div class="feature-tag-item">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f472b6" stroke-width="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
                    <span>Adaptive Mock Interview Studio</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <div class="form-heading-title">Welcome Back</div>
            <div class="form-heading-sub">Sign in to your account or explore with demo access.</div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])
        
        with tab_login:
            render_login_tab()
            
        with tab_signup:
            render_signup_tab()

def render_login_tab():
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="login_password")
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        col_submit, col_demo = st.columns([1, 1])
        
        with col_submit:
            login_submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)
        with col_demo:
            demo_login = st.form_submit_button("Try Demo", type="secondary", use_container_width=True)

        if login_submitted:
            if not username or not password:
                st.warning("Please enter your credentials.")
            else:
                success, user_data = verify_user_login(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.current_page = 'chatroom'
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        if demo_login:
            demo_username = f"guest_{int(time.time()) % 10000}"
            demo_password = "demo_password_123"
            success, _ = create_user_account(demo_username, demo_password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = demo_username
                st.session_state.current_page = 'chatroom'
                st.rerun()
            else:
                st.error("Unable to create demo session.")

def render_signup_tab():
    with st.form("signup_form", clear_on_submit=False):
        new_username = st.text_input("Choose Username", placeholder="Enter desired username", key="signup_username")
        new_password = st.text_input("Create Password", type="password", placeholder="At least 6 characters", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="confirm_password")
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        signup_submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if signup_submitted:
            if not new_username or not new_password:
                st.warning("Please fill in all required fields.")
            elif len(new_username.strip()) < 3:
                st.error("Username must be at least 3 characters long.")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = create_user_account(new_username.strip(), new_password)
                if success:
                    st.success("Account created. Please switch to Sign In.")
                else:
                    st.error(message)

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'chatroom'
    if 'show_externals' not in st.session_state:
        st.session_state.show_externals = False
    if 'processing_message' not in st.session_state:
        st.session_state.processing_message = False

if __name__ == "__main__":
    init_session_state()
    if not st.session_state.logged_in:
        login_page()
    else:
        st.write(f"Logged in as {st.session_state.username}")
