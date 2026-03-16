# CodeShield-SDP: Technical Debt and Security Scanner

![Status](https://img.shields.io/badge/status-WIP-orange)
![Python](https://img.shields.io/badge/Python-100%25-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FF6B35.svg?&logo=streamlit&logoColor=white)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)

**CodeShield-SDP** is an AI‑assisted web application built with Streamlit that scans Python code for technical debt metrics (e.g., cyclomatic complexity via AST parsing) and security vulnerabilities. Upload code, visualize metrics, and get actionable insights to improve code quality and security.[page:1]

> ⚠️ This project is a **work in progress (WIP)**.  
> Features, UI, and analysis logic may change frequently as I iterate on the scanner and underlying models.[page:1]

---

## 🌐 Live Demo

You can try CodeShield-SDP online here:

👉 **[Open the live app](https://codeshield-tech-solutions.streamlit.app/)**

No setup needed – upload your Python file and explore the technical debt and security insights directly in the browser.[page:1]

---

## ✨ Key Features

- **Code analysis via AST** – Parses Python Abstract Syntax Trees to calculate nodes, edges, and complexity scores for technical debt metrics.[page:1]
- **Security scanning** – Detects common issues such as hardcoded secrets or unsafe patterns (with room to add more rules over time).[page:1]
- **Interactive dashboard** – Streamlit UI to upload files, display metrics, and visualize results.[page:1]
- **Database integration** – Uses a backend database (e.g., Supabase/Postgres) to store scan metadata and results for further analysis.[page:1]
- **Deployment ready** – Contains `app.py`, `pages/`, `utils/`, and `requirements.txt` for local or cloud deployment.[page:1]

---

## 🧱 Tech Stack & Structure

- **Frontend / Backend:** Streamlit (`app.py`, `pages/`).[page:1]
- **Language:** Python.[page:1]
- **Analysis logic:** Custom utilities for AST‑based metrics and security checks in `utils/`.[page:1]
- **Database:** Integration layer in `utils/` for inserting and querying scan data (e.g., with Supabase/Postgres).[page:1]

### Project layout

```text
codeshield-sdp/
├── app.py            # Main Streamlit application
├── pages/            # Additional Streamlit pages (navigation, views)
├── utils/            # Analysis logic, DB utilities, helpers
├── testing.py        # Testing / experimentation scripts
├── requirements.txt  # Python dependencies
├── .gitignore
├── LICENSE
└── README.md

### <details>

<summary>🚀 Quick Start</summary>

1. Clone: `git clone https://github.com/afsheenkhan-24/codeshield-sdp.git`
2. Install: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. Open browser to `localhost:8501` and upload Python code for scanning.

Set Supabase env vars for full features.

</details>

### <details>

<summary>📈 Recent Updates</summary>

- Switched to AST module for accurate node/edge calculation.
- Supabase integration for persistent data.
- CSS refinements and testing enhancements.

See [commits](https://github.com/afsheenkhan-24/codeshield-sdp/commits/main/) for full history.

</details>

## 🤝 Contributing

Fork, PRs welcome! Focus on adding more vuln detectors or ML-based debt scoring.

## 📄 License

GPL-3.0 [LICENSE](LICENSE)

**Stars and feedback appreciated! ⭐**
```
