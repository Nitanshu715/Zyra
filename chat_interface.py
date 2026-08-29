import streamlit as st
import os
import json
import time
import requests
from datetime import datetime
from auth_landing import load_user_data, save_user_data

def get_api_key():
    """Dynamically resolve API key from all possible Streamlit Cloud secrets & env variables"""
    # 1. Streamlit Secrets (Flat and Nested)
    try:
        if hasattr(st, "secrets"):
            for k in ["API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "api_key", "gemini_api_key"]:
                if k in st.secrets and st.secrets[k]:
                    return str(st.secrets[k]).strip()
            if "general" in st.secrets:
                for k in ["API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "api_key"]:
                    if k in st.secrets["general"] and st.secrets["general"][k]:
                        return str(st.secrets["general"][k]).strip()
    except Exception:
        pass

    # 2. Environment Variables
    for env_k in ["GEMINI_API_KEY", "API_KEY", "GOOGLE_API_KEY"]:
        val = os.environ.get(env_k)
        if val and val.strip():
            return val.strip()

    return None

def query_gemini_api(prompt_text):
    """Direct, fast HTTPS REST call with automated multi-tier model fallbacks"""
    api_key = get_api_key()
    
    if not api_key:
        return None, "API Key is missing. Please add API_KEY to your Streamlit Cloud Secrets (App Settings -> Secrets)."

    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }
    
    payload = {
        'contents': [
            {
                'parts': [
                    {'text': prompt_text}
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 1500
        }
    }
    
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-3.7-flash",
        "gemini-flash-latest",
        "gemini-pro-latest",
        "gemini-2.5-pro"
    ]
    
    last_error = ""
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=18)
            if res.status_code == 200:
                data = res.json()
                candidates = data.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        return parts[0].get('text', '').strip(), None
            elif res.status_code == 429:
                last_error = "Rate limit reached on current model. Switching tier..."
                continue
            else:
                last_error = f"API status {res.status_code}: {res.text[:150]}"
                continue
        except Exception as e:
            last_error = str(e)
            continue
            
    return None, f"Unable to generate response ({last_error}). Please check your API key quota or try again in a moment."

def load_chat_css():
    st.markdown("""
    <style>
    .chat-stream-panel {
        max-width: 860px !important;
        margin: 0 auto !important;
        padding-bottom: 2.5rem;
    }

    .chat-row-container {
        display: flex;
        width: 100%;
        margin-bottom: 1.25rem;
        gap: 12px;
        align-items: flex-start;
        animation: fadeInBubble 0.2s ease forwards;
    }

    .chat-row-container.user {
        justify-content: flex-end;
    }

    .chat-row-container.bot {
        justify-content: flex-start;
    }

    @keyframes fadeInBubble {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .chat-avatar-chip {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.9rem;
        flex-shrink: 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-top: 2px;
    }

    .chat-avatar-chip.user {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }

    .chat-avatar-chip.bot {
        background: linear-gradient(135deg, #0284c7, #2563eb);
        color: white;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }

    .bubble-wrapper {
        display: flex;
        flex-direction: column;
        max-width: 78%;
    }

    .bubble-wrapper.user {
        align-items: flex-end;
    }

    .bubble-wrapper.bot {
        align-items: flex-start;
    }

    .chat-bubble-card {
        width: fit-content !important;
        display: inline-block;
        padding: 0.85rem 1.35rem;
        font-size: 0.96rem;
        line-height: 1.55;
        word-break: break-word;
        box-sizing: border-box;
    }

    .chat-bubble-card.user {
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
        color: #ffffff;
        border-radius: 18px 18px 4px 18px;
        box-shadow: 0 6px 20px rgba(67, 56, 202, 0.35);
    }

    .chat-bubble-card.bot {
        background: rgba(15, 22, 36, 0.95);
        color: #f1f5f9;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px 18px 18px 4px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }

    .chat-bubble-card.bot h1, .chat-bubble-card.bot h2, .chat-bubble-card.bot h3 {
        color: #a5b4fc;
        margin-top: 0.5rem;
        margin-bottom: 0.35rem;
        font-family: 'Outfit', sans-serif;
    }

    .chat-bubble-card.bot ul, .chat-bubble-card.bot ol {
        margin-left: 1.25rem;
        margin-bottom: 0.5rem;
    }

    .chat-bubble-card.bot strong {
        color: #38bdf8;
    }

    .chat-bubble-card.bot code {
        background: rgba(11, 17, 32, 0.85);
        color: #f472b6;
        padding: 2px 6px;
        border-radius: 6px;
        font-size: 0.9em;
    }

    .chat-timestamp {
        font-size: 0.72rem;
        color: #64748b;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    /* Fixed Dark Theme Chat Input */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="base-input"],
    [data-testid="stChatInput"] [data-baseweb="input"] {
        background: #0d1322 !important;
        background-color: #0d1322 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7) !important;
    }

    [data-testid="stChatInput"]:focus-within,
    [data-testid="stChatInput"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3) !important;
    }

    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        background-color: transparent !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 0.98rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.8rem 1rem !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }

    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_single_bubble(msg, user_data):
    sender = msg.get('sender', 'user')
    content = msg.get('content', '')
    timestamp = msg.get('timestamp', '')
    time_display = ""
    try:
        if timestamp:
            time_display = datetime.fromisoformat(timestamp).strftime("%I:%M %p")
    except:
        pass

    if sender == 'user':
        user_initial = user_data['profile']['name'][0].upper() if user_data['profile'].get('name') else 'U'
        st.markdown(f"""
        <div class="chat-row-container user">
            <div class="bubble-wrapper user">
                <div class="chat-bubble-card user">{content}</div>
                {f'<div class="chat-timestamp">{time_display}</div>' if time_display else ''}
            </div>
            <div class="chat-avatar-chip user">{user_initial}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        bot_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>'
        st.markdown(f"""
        <div class="chat-row-container bot">
            <div class="chat-avatar-chip bot">{bot_svg}</div>
            <div class="bubble-wrapper bot">
                <div class="chat-bubble-card bot">{content}</div>
                {f'<div class="chat-timestamp">{time_display}</div>' if time_display else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_chat_interface(user_data):
    load_chat_css()
    chat_history = user_data.setdefault('chat_history', [])

    st.markdown('<div class="chat-stream-panel">', unsafe_allow_html=True)

    if len(chat_history) == 0:
        name = user_data['profile'].get('name', 'Explorer')
        st.markdown(f"""
        <div style="text-align: center; padding: 4.5rem 1.5rem 2.5rem 1.5rem; color: #94a3b8;">
            <div style="width: 64px; height: 64px; margin: 0 auto 1.25rem auto; border-radius: 20px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(236, 72, 153, 0.25)); border: 1.5px solid rgba(99, 102, 241, 0.4); display: flex; align-items: center; justify-content: center; color: #818cf8; box-shadow: 0 0 35px rgba(99, 102, 241, 0.3);">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
            </div>
            <h2 style="color: #f8fafc; font-size: 1.8rem; font-weight: 900; margin-bottom: 0.4rem; font-family: 'Outfit', sans-serif;">
                Hey {name}, how can I help you today?
            </h2>
            <p style="max-width: 460px; margin: 0 auto; line-height: 1.6; color: #94a3b8; font-size: 0.94rem;">
                Ask anything about coding, tech career transitions, skill gaps, or interview prep.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in chat_history:
            render_single_bubble(msg, user_data)

    st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input with Instant Rendering
    user_input = st.chat_input("Message Zyra...")
    if user_input:
        user_msg = {
            'sender': 'user',
            'content': user_input.strip(),
            'timestamp': datetime.now().isoformat()
        }
        chat_history.append(user_msg)
        save_user_data(st.session_state.username, user_data)

        # Immediately render the user's question on screen
        render_single_bubble(user_msg, user_data)

        # Query AI
        ai_prompt = create_ai_context(user_data, user_input.strip())
        with st.spinner("Thinking..."):
            bot_reply, error_msg = query_gemini_api(ai_prompt)
            if not bot_reply:
                bot_reply = f"I apologize, I encountered an issue: {error_msg}"

            chat_history.append({
                'sender': 'bot',
                'content': bot_reply,
                'timestamp': datetime.now().isoformat()
            })
            update_user_progress(user_data, user_input.strip())
            save_user_data(st.session_state.username, user_data)
        
        st.rerun()

def create_ai_context(user_data, user_input):
    profile = user_data.get('profile', {})
    skills = user_data.get('skills', {})
    chat_history = user_data.get('chat_history', [])
    
    recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history[:-1]
    history_formatted = ""
    for msg in recent_history:
        role = "User" if msg.get('sender') == 'user' else "Zyra"
        history_formatted += f"{role}: {msg.get('content', '')}\n"

    tech_skills_str = ', '.join([f"{k} ({v}%)" for k, v in skills.get('technical', {}).items() if v > 0]) or 'Not specified'

    system_prompt = f"""
You are Zyra, an intelligent, friendly, and highly adaptive AI Career Companion and Mentor.

### USER CONTEXT:
- Name: {profile.get('name', 'User')}
- Current Role: {profile.get('current_role', 'Student')}
- Target Goal: {profile.get('goal', 'Software / AI Engineer')}
- Key Skills: {tech_skills_str}

### RECENT CHAT HISTORY:
{history_formatted if history_formatted else 'No prior messages.'}

### CURRENT USER MESSAGE:
"{user_input}"

### INSTRUCTIONS:
1. **Be Conversational & Natural**: If the user is just saying hello, greeting you, or making small talk (e.g. "hello", "how are you", "what's up"), respond warmly and concisely in 1-2 friendly sentences. DO NOT dump an entire unsolicited career roadmap!
2. **Match the User's Intent**:
   - If they ask a quick question, give a direct, concise answer.
   - If they ask for a detailed roadmap, salary analysis, or mock interview, then provide a structured, in-depth guide with markdown headers and bullet points.
3. Keep the tone helpful, authentic, modern, and engaging.
"""
    return system_prompt

def update_user_progress(user_data, user_input):
    user_data['xp'] = user_data.get('xp', 0) + 20
    new_level = max(1, (user_data['xp'] // 150) + 1)
    old_level = user_data.get('level', 1)
    user_data['level'] = new_level
    
    badges = user_data.setdefault('badges', ['New Member'])
    chat_count = len(user_data.get('chat_history', []))
    
    if chat_count >= 2 and "First Dialogue" not in badges:
        badges.append("First Dialogue")
        user_data['xp'] += 30
    if chat_count >= 10 and "Career Enthusiast" not in badges:
        badges.append("Career Enthusiast")
        user_data['xp'] += 60
    if chat_count >= 20 and "Master Strategist" not in badges:
        badges.append("Master Strategist")
        user_data['xp'] += 120

    user_data['badges'] = list(set(badges))
    user_data['last_active'] = datetime.now().isoformat()
