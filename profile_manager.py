"""
Profile Management & Skills Analytics for Zyra AI
"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from auth_landing import save_user_data

def calculate_profile_completion(user_data):
    """Dynamically calculate actual profile completion percentage based on populated data"""
    score = 0
    profile = user_data.get('profile', {})
    
    # Basic Details (40 points)
    if profile.get('name') and profile['name'].strip() and not profile['name'].startswith('guest_'):
        score += 8
    if profile.get('current_role'):
        score += 6
    if profile.get('location') and profile['location'].strip():
        score += 6
    if profile.get('education') and profile['education'].strip():
        score += 6
    if profile.get('bio') and len(profile['bio'].strip()) > 10:
        score += 7
    if profile.get('goal') and len(profile['goal'].strip()) > 5:
        score += 7

    # Skills (30 points)
    tech = user_data.get('skills', {}).get('technical', {})
    if any(v > 0 for v in tech.values()):
        score += 15
    if len([v for v in tech.values() if v >= 50]) >= 3:
        score += 5

    soft = user_data.get('skills', {}).get('soft', {})
    if any(v > 0 for v in soft.values()):
        score += 10

    # Interests (15 points)
    interests = profile.get('interests', [])
    if len(interests) >= 1:
        score += 8
    if len(interests) >= 3:
        score += 7

    # Goals (15 points)
    goals = user_data.get('goals_tracking', {})
    total_goals = len(goals.get('short_term', [])) + len(goals.get('long_term', [])) + len(goals.get('completed', []))
    if total_goals >= 1:
        score += 8
    if total_goals >= 3:
        score += 7

    return min(100, score)

def load_profile_css():
    st.markdown("""
    <style>
    /* Dark Theme Form Controls */
    [data-baseweb="base-input"],
    [data-baseweb="input"],
    [data-baseweb="select"] > div,
    .stTextArea textarea {
        background: #0d1322 !important;
        background-color: #0d1322 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-size: 0.95rem !important;
    }

    [data-baseweb="base-input"]:focus-within,
    [data-baseweb="input"]:focus-within,
    [data-baseweb="select"] > div:focus-within,
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    }

    .stTextInput input,
    .stSelectbox div,
    .stTextArea textarea {
        color: #f8fafc !important;
    }

    .stTextInput label,
    .stSelectbox label,
    .stTextArea label,
    .stMultiSelect label {
        color: #cbd5e1 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.35rem !important;
    }

    /* Form Container */
    [data-testid="stForm"] {
        background: rgba(15, 20, 32, 0.85) !important;
        backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 1.75rem !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
    }

    /* Profile Tabs */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        width: 100% !important;
        gap: 8px !important;
        background: rgba(11, 16, 28, 0.85) !important;
        border-radius: 16px !important;
        padding: 5px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 1.5rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center !important;
        justify-content: center !important;
        background: transparent !important;
        border-radius: 12px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 10px 0 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.04) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
    }

    /* Header Profile Card */
    .profile-hero-card {
        background: rgba(15, 20, 32, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(25px);
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }

    .profile-avatar-box {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        font-size: 1.7rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
        border: 1.5px solid rgba(255, 255, 255, 0.2);
    }

    .skill-meter-card {
        background: rgba(11, 17, 32, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.85rem;
        transition: all 0.2s ease;
    }

    .skill-meter-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }

    .badge-chip {
        display: inline-flex;
        align-items: center;
        background: rgba(99, 102, 241, 0.12);
        color: #c7d2fe;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 8px 16px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.88rem;
        margin: 4px;
    }

    .interest-pill {
        display: inline-block;
        background: rgba(99, 102, 241, 0.12);
        color: #c7d2fe;
        border: 1px solid rgba(99, 102, 241, 0.25);
        padding: 5px 12px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.84rem;
        margin: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_profile_manager(user_data):
    load_profile_css()
    profile = user_data.setdefault('profile', {})
    user_data.setdefault('skills', {'technical': {}, 'soft': {}})
    
    # Calculate real-time dynamic completion score
    completion = calculate_profile_completion(user_data)
    profile['completion'] = completion
    
    name = profile.get('name', 'User')
    initial = name[0].upper() if name else 'U'
    role = profile.get('current_role', 'Student')
    
    # Dynamic completion pill color
    pill_color = "#34d399" if completion >= 70 else ("#818cf8" if completion >= 40 else "#fbbf24")
    pill_bg = "rgba(16, 185, 129, 0.12)" if completion >= 70 else ("rgba(99, 102, 241, 0.12)" if completion >= 40 else "rgba(245, 158, 11, 0.12)")
    pill_border = "rgba(16, 185, 129, 0.3)" if completion >= 70 else ("rgba(99, 102, 241, 0.3)" if completion >= 40 else "rgba(245, 158, 11, 0.3)")

    st.markdown(f"""
    <div class="profile-hero-card">
        <div style="display: flex; align-items: center; gap: 1.25rem;">
            <div class="profile-avatar-box">{initial}</div>
            <div>
                <h1 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: #f8fafc; margin: 0 0 0.25rem 0;">{name}</h1>
                <p style="color: #94a3b8; font-size: 0.92rem; margin: 0;">{role} • Level {user_data.get('level', 1)} • {user_data.get('xp', 0)} XP</p>
            </div>
        </div>
        <div style="background: {pill_bg}; color: {pill_color}; border: 1px solid {pill_border}; padding: 0.55rem 1.2rem; border-radius: 16px; font-weight: 700; font-size: 0.9rem;">
            Profile {completion}% Complete
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Basic Details", 
        "Skills & Radar", 
        "Career Goals", 
        "Milestones & Badges"
    ])

    with tab1:
        render_basic_info_tab(user_data)
        
    with tab2:
        render_skills_tab(user_data)
        
    with tab3:
        render_goals_tab(user_data)
        
    with tab4:
        render_achievements_tab(user_data)

def render_basic_info_tab(user_data):
    profile = user_data['profile']
    
    with st.form("basic_info_form"):
        st.markdown("<h3 style='font-family: Outfit, sans-serif; color: #f8fafc; font-size: 1.3rem; margin-bottom: 1.25rem;'>Personal & Professional Background</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=profile.get('name', ''))
            role_options = ["Student", "Job Seeker", "Software Developer", "Data Scientist", "Product Manager", "Designer", "Career Changer"]
            current_role = profile.get('current_role', 'Student')
            role_idx = role_options.index(current_role) if current_role in role_options else 0
            role = st.selectbox("Current Status", role_options, index=role_idx)
            
            exp_options = ["Beginner (0-1 yrs)", "Intermediate (1-3 yrs)", "Advanced (3-5 yrs)", "Lead / Senior (5+ yrs)"]
            current_exp = profile.get('experience_level', 'Beginner (0-1 yrs)')
            exp_idx = 0
            for i, opt in enumerate(exp_options):
                if current_exp.split()[0].lower() in opt.lower():
                    exp_idx = i
                    break
            experience = st.selectbox("Experience Level", exp_options, index=exp_idx)

        with col2:
            location = st.text_input("Location / City", value=profile.get('location', ''))
            education = st.text_input("Education / Major", value=profile.get('education', ''))
            work_type_options = ["Remote", "Hybrid", "On-site", "Flexible"]
            curr_wt = profile.get('preferred_work_type', 'Remote')
            wt_idx = work_type_options.index(curr_wt) if curr_wt in work_type_options else 0
            preferred_work = st.selectbox("Preferred Work Style", work_type_options, index=wt_idx)

        bio = st.text_area("Professional Summary", value=profile.get('bio', ''), height=90, placeholder="Briefly describe your background, technical interests, and experience...")
        goal = st.text_area("Primary Target Role / Career Goal", value=profile.get('goal', ''), height=70, placeholder="e.g. Become an AI Engineer at a high-growth tech company")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.form_submit_button("Save Profile Details", type="primary", use_container_width=True):
            profile['name'] = name.strip() or 'User'
            profile['current_role'] = role
            profile['experience_level'] = experience
            profile['location'] = location.strip()
            profile['education'] = education.strip()
            profile['preferred_work_type'] = preferred_work
            profile['bio'] = bio.strip()
            profile['goal'] = goal.strip()
            
            profile['completion'] = calculate_profile_completion(user_data)
            user_data['xp'] = user_data.get('xp', 0) + 20
            save_user_data(st.session_state.username, user_data)
            st.success("Profile saved successfully.")
            st.rerun()

def render_skills_tab(user_data):
    st.markdown("<div style='background: rgba(15, 20, 32, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.75rem; box-shadow: 0 15px 35px rgba(0,0,0,0.5); margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: Outfit, sans-serif; color: #f8fafc; font-size: 1.3rem; margin-bottom: 1.25rem;'>Skills Radar & Proficiency</h3>", unsafe_allow_html=True)

    tech_skills = user_data['skills'].get('technical', {})
    soft_skills = user_data['skills'].get('soft', {})

    if not tech_skills:
        tech_skills = {'Python': 70, 'SQL': 60, 'JavaScript': 50, 'React': 40, 'Machine Learning': 40}
        user_data['skills']['technical'] = tech_skills

    categories = list(tech_skills.keys())
    values = list(tech_skills.values())
    benchmark = [75] * len(categories)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Level',
        line=dict(color='#818cf8', width=2.5),
        fillcolor='rgba(99, 102, 241, 0.35)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=benchmark,
        theta=categories,
        name='Industry Target',
        line=dict(color='#38bdf8', width=2, dash='dash'),
        fillcolor='rgba(56, 189, 248, 0.08)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='#94a3b8', size=9),
                gridcolor='rgba(255, 255, 255, 0.12)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#f8fafc', size=11, family='Plus Jakarta Sans'),
                gridcolor='rgba(255, 255, 255, 0.12)'
            ),
            bgcolor='rgba(11, 17, 32, 0.6)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30),
        height=380,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color='#cbd5e1', size=12)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='color: #a5b4fc; font-size: 1.1rem; font-weight: 700; margin-bottom: 12px;'>Technical Proficiency</h4>", unsafe_allow_html=True)
        for skill, val in tech_skills.items():
            st.markdown(f"""
            <div class="skill-meter-card">
                <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.92rem; color: #f1f5f9; margin-bottom: 0.5rem;">
                    <span>{skill}</span>
                    <span style="color: #818cf8; font-weight: 800;">{val}%</span>
                </div>
                <div style="background: rgba(255,255,255,0.08); border-radius: 8px; height: 7px; overflow:hidden;">
                    <div style="background: linear-gradient(90deg, #4f46e5, #7c3aed); width: {val}%; height: 100%; border-radius: 8px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<h4 style='color: #38bdf8; font-size: 1.1rem; font-weight: 700; margin-bottom: 12px;'>Soft Skills</h4>", unsafe_allow_html=True)
        for skill, val in soft_skills.items():
            st.markdown(f"""
            <div class="skill-meter-card">
                <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.92rem; color: #f1f5f9; margin-bottom: 0.5rem;">
                    <span>{skill}</span>
                    <span style="color: #38bdf8; font-weight: 800;">{val}%</span>
                </div>
                <div style="background: rgba(255,255,255,0.08); border-radius: 8px; height: 7px; overflow:hidden;">
                    <div style="background: linear-gradient(90deg, #0284c7, #2563eb); width: {val}%; height: 100%; border-radius: 8px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("Update Skill Proficiency Levels"):
        with st.form("edit_skills_form"):
            st.markdown("**Technical Skills:**")
            new_tech = {}
            for skill, val in tech_skills.items():
                new_tech[skill] = st.slider(skill, 0, 100, val, step=5, key=f"sl_tech_{skill}")
            
            st.markdown("**Soft Skills:**")
            new_soft = {}
            for skill, val in soft_skills.items():
                new_soft[skill] = st.slider(skill, 0, 100, val, step=5, key=f"sl_soft_{skill}")
                
            if st.form_submit_button("Update Skills Database", type="primary"):
                user_data['skills']['technical'] = new_tech
                user_data['skills']['soft'] = new_soft
                user_data['profile']['completion'] = calculate_profile_completion(user_data)
                user_data['xp'] = user_data.get('xp', 0) + 15
                save_user_data(st.session_state.username, user_data)
                st.success("Skills matrix updated.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def render_goals_tab(user_data):
    st.markdown("<div style='background: rgba(15, 20, 32, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.75rem; box-shadow: 0 15px 35px rgba(0,0,0,0.5); margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: Outfit, sans-serif; color: #f8fafc; font-size: 1.3rem; margin-bottom: 1.25rem;'>Career Interests & Goal Tracking</h3>", unsafe_allow_html=True)

    all_interests = [
        "Web Development", "Artificial Intelligence", "Machine Learning", "Cloud & DevOps",
        "Data Engineering", "Cybersecurity", "Mobile Apps", "UI/UX Design", 
        "Product Management", "Blockchain / Web3", "FinTech", "System Design"
    ]
    current_interests = user_data['profile'].get('interests', [])
    
    with st.form("interests_form"):
        selected = st.multiselect("Select your career domains of interest:", all_interests, default=current_interests)
        if st.form_submit_button("Save Interests", type="secondary"):
            user_data['profile']['interests'] = selected
            user_data['profile']['completion'] = calculate_profile_completion(user_data)
            save_user_data(st.session_state.username, user_data)
            st.success("Interests saved.")
            st.rerun()

    if selected:
        st.markdown("<div>" + "".join([f'<span class="interest-pill">{item}</span>' for item in selected]) + "</div><br>", unsafe_allow_html=True)

    goals_tracking = user_data.setdefault('goals_tracking', {'short_term': [], 'long_term': [], 'completed': []})
    short_term = goals_tracking.setdefault('short_term', [])
    long_term = goals_tracking.setdefault('long_term', [])
    completed = goals_tracking.setdefault('completed', [])

    col_st, col_lt = st.columns(2)
    with col_st:
        st.markdown("<h4 style='color: #a5b4fc; font-size: 1.05rem; font-weight:700;'>Short-Term Goals (3-6 Months)</h4>", unsafe_allow_html=True)
        for i, g in enumerate(short_term):
            c_text, c_btn = st.columns([3.5, 1])
            with c_text:
                st.markdown(f"• **{g.get('goal')}**")
            with c_btn:
                if st.button("Complete", key=f"done_st_{i}"):
                    item = short_term.pop(i)
                    item['completed_date'] = datetime.now().isoformat()
                    completed.append(item)
                    user_data['profile']['completion'] = calculate_profile_completion(user_data)
                    user_data['xp'] = user_data.get('xp', 0) + 30
                    save_user_data(st.session_state.username, user_data)
                    st.success("Goal completed (+30 XP)")
                    st.rerun()

        new_st = st.text_input("Add new short-term goal:", key="input_new_st")
        if st.button("Add Short-Term Goal", key="btn_add_st") and new_st.strip():
            short_term.append({'goal': new_st.strip(), 'created_date': datetime.now().isoformat()})
            user_data['profile']['completion'] = calculate_profile_completion(user_data)
            save_user_data(st.session_state.username, user_data)
            st.rerun()

    with col_lt:
        st.markdown("<h4 style='color: #38bdf8; font-size: 1.05rem; font-weight:700;'>Long-Term Goals (6+ Months)</h4>", unsafe_allow_html=True)
        for i, g in enumerate(long_term):
            c_text, c_btn = st.columns([3.5, 1])
            with c_text:
                st.markdown(f"• **{g.get('goal')}**")
            with c_btn:
                if st.button("Complete", key=f"done_lt_{i}"):
                    item = long_term.pop(i)
                    item['completed_date'] = datetime.now().isoformat()
                    completed.append(item)
                    user_data['profile']['completion'] = calculate_profile_completion(user_data)
                    user_data['xp'] = user_data.get('xp', 0) + 60
                    save_user_data(st.session_state.username, user_data)
                    st.success("Milestone achieved (+60 XP)")
                    st.rerun()

        new_lt = st.text_input("Add new long-term goal:", key="input_new_lt")
        if st.button("Add Long-Term Goal", key="btn_add_lt") and new_lt.strip():
            long_term.append({'goal': new_lt.strip(), 'created_date': datetime.now().isoformat()})
            user_data['profile']['completion'] = calculate_profile_completion(user_data)
            save_user_data(st.session_state.username, user_data)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def render_achievements_tab(user_data):
    st.markdown("<div style='background: rgba(15, 20, 32, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.75rem; box-shadow: 0 15px 35px rgba(0,0,0,0.5); margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: Outfit, sans-serif; color: #f8fafc; font-size: 1.3rem; margin-bottom: 1.25rem;'>Milestones & Accolades</h3>", unsafe_allow_html=True)

    xp = user_data.get('xp', 0)
    level = user_data.get('level', 1)
    next_level_xp = level * 150
    curr_level_base = (level - 1) * 150
    progress_pct = min(100, max(0, int(((xp - curr_level_base) / 150) * 100)))

    st.markdown(f"""
    <div style="background: rgba(11, 17, 32, 0.85); border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-weight: 800; font-size: 1.1rem; color: #f8fafc;">Level {level} Explorer</span>
            <span style="color: #a5b4fc; font-weight: 700;">{xp} / {next_level_xp} XP</span>
        </div>
        <div style="background: rgba(255, 255, 255, 0.08); height: 10px; border-radius: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #4f46e5, #7c3aed); width: {progress_pct}%; height: 100%; border-radius: 8px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    badges = user_data.get('badges', ['New Member', 'First Step'])
    st.markdown("<h4 style='color: #cbd5e1; margin-bottom: 10px;'>Unlocked Badges:</h4>", unsafe_allow_html=True)
    
    badge_html = "".join([
        f'<div class="badge-chip">{b}</div>' 
        for b in badges
    ])
    st.markdown(f"<div>{badge_html}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
