import streamlit as st
import json
import os
import hashlib
import time
import base64
from datetime import datetime

# ---- INDIVIDUAL USER FILE MANAGEMENT ----
def get_user_filename(username):
    """Get sanitized filename for user data"""
    safe_username = "".join(c for c in username if c.isalnum() or c in ('_', '-')).lower()
    return f"user_{safe_username}.json"

def load_user_data(username):
    """Load individual user data from their JSON file"""
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
    """Save individual user data to their JSON file"""
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
    """Check if user exists (has a JSON file)"""
    filename = get_user_filename(username)
    return os.path.exists(filename)

def create_user_account(username, password):
    """Create new user account with individual JSON file"""
    if user_exists(username):
        return False, "Username already exists!"
    user_data = init_user_data(username)
    user_data['password'] = hash_password(password)
    if save_user_data(username, user_data):
        return True, "Account created successfully!"
    else:
        return False, "Error creating account!"

def verify_user_login(username, password):
    """Verify user login credentials"""
    user_data = load_user_data(username)
    if user_data and user_data.get('password') == hash_password(password):
        return True, user_data
    return False, None

# ---- HELPER FUNCTIONS ----
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_user_data(username):
    """Initialize clean user data structure"""
    return {
        'username': username,
        'password': '',
        'created_at': datetime.now().isoformat(),
        'profile': {
            'name': username.title(),
            'current_role': 'Student',
            'experience_level': 'Beginner',
            'location': '',
            'education': '',
            'preferred_work_type': 'Remote',
            'availability': 'Learning and growing',
            'bio': '',
            'goal': '',
            'interests': [],
            'completion': 20
        },
        'skills': {
            'technical': {
                'Python': 0,
                'JavaScript': 0,
                'HTML/CSS': 0,
                'SQL': 0,
                'React': 0,
                'Machine Learning': 0
            },
            'soft': {
                'Communication': 50,
                'Teamwork': 50,
                'Problem Solving': 50,
                'Leadership': 30,
                'Time Management': 40,
                'Adaptability': 45
            }
        },
        'goals_tracking': {
            'short_term': [],
            'long_term': [],
            'completed': []
        },
        'chat_history': [],
        'xp': 0,
        'level': 1,
        'badges': ['New Member'],
        'streak': 1,
        'last_active': datetime.now().isoformat()
    }

def get_logo_base64():
    """Get base64 encoded logo if it exists"""
    try:
        if os.path.exists("logo.png"):
            with open("logo.png", "rb") as f:
                logo_data = f.read()
                return base64.b64encode(logo_data).decode()
        return None
    except:
        return None

