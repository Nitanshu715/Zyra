import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime
from auth_landing import load_user_data, save_user_data

# ---- CONFIG ----
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def load_chat_css():
    """Big box, chat and chatbox ALWAYS inside the box, welcome disappears after first message, old chats never show outside box"""
    st.markdown("""
    <style>
    body, .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

    /* Hide Streamlit's default elements that might interfere */
    .stForm {
        border: none !important;
        background: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Make sure the main content area has no default padding */
    .main > div {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Ensure the Streamlit container itself doesn't add padding */
    .st-emotion-cache-1kyq9sp {
        padding: 0 !important;
    }
    
    .chat-content-area {
        flex: 1;
        display: flex;
        flex-direction: column;
        height: 100%;
        overflow: hidden;
    }
    
    .welcome-cursive {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-family: 'Pacifico', cursive, 'Inter', sans-serif;
        font-size: 2.7rem;
        font-weight: 500;
        color: #6c63ff;
        padding: 20px;
        margin: 0;
        letter-spacing: 0.01em;
        background: none;
        border: none;
        box-shadow: none;
        transition: opacity 0.3s;
    }
    
    /* Updated styling for chat history container */
    .chat-history-container {
        flex: 1;
        padding: 20px 42px 10px 42px;
        overflow-y: auto;
        min-height: 0;
    }
    
    .chat-message-row {
        display: flex;
        align-items: flex-end;
        margin-bottom: 18px;
    }
    
    .chat-message-bubble {
        font-size: 1.08rem;
        line-height: 1.62;
        border-radius: 23px;
        padding: 1.15rem 1.75rem;
        max-width: 78%;
        box-shadow: 0 2px 10px rgba(102,126,234,0.09);
        word-break: break-word;
        margin-bottom: 0.5rem;
        background: #f4f7fe;
        color: #2d3748;
    }
    
    .chat-message-bubble.user {
        background: linear-gradient(135deg, #667eea 60%, #6c63ff 100%);
        color: white;
        margin-left: auto;
    }
    
    .chat-message-bubble.bot {
        background: linear-gradient(120deg, #e7eafc 70%, #fff 100%);
        color: #2d3748;
        margin-right: auto;
        border: 1.5px solid rgba(102,126,234,0.08);
    }
    
    .chat-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        font-size: 1.22rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 10px;
        box-shadow: 0 1px 8px rgba(102,126,234,0.13);
    }
    
    .chat-avatar.user {
        background: linear-gradient(135deg, #667eea 60%, #6c63ff 100%);
        color: white;
        order: 2;
        margin-left: 10px;
        margin-right: 0;
    }
    
    .chat-avatar.bot {
        background: linear-gradient(135deg, #10b981 30%, #059669 100%);
        color: white;
        order: 1;
        margin-right: 10px;
        margin-left: 0;
    }
    button, .stButton > button {
        box-shadow: none !important;
    }
    .input-area-section {
        background: rgba(245, 247, 255, 1);
        border-radius: 0 0 40px 40px;
        padding: 0px 52px 26px 52px;
        border-top: 1.5px solid #e5e7eb;
        box-shadow: 0 2px 10px rgba(102,126,234,0.07);
        flex-shrink: 0;
        width: 100%;
    }
    
    .stTextArea > div > div > textarea {
        border: 2px solid #a5b4fc !important;
        border-radius: 19px !important;
        padding: 1rem 1.25rem !important;
        font-size: 1.12rem !important;
        min-height: 70px !important;
        max-height: 120px !important;
        background: #e7eafc !important;
        font-family: 'Inter', sans-serif !important;
        resize: none !important;
        transition: border-color 0.3s;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #6c63ff !important;
        box-shadow: 0 0 0 4px rgba(102,126,234,0.19) !important;
        outline: none !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #8b94b5 !important;
        font-size: 1.07rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 60%, #6c63ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 17px !important;
        padding: 0.85rem 2.05rem !important;
        font-weight: 600 !important;
        font-size: 1.07rem !important;
        box-shadow: 0 2px 8px rgba(102,126,234,0.13) !important;
        margin: 0.5rem 0.25rem !important;
        min-width: 110px !important;
        transition: box-shadow 0.2s, transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 6px 18px rgba(102,126,234,0.23) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 0.6rem 0 0.6rem 0;
        color: #667eea;
        font-style: italic;
        font-size: 1.06rem;
        font-weight: 500;
    }
    
    .typing-dots {
        display: flex;
        margin-left: 0.5rem;
    }
    
    .typing-dot {
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background: #667eea;
        margin: 0 2px;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

def render_chat_interface(user_data):
    """
    - Enclose ALL content inside big box.
    - Chatbox is ALWAYS at bottom INSIDE the box.
    - On login: Only cursive welcome message and chatbox at bottom inside box.
    - After first message: Welcome disappears, chat history starts stacking up above chatbox, all inside the box.
    - Old chats never show outside the box.
    """

    if st.session_state.get("first_login", True):
        user_data['chat_history'] = []
        save_user_data(st.session_state.username, user_data)
        st.session_state.first_login = False

    load_chat_css()
    chat_history = user_data.get('chat_history', [])

    with st.container():
        st.markdown('<div class="main-chat-boundary">', unsafe_allow_html=True)
        st.markdown('<div class="chat-content-area">', unsafe_allow_html=True)

        if len(chat_history) == 0:
            st.markdown('<div class="welcome-cursive">Hiii, let\'s talk and find a path together!</div>', unsafe_allow_html=True)
        else:
            # Use a container for the chat history to enable scrolling
            with st.container(height=650):
                for message in chat_history:
                    if message['sender'] == 'user':
                        user_initial = user_data['profile']['name'][0].upper() if user_data['profile']['name'] else 'U'
                        st.markdown(f'''
                        <div class="chat-message-row" style="justify-content:flex-end;">
                            <div class="chat-message-bubble user">{message['content']}</div>
                            <div class="chat-avatar user">{user_initial}</div>
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                        <div class="chat-message-row" style="justify-content:flex-start;">
                            <div class="chat-avatar bot">🤖</div>
                            <div class="chat-message-bubble bot">{message['content']}</div>
                        </div>
                        ''', unsafe_allow_html=True)
                
                if st.session_state.get('processing_message', False):
                    st.markdown('''
                    <div class="typing-indicator">
                        Zyra is thinking
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # close chat-content-area
        
        # This is the form, which must be INSIDE the boundary.
        # It's placed directly after the chat content area.
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "",
                placeholder="Type your message here...",
                height=70,
                key="chat_input",
                label_visibility="collapsed",
            )
            # Wrap form content in the input-area-section div
            send_button = st.form_submit_button("Send Message 🚀", type="primary")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # close main-chat-boundary

    if send_button and user_input.strip():
        process_chat_message(user_input.strip(), user_data)

def process_chat_message(user_input, user_data):
    """Process chat message and generate AI response, persistent history"""
    try:
        st.session_state.processing_message = True
        if 'chat_history' not in user_data:
            user_data['chat_history'] = []
        user_data['chat_history'].append({
            'sender': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        profile_context = create_ai_context(user_data, user_input)
        with st.spinner("Zyra is thinking..."):
            response = model.generate_content(profile_context)
            bot_reply = response.text
            bot_reply = bot_reply.replace("```", "").strip()

        user_data['chat_history'].append({
            'sender': 'bot',
            'content': bot_reply,
            'timestamp': datetime.now().isoformat()
        })
        update_user_progress(user_data, user_input)
        save_user_data(st.session_state.username, user_data)
        st.session_state.processing_message = False
        st.rerun()
        except Exception as e:
        st.session_state.processing_message = False
        st.error("I'm having trouble processing your message right now. Please try again in a moment.")
        st.error(f"Technical details: {str(e)}")

def create_ai_context(user_data, user_input):
    """Context for AI: personalized, Indian market, guidance style"""
    profile = user_data.get('profile', {})
    skills = user_data.get('skills', {})
    context = f"""
You are Zyra, an expert AI career advisor with deep knowledge of the Indian job market and global career trends.

You're currently helping {profile.get('name', 'User')}, who has the following profile:

PROFILE INFORMATION:
- Current Role: {profile.get('current_role', 'Student')}
- Experience Level: {profile.get('experience_level', 'Beginner')}
- Location: {profile.get('location', 'India')}
- Education: {profile.get('education', 'Not specified')}
- Career Goal: {profile.get('goal', 'Professional growth')}
- Interests: {', '.join(profile.get('interests', ['General career development']))}

CURRENT SKILLS:
Technical Skills: {', '.join([f"{skill} ({level}%)" for skill, level in skills.get('technical', {}).items() if level > 0]) or 'None specified'}
Soft Skills: {', '.join([f"{skill} ({level}%)" for skill, level in skills.get('soft', {}).items() if level > 50]) or 'Basic communication skills'}

USER'S QUESTION: "{user_input}"

RESPONSE GUIDELINES:
1. Provide personalized, actionable advice based on their profile
2. Include specific salary ranges in Indian context (₹X LPA) when discussing careers
3. Suggest concrete next steps they can take
4. Be encouraging and supportive while being realistic
5. Keep responses focused and under 300 words
6. Use bullet points or numbered lists when providing multiple recommendations
7. Reference current market trends and in-demand skills when relevant
8. If asked about career changes, provide a structured transition plan

Respond in a warm, professional tone as their personal career mentor.
    """
    return context

def update_user_progress(user_data, user_input):
    """XP, level, badges, persistent progress"""
    user_data['xp'] = user_data.get('xp', 0) + 15
    new_level = max(1, user_data['xp'] // 200)
    old_level = user_data.get('level', 1)
    user_data['level'] = new_level
    if new_level > old_level:
        st.balloons()
        st.success(f"Congratulations! You've reached Level {new_level}!")
    badges = user_data.get('badges', [])
    chat_count = len(user_data.get('chat_history', []))
    if chat_count >= 2 and "First Chat" not in badges:
        badges.append("First Chat")
        user_data['xp'] += 25
        st.success("Badge earned: First Chat!")
    if chat_count >= 10 and "Regular User" not in badges:
        badges.append("Regular User")
        user_data['xp'] += 50
        st.success("Badge earned: Regular User!")
    if chat_count >= 25 and "Career Explorer" not in badges:
        badges.append("Career Explorer")
        user_data['xp'] += 100
        st.success("Badge earned: Career Explorer!")
    user_data['badges'] = badges
    user_data['last_active'] = datetime.now().isoformat()







