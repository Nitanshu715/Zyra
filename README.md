<h1 align="center">🤖 Zyra – Your AI Career Companion</h1>
<p align="center">
  <em>AI-powered chatbot for personalized career growth & guidance</em><br>
  <strong>🌐 Built with Python, Streamlit, NLP & Recommendation Systems</strong>
</p>

<p align="center">
  <a href="https://its-zyra.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Demo-Streamlit-brightgreen?style=for-the-badge&logo=streamlit" />
  </a>
  <a href="https://github.com/Nitanshu715/Zyra">
    <img src="https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github" />
  </a>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com/?lines=Smart+Career+Guidance;Resume+Analysis+%26+Skill+Mapping;Interview+Preparation+Tips;Adaptive+Roadmaps+for+Growth&font=Fira%20Code&center=true&width=550&height=45&color=00C9A7&vCenter=true&pause=1000" />
</p>

---

## 📌 About Zyra

Zyra is not just another chatbot — it’s a **career growth companion**.  
It analyzes resumes, maps your skills to emerging job roles, gives interview tips, and adapts to your progress over time.

✨ **Why Zyra?**  
Traditional career portals give static or generic advice. Zyra adapts continuously, just like a real mentor.

---

## 🚀 Features

- 📄 **Resume Parsing & Analysis** – Extract skills, education, and experiences  
- 🎯 **Career Suggestions** – Recommend job roles and career paths  
- 💬 **Interactive Chat Interface** – Powered by NLP for real conversations  
- 🎤 **Interview Prep** – Mock questions, tips & feedback  
- 📊 **Skill-Gap Analysis** – Find missing skills and suggest how to acquire them  
- 🔄 **Adaptive Guidance** – Suggestions evolve as your profile grows  

---

## 🖼️ Prototype Flow

1. **Landing / Auth:** Login or Signup via `auth_landing.py`  
2. **Dashboard / Sidebar:** Navigate through Profile, Chat, History, Career, Externals  
3. **Chat & History:** Ask questions, get tailored advice, and track previous conversations  
4. **Career Suggestions:** View paths, resources, and project recommendations  
5. **Progress Tracking:** Update profile and see smarter suggestions over time  

---

## 🛠️ Tech Stack

Languages & Frameworks:
- Python (Streamlit, NLP, ML)
- HTML, CSS, JS (UI Extensions)

Core Modules:
- auth_landing.py     # Login & Signup
- chat_interface.py   # Conversational AI
- profile_manager.py  # Profile CRUD
- sidebar_components.py # Navigation

AI & Tools:
- NLP (spaCy / Transformers)
- Recommendation Systems
- scikit-learn, TensorFlow, PyTorch
- Streamlit for UI

---

## 📂 Project Structure

Zyra/
├── main.py                 # Entry point
├── auth_landing.py         # Authentication
├── chat_interface.py       # Chat logic
├── profile_manager.py      # Profile manager
├── sidebar_components.py   # Sidebar UI
├── requirements.txt        # Dependencies
├── logo.png                # App logo
└── photos/                 # Screenshots

---

## ⚡ Installation & Run

```bash
# Clone the repo
git clone https://github.com/Nitanshu715/Zyra.git
cd Zyra

# Setup virtual environment
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)

# Install requirements
pip install -r requirements.txt

# Run app
streamlit run main.py
```

---

## 📸 Screenshots

<p align="center">
  <img src="photos/login_page.png" width="400" />
  <img src="photos/chat_interface.png" width="400" />
</p>

---

## 🔮 Roadmap

- ✅ Prototype on Streamlit  
- 🔲 Connect to live job APIs (LinkedIn, Naukri, Indeed)  
- 🔲 Resume scoring using ML models  
- 🔲 Gamified career roadmap tracking  
- 🔲 AI mentors & peer community integration  

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/Nitanshu715/Zyra/issues).

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ by <a href="https://github.com/Nitanshu715">Nitanshu</a></p>