def load_css():
    """Modern CSS styles for landing page, with improved login box and tabs spacing"""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    .stApp {{
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%) !important;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }}
    /* Remove white login box */
    .login-container {{
        max-width: 480px;
        margin-top: -4rem !important;
        margin: 0px auto 2rem auto;
        padding-bottom: 0.5rem !important;
        background: transparent !important;
        backdrop-filter: none !important;
        border-radius: 30px;
        padding: 0px 0px 0px 0px;
        box-shadow: none !important;
        border: none !important;
        position: relative;
        z-index: 100;
    }}
    button, .stButton > button {{
    box-shadow: none !important;
    }}
    /* Tabs drag up and spacing */
    .stTabs {{
        margin-top: -35px !important;
        margin-bottom: 1rem !important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(241, 245, 249, 0.8) !important;
        border-radius: 15px;
        padding: 5px;
        margin-bottom: 0.5rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        border-radius: 12px;
        color: #64748b !important;
        font-weight: 500;
        padding: 12px 25px;
        border: none;
        transition: all 0.3s ease;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }}
    /* Form fields spacing and centering fix */
    .stTextInput, .stPasswordInput {{
        margin-bottom: 10px !important;
    }}
    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input {{
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: rgba(255, 255, 255, 0.9) !important;
        width: 100% !important;
        margin-bottom: 10px !important;
        color: #222 !important;
        text-align: left !important;
        /* Center vertically in the input box */
        display: flex !important;
        align-items: center !important;
        height: 48px !important;
    }}
    /* Fix label color and visibility */
    label, .stTextInput label, .stPasswordInput label {{
        color: #fff !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }}
    /* Placeholder text style (grey and left aligned) */
    ::placeholder {{
        color: #bdbdbd !important;
        opacity: 1 !important;
        font-size: 1rem !important;
        text-align: left !important;
    }}
    /* Fix the icon color for password field */
    .stPasswordInput svg {{
        color: #64748b !important;
    }}
    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus {{
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        margin: 10px 0 !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4) !important;
    }}
    .stButton > button:active {{
        transform: translateY(-1px) !important;
    }}
    /* SUCCESS AND ERROR MESSAGES */
    .stAlert {{
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        margin: 15px 0 !important;
        border: none !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    }}
    .stAlert[data-baseweb="notification"] {{
        background: rgba(255, 255, 255, 0.95) !important;
    }}
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{visibility: hidden;}}
    /* Force remove any remaining white backgrounds */
    .css-1d391kg, .css-1y4p8pa, .css-12oz5g7, .css-1lcbmhc {{
        background: transparent !important;
    }}
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }}
    /* Logo area - make logo 2x bigger */
    .logo-container {{
        text-align: center;
        padding: 0rem 0 1rem 0;
        background: transparent !important;
    }}
    .logo-image {{
        width: 560px;
        height: 360px;
        border-radius: 50px;
        filter: drop-shadow(0 20px 80px rgba(255, 255, 255, 0.3));
        animation: logoFloat 6s ease-in-out infinite;
    }}
    .logo-fallback {{
        font-size: 16rem;
        animation: logoFloat 6s ease-in-out infinite;
        color: white;
    }}
    @keyframes logoFloat {{
        0%, 100% {{
            transform: translateY(0px);
        }}
        50% {{
            transform: translateY(-30px);
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def login_page():
    """Modern redesigned login page"""
    load_css()
    # Logo section
    logo_b64 = get_logo_base64()
    if logo_b64:
        st.markdown(f'''
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_b64}" class="logo-image" alt="Zyra Logo">
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="logo-container">
            <div class="logo-fallback">🎯</div>
        </div>
        ''', unsafe_allow_html=True)
    # Center the login container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        with tab1:
            render_login_tab()
        with tab2:
            render_signup_tab()
        st.markdown('</div>', unsafe_allow_html=True)

def render_login_tab():
    """Render login tab"""
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        col_login, col_demo = st.columns(2)
        with col_login:
            login_submitted = st.form_submit_button("Sign In", type="primary")
        with col_demo:
            demo_login = st.form_submit_button("Try Demo")
        if login_submitted and username and password:
            success, user_data = verify_user_login(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Welcome back!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password!")
        if demo_login:
            demo_username = f"demo_user_{int(time.time())}"
            demo_password = "demo123"
            success, message = create_user_account(demo_username, demo_password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = demo_username
                st.success("Demo account created! Explore Zyra now.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Error creating demo account!")

def render_signup_tab():
    """Render signup tab"""
    with st.form("signup_form", clear_on_submit=False):
        new_username = st.text_input("Username", placeholder="Choose a unique username", key="signup_username")
        new_password = st.text_input("Password", type="password", placeholder="Create a secure password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="confirm_password")
        signup_submitted = st.form_submit_button("Create Account", type="primary")
        if signup_submitted and new_username and new_password:
            if len(new_username) < 3:
                st.error("Username must be at least 3 characters long!")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif new_password != confirm_password:
                st.error("Passwords don't match!")
            else:
                success, message = create_user_account(new_username, new_password)
                if success:
                    st.success(message + " Please sign in with your new account.")
                else:
                    st.error(message)

def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'chat'

# To run:
if __name__ == "__main__":
    init_session_state()
    if not st.session_state.logged_in:
        login_page()
    else:
        st.write(f"Hello, {st.session_state.username}! You're logged in.")