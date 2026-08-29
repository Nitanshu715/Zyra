"""
Navigation & External Tool Components for Zyra AI
"""
import streamlit as st
import os
import base64

def get_image_base64(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                img_data = f.read()
            ext = os.path.splitext(image_path)[1].lstrip('.').lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{base64.b64encode(img_data).decode()}"
        return None
    except:
        return None

def render_external_resources_grid():
    tools = [
        {"name": "Resume Worded", "desc": "Score & optimize your resume with AI", "url": "https://resumeworded.com/", "img": "resume.jpg", "tag": "Resume"},
        {"name": "LinkedIn", "desc": "Network & find targeted recruiters", "url": "https://linkedin.com/", "img": "linkedin.png", "tag": "Network"},
        {"name": "GitHub", "desc": "Showcase your open source portfolio", "url": "https://github.com/", "img": "github.jpg", "tag": "Projects"},
        {"name": "Naukri", "desc": "Search active job openings in India", "url": "https://naukri.com/", "img": "naukri.png", "tag": "Jobs"},
        {"name": "GeeksforGeeks", "desc": "DSA, algorithms & system design", "url": "https://geeksforgeeks.org/", "img": "gfg.png", "tag": "Learning"},
        {"name": "YouTube Tech", "desc": "Video tutorials & tech interview prep", "url": "https://youtube.com/", "img": "youtube.jpg", "tag": "Courses"},
        {"name": "Canva Resume", "desc": "Design modern visual resumes & portfolios", "url": "https://canva.com/", "img": "canva.jpg", "tag": "Design"},
        {"name": "Miro Notes", "desc": "Map your learning roadmap & system architectures", "url": "https://miro.com/", "img": "notes.jpg", "tag": "Planning"}
    ]

    cols = st.columns(4)
    for i, item in enumerate(tools):
        with cols[i % 4]:
            img_path = os.path.join("photos", item["img"])
            img_uri = get_image_base64(img_path)
            
            img_element = f'<img src="{img_uri}" style="width: 100%; height: 120px; object-fit: cover; border-top-left-radius: 16px; border-top-right-radius: 16px;">' if img_uri else '<div style="height: 120px; background: linear-gradient(135deg, #4f46e5, #7c3aed); border-top-left-radius: 16px; border-top-right-radius: 16px; display:flex; align-items:center; justify-content:center; color:white; font-weight:700;">Zyra</div>'

            st.markdown(f"""
            <a href="{item['url']}" target="_blank" style="text-decoration: none; color: inherit;">
                <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; overflow: hidden; margin-bottom: 16px; transition: all 0.25s ease; box-shadow: 0 10px 25px rgba(0,0,0,0.3); backdrop-filter: blur(20px);">
                    {img_element}
                    <div style="padding: 14px 16px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 800; color: #f8fafc; font-size: 0.98rem;">{item['name']}</span>
                            <span style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); color: #a5b4fc; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 8px;">{item['tag']}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.84rem; line-height: 1.45; margin: 0;">{item['desc']}</p>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)
