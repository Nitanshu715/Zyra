<div align=\"center\">

# Zyra AI — Intelligent Career Strategy & Skills Engine

**An enterprise-grade, conversational AI career mentor, skills diagnostic engine, and technical interview preparation platform powered by Google Gemini.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-v1beta%20REST-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Plotly](https://img.shields.io/badge/Plotly-Radar%20Analytics-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[**Explore Live Demo**](https://its-zyra.streamlit.app/) • [**Report Bug**](https://github.com/Nitanshu715/Zyra/issues) • [**Request Feature**](https://github.com/Nitanshu715/Zyra/issues)

</div>

---

## Overview

Traditional career portals provide static, one-size-fits-all roadmaps and outdated advice. **Zyra AI** functions as a personalized, context-aware AI career strategist and technical mentor. 

By evaluating a user's background, active technical proficiencies, soft skills, and target career paths, Zyra generates actionable 6-month milestones, conducts adaptive technical/behavioral mock interviews, visualizes skill gaps through interactive multi-axis radar charts, and provides localized Indian and global tech compensation benchmarks.

---

## Core Capabilities

### 1. Intelligent Conversational Advisor
- **Context-Aware Mentorship:** Evaluates the user's current seniority, skills, goals, and recent dialogue history to tailor responses.
- **Natural Dialogue Nuance:** Accurately distinguishes between conversational greetings (*\"Hey, how are you?\"*) and in-depth career inquiries, eliminating repetitive boilerplate monologues.
- **Instant Message Rendering:** User messages appear immediately on screen with zero lag, supported by high-speed Google Gemini REST pipelines.

### 2. Interactive Skills Radar & Diagnostics
- **Polar Proficiency Matrix:** Visualizes technical mastery against industry standards using interactive Plotly radar charts.
- **Dynamic Profile Scoring:** Evaluates completeness in real time based on active proficiencies, personal background, target roles, and tracked goals.
- **Multi-Level Sliders:** Real-time adjustments for both core engineering and soft skill proficiencies.

### 3. Emerging Career Pathways & Benchmarks
- **Market-Driven Roles:** Curated roadmaps for high-growth fields including AI/ML Engineering, Full-Stack Development, Data Science, and Cloud/DevOps Architecture.
- **Salary Benchmarks:** Transparent compensation insights tailored for both the Indian market (₹ LPA) and international tech hubs.
- **One-Click Roadmaps:** Instantly inject specific career pathways into the active AI consultation workspace.

### 4. Searchable Conversation Archive
- **Full History Archiving:** Automatically stores, dates, and organizes every consultation turn.
- **Keyword Filtering:** Instant real-time search across past mentorship dialogues, roadmaps, and interview transcripts.

### 5. Gamified XP & Milestone Tracking
- **Leveling Progression:** Earn XP through strategic dialogues, goal achievements, and profile milestones.
- **Unlockable Badges:** Accolades for consistent engagement, initial consultations, and roadmap execution.

---

## Architecture & Modular Design

Zyra follows a clean, decoupled modular architecture built on Streamlit:

`
Zyra/
├── main.py                 # Core application orchestrator, global theme & router
├── auth_landing.py         # 3D animated coin landing showcase, login & registration
├── chat_interface.py       # Conversational AI engine & direct Gemini REST interface
├── profile_manager.py      # Dynamic profile calculation, Plotly radar & goal tracker
├── sidebar_components.py   # Curated developer resource directory & learning hubs
├── requirements.txt        # Production dependencies
├── logo.png                # Brand identity asset
├── photos/                 # Curated external platform assets
└── .streamlit/
    ├── config.toml         # Native dark theme & minimalist UI configuration
    └── secrets.toml        # Secure Google Gemini API credentials (local/cloud)
`

---

## Tech Stack

| Domain | Technologies |
| :--- | :--- |
| **Frontend & UI** | Streamlit, Glassmorphic CSS3, HTML5 SVGs, Responsive Canvas |
| **AI & LLM Engine** | Google Gemini 1beta HTTPS REST API (gemini-flash-latest, gemini-2.5-flash, gemini-3.7-flash) |
| **Data Visualization** | Plotly Graph Objects (Scatterpolar), Dynamic Progress Fillers |
| **State & Persistence** | Streamlit Session State, Local JSON User Databases, SHA-256 Hashing |
| **Language & Runtime**| Python 3.10+ |

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- A Google Gemini API Key ([Get one here from Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone the Repository:**
   `ash
   git clone https://github.com/Nitanshu715/Zyra.git
   cd Zyra
   `

2. **Create & Activate a Virtual Environment:**
   `ash
   # Windows (PowerShell / Command Prompt)
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   `

3. **Install Dependencies:**
   `ash
   pip install -r requirements.txt
   `

4. **Configure Your API Key:**
   Create a .streamlit/secrets.toml file in the root directory:
   `	oml
   API_KEY = "your-google-gemini-api-key-here"
   `
   *(Alternatively, set the environment variable: export GEMINI_API_KEY="your-key")*

5. **Launch the Application:**
   `ash
   streamlit run main.py
   `

---

## Security & Best Practices

- **Zero Hardcoded Secrets:** API keys are dynamically loaded through st.secrets and environment variables.
- **Secure Password Hashing:** User passwords are encrypted with SHA-256 before disk storage.
- **Input Sanitization:** Usernames and form inputs are sanitized against directory traversal and invalid characters.
- **Resilient API Fallback:** Automated model failover prevents disruptions if a specific Gemini model tier encounters rate limits.

---

## Authors & Acknowledgments

- **Nitanshu Tak** — [*LinkedIn*](https://www.linkedin.com/in/nitanshu-tak-89a1ba289/) • [*GitHub*](https://github.com/Nitanshu715)
- **Khushi Kushwaha** — [*LinkedIn*](https://www.linkedin.com/in/khushkushwaha45/)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete details.
