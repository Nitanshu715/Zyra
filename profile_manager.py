"""
Redesigned Profile Management Module for Zyra AI Career Advisor
Clean, modern profile interface with better organization and visual hierarchy
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from auth_landing import save_user_data, load_user_data

def load_profile_css():
    """Modern CSS styles for profile management interface"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .profile-main-container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    
    .profile-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2.5rem 2rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .profile-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .profile-subtitle {
        color: #64748b;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 2rem;
        line-height: 1.5;
    }
    
    .profile-completion {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .section-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.1);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
        display: block;
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        border: 2px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        background: rgba(255, 255, 255, 0.9) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        margin: 0.5rem 0.25rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .skill-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .skill-item {
        background: rgba(248, 250, 252, 0.8);
        border: 2px solid rgba(148, 163, 184, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .skill-item:hover {
        border-color: rgba(102, 126, 234, 0.4);
        background: rgba(255, 255, 255, 0.9);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .skill-name {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .skill-level {
        font-size: 0.9rem;
        color: #667eea;
        font-weight: 600;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #64748b;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .achievement-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    .interest-tag {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        font-weight: 500;
        margin: 0.25rem;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .interest-tag:hover {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-color: transparent;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(241, 245, 249, 0.8);
        border-radius: 15px;
        padding: 5px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #64748b;
        font-weight: 500;
        padding: 12px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def render_profile_manager(user_data):
    """Render modern profile management interface"""
    load_profile_css()
    
    st.markdown('<div class="profile-main-container">', unsafe_allow_html=True)
    
    # Profile Header with completion status
    completion = user_data['profile'].get('completion', 20)
    st.markdown(f'''
    <div class="profile-header">
        <div class="profile-title">Your Professional Profile</div>
        <div class="profile-subtitle">
            Manage your career information and track your professional growth
        </div>
        <div class="profile-completion">
            Profile {completion}% Complete
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "Basic Info", 
        "Skills & Expertise", 
        "Goals & Interests", 
        "Achievements"
    ])
    
    with tab1:
        render_basic_info_tab(user_data)
    
    with tab2:
        render_skills_tab(user_data)
    
    with tab3:
        render_goals_tab(user_data)
    
    with tab4:
        render_achievements_tab(user_data)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_basic_info_tab(user_data):
    """Render basic information editing tab"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"> Personal & Professional Information</div>', unsafe_allow_html=True)
    
    with st.form("basic_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input(
                "Full Name", 
                value=user_data['profile']['name'],
                help="Your professional name"
            )
            
            new_role = st.selectbox(
                "Current Role",
                ["Student", "Job Seeker", "Professional", "Entrepreneur", "Freelancer", "Career Changer"],
                index=["Student", "Job Seeker", "Professional", "Entrepreneur", "Freelancer", "Career Changer"].index(user_data['profile']['current_role']),
                help="Select your current professional status"
            )
            
            new_experience = st.selectbox(
                "Experience Level",
                ["Beginner", "Intermediate", "Advanced", "Expert"],
                index=["Beginner", "Intermediate", "Advanced", "Expert"].index(user_data['profile']['experience_level']),
                help="Your overall experience in your field"
            )
        
        with col2:
            new_location = st.text_input(
                "Location",
                value=user_data['profile']['location'],
                help="Your current city/region"
            )
            
            new_education = st.text_input(
                "Education/Field of Study",
                value=user_data['profile']['education'],
                help="Your educational background or field of study"
            )
            
            new_work_type = st.selectbox(
                "Preferred Work Type",
                ["Remote", "Hybrid", "On-site", "Flexible"],
                index=["Remote", "Hybrid", "On-site", "Flexible"].index(user_data['profile'].get('preferred_work_type', 'Remote')),
                help="Your preferred working arrangement"
            )
        
        new_bio = st.text_area(
            "Professional Bio",
            value=user_data['profile']['bio'],
            height=100,
            help="A brief description of your professional background and aspirations"
        )
        
        new_goal = st.text_area(
            "Primary Career Goal",
            value=user_data['profile']['goal'],
            height=80,
            help="What you want to achieve in your career"
        )
        
        # Update button
        if st.form_submit_button("Update Profile Information", type="primary"):
            user_data['profile']['name'] = new_name
            user_data['profile']['current_role'] = new_role
            user_data['profile']['experience_level'] = new_experience
            user_data['profile']['location'] = new_location
            user_data['profile']['education'] = new_education
            user_data['profile']['preferred_work_type'] = new_work_type
            user_data['profile']['bio'] = new_bio
            user_data['profile']['goal'] = new_goal
            
            # Update completion percentage
            fields_completed = sum([
                bool(new_name.strip()),
                bool(new_role),
                bool(new_location.strip()),
                bool(new_education.strip()),
                bool(new_bio.strip()),
                bool(new_goal.strip()),
                bool(user_data['profile']['interests'])
            ])
            user_data['profile']['completion'] = min(90, int((fields_completed / 7) * 100))
            
            # Award profile completion badges
            if user_data['profile']['completion'] >= 70 and "Profile Pro" not in user_data.get('badges', []):
                user_data.setdefault('badges', []).append("Profile Pro")
                user_data['xp'] = user_data.get('xp', 0) + 50
            
            save_user_data(st.session_state.username, user_data)
            st.success("Profile updated successfully!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_skills_tab(user_data):
    """Render modern skills management tab"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Technical Skills</div>', unsafe_allow_html=True)
    
    # Technical skills display and editing
    technical_skills = user_data['skills']['technical']
    
    # Create skill grid
    st.markdown('<div class="skill-grid">', unsafe_allow_html=True)
    
    # Display skills in a modern grid
    cols = st.columns(3)
    skills_list = list(technical_skills.items())
    
    for i, (skill, level) in enumerate(skills_list):
        with cols[i % 3]:
            st.markdown(f'''
            <div class="skill-item">
                <div class="skill-name">
                    <span>{skill}</span>
                    <span class="skill-level">{level}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {level}%"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Skill editing form
    with st.expander("Edit Technical Skills"):
        with st.form("technical_skills_form"):
            st.markdown("**Update your skill levels:**")
            updated_skills = {}
            
            col1, col2 = st.columns(2)
            skills_list = list(technical_skills.items())
            mid_point = len(skills_list) // 2
            
            with col1:
                for skill, current_level in skills_list[:mid_point]:
                    new_level = st.slider(
                        f"{skill}",
                        min_value=0,
                        max_value=100,
                        value=current_level,
                        step=5,
                        key=f"tech_{skill}"
                    )
                    updated_skills[skill] = new_level
            
            with col2:
                for skill, current_level in skills_list[mid_point:]:
                    new_level = st.slider(
                        f"{skill}",
                        min_value=0,
                        max_value=100,
                        value=current_level,
                        step=5,
                        key=f"tech_{skill}_2"
                    )
                    updated_skills[skill] = new_level
            
            if st.form_submit_button("Update Technical Skills", type="primary"):
                user_data['skills']['technical'] = updated_skills
                save_user_data(st.session_state.username, user_data)
                st.success("Technical skills updated!")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Soft Skills Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Soft Skills</div>', unsafe_allow_html=True)
    
    soft_skills = user_data['skills']['soft']
    
    # Display soft skills
    cols = st.columns(3)
    soft_skills_list = list(soft_skills.items())
    
    for i, (skill, level) in enumerate(soft_skills_list):
        with cols[i % 3]:
            st.markdown(f'''
            <div class="skill-item">
                <div class="skill-name">
                    <span>{skill}</span>
                    <span class="skill-level">{level}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {level}%"></div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Soft skill editing form
    with st.expander("Edit Soft Skills"):
        with st.form("soft_skills_form"):
            st.markdown("**Update your soft skill levels:**")
            updated_soft_skills = {}
            
            col1, col2 = st.columns(2)
            soft_skills_list = list(soft_skills.items())
            soft_mid_point = len(soft_skills_list) // 2
            
            with col1:
                for skill, current_level in soft_skills_list[:soft_mid_point]:
                    new_level = st.slider(
                        f"{skill}",
                        min_value=0,
                        max_value=100,
                        value=current_level,
                        step=5,
                        key=f"soft_{skill}"
                    )
                    updated_soft_skills[skill] = new_level
            
            with col2:
                for skill, current_level in soft_skills_list[soft_mid_point:]:
                    new_level = st.slider(
                        f"{skill}",
                        min_value=0,
                        max_value=100,
                        value=current_level,
                        step=5,
                        key=f"soft_{skill}_2"
                    )
                    updated_soft_skills[skill] = new_level
            
            if st.form_submit_button("Update Soft Skills", type="primary"):
                user_data['skills']['soft'] = updated_soft_skills
                save_user_data(st.session_state.username, user_data)
                st.success("Soft skills updated!")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_goals_tab(user_data):
    """Render goals and interests management tab"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Career Interests</div>', unsafe_allow_html=True)
    
    # Interest selection
    all_interests = [
        "Web Development", "Mobile App Development", "Data Science", "Machine Learning", 
        "Artificial Intelligence", "Cybersecurity", "Cloud Computing", "DevOps",
        "Product Management", "Project Management", "Business Analysis", "Digital Marketing",
        "UI/UX Design", "Graphic Design", "Game Development", "Blockchain",
        "Financial Technology", "Healthcare Technology", "EdTech", "E-commerce"
    ]
    
    current_interests = user_data['profile']['interests']
    
    with st.form("interests_form"):
        selected_interests = st.multiselect(
            "Select your areas of interest (choose 3-8 for best results):",
            options=all_interests,
            default=current_interests,
            help="Choose areas that genuinely interest you for better career recommendations"
        )
        
        if st.form_submit_button("Update Interests", type="primary"):
            user_data['profile']['interests'] = selected_interests
            save_user_data(st.session_state.username, user_data)
            st.success("Interests updated!")
            st.rerun()
    
    # Display current interests
    if selected_interests:
        st.markdown("**Current Interests:**")
        interests_html = ""
        for interest in selected_interests:
            interests_html += f'<span class="interest-tag">{interest}</span>'
        st.markdown(interests_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Goals tracking section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Goal Tracking</div>', unsafe_allow_html=True)
    
    # Goal management simplified for cleaner UI
    goals_tracking = user_data.get('goals_tracking', {'short_term': [], 'long_term': [], 'completed': []})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Short-term Goals (3-6 months)**")
        short_goals = goals_tracking.get('short_term', [])
        
        for i, goal in enumerate(short_goals):
            col_goal, col_btn = st.columns([3, 1])
            with col_goal:
                st.write(f"• {goal['goal']}")
            with col_btn:
                if st.button("", key=f"complete_short_{i}"):
                    completed_goal = short_goals.pop(i)
                    completed_goal['completed_date'] = datetime.now().isoformat()
                    goals_tracking['completed'].append(completed_goal)
                    user_data['xp'] = user_data.get('xp', 0) + 25
                    save_user_data(st.session_state.username, user_data)
                    st.success("Goal completed! +25 XP")
                    st.rerun()
        
        new_short_goal = st.text_input("Add new short-term goal:", key="new_short_goal")
        if st.button("Add Goal") and new_short_goal:
            goals_tracking['short_term'].append({
                'goal': new_short_goal,
                'created_date': datetime.now().isoformat()
            })
            user_data['goals_tracking'] = goals_tracking
            save_user_data(st.session_state.username, user_data)
            st.success("Goal added!")
            st.rerun()
    
    with col2:
        st.markdown("**Long-term Goals (6+ months)**")
        long_goals = goals_tracking.get('long_term', [])
        
        for i, goal in enumerate(long_goals):
            col_goal, col_btn = st.columns([3, 1])
            with col_goal:
                st.write(f"• {goal['goal']}")
            with col_btn:
                if st.button("", key=f"complete_long_{i}"):
                    completed_goal = long_goals.pop(i)
                    completed_goal['completed_date'] = datetime.now().isoformat()
                    goals_tracking['completed'].append(completed_goal)
                    user_data['xp'] = user_data.get('xp', 0) + 50
                    save_user_data(st.session_state.username, user_data)
                    st.success("Major goal completed! +50 XP")
                    st.rerun()
        
        new_long_goal = st.text_input("Add new long-term goal:", key="new_long_goal")
        if st.button("Add Goal", key="add_long_goal") and new_long_goal:
            goals_tracking['long_term'].append({
                'goal': new_long_goal,
                'created_date': datetime.now().isoformat()
            })
            user_data['goals_tracking'] = goals_tracking
            save_user_data(st.session_state.username, user_data)
            st.success("Goal added!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_achievements_tab(user_data):
    """Render achievements and progress tab"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{user_data.get('level', 1)}</div>
            <div class="metric-label">Current Level</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{user_data.get('xp', 0)}</div>
            <div class="metric-label">Experience Points</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        total_chats = len(user_data.get('chat_history', []))
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_chats}</div>
            <div class="metric-label">Conversations</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        completed_goals = len(user_data.get('goals_tracking', {}).get('completed', []))
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{completed_goals}</div>
            <div class="metric-label">Goals Completed</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Your Badges</div>', unsafe_allow_html=True)
    
    # Display badges
    badges = user_data.get('badges', [])
    if badges:
        badges_html = ""
        for badge in badges:
            badges_html += f'<span class="achievement-badge">{badge}</span>'
        st.markdown(badges_html, unsafe_allow_html=True)
    else:
        st.info("Start using Zyra to earn your first badges!")
    
    st.markdown('</div>', unsafe_allow_html=True)