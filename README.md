# BrandSphere AI 🎨
### AI-Powered Automated Branding Assistant for Businesses

> **CRS AI Capstone 2025–26 · Scenario 1**  
> Aashi Dimple Soni (2405728) · Hemer Manish Pandya (2405426) · Zivantika Amit Singh (2405744)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dxyqtqy2vmevept6gqz9qe.streamlit.app)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Project Title and Description

BrandSphere AI is an end-to-end **AI-powered branding intelligence platform** designed for small and medium-sized businesses (SMBs). It automates the complete brand identity creation process — from logo generation and colour palettes to taglines, multilingual campaigns, animated visuals, and predictive analytics — all within a single interactive Streamlit web application.

The platform integrates **Computer Vision**, **Natural Language Processing**, **Generative AI (Gemini 2.0 Flash)**, and **Machine Learning** to deliver professional-grade branding in under 10 minutes at zero cost.

**Live App:** https://dxyqtqy2vmevept6gqz9qe.streamlit.app  
**PRD Document:** See `/docs/` folder

---

## ✨ Features

| Module | Feature | Technology |
|---|---|---|
| 🎨 Logo Studio | 5 SVG logo styles + KNN similarity retrieval | KNN, SVG, Pillow |
| 🖋 Fonts & Palette | KNN font classifier (91.4% acc) + KMeans palette | scikit-learn, KMeans |
| ✍️ Slogans & Content | NLTK TF-IDF retrieval + Gemini generation + Brand Narrative | NLTK, Gemini API |
| 📣 Campaign Analytics | ML prediction (CTR, ROI, Engagement) + Plotly dashboards | Random Forest, Ridge |
| 🌍 Multilingual Studio | 7-language translation with tone validation | Gemini API |
| 🎬 Animation Preview | 1080×1080 GIF (typewriter, fade, slide styles) | Pillow |
| 📡 Trend Radar | Industry trend analysis with momentum scores | Gemini API |
| ✅ Launch Checklist | Personalised 30-step GTM plan | Gemini API |
| 🔍 Competitor Gaps | Strategic gap finder with opportunity scores | Gemini API |
| 👥 Audience Personas | 3 detailed buyer personas | Gemini API |
| ⭐ Feedback | Per-module ratings + Plotly analytics dashboard | pandas, Plotly |
| 📦 Download Kit | Full brand ZIP (SVG, PNG, GIF, JSON, CSV) | zipfile |

---

## 🛠 Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.14.3 | Core language |
| Streamlit | 1.55.0 | Web interface & deployment |
| google-genai | 1.67.0 | Gemini 2.0 Flash (Generative AI) |
| scikit-learn | 1.8.0 | KNN, Random Forest, KMeans, Ridge |
| Pillow | 12.1.1 | 1080×1080 GIF animation |
| Plotly | 6.6.0 | Interactive dashboards |
| NLTK | 3.9.3 | TF-IDF, tokenisation, NLP |
| pandas / NumPy | 2.3 / 2.4 | Data processing |
| Matplotlib / Seaborn | 3.10 / 0.13 | EDA & visualisation |
| OpenCV (cv2) | via notebook | Logo image preprocessing |

---

## 📁 Repository Structure

```
BrandSphere-AI/
├── app.py                          ← Main Streamlit application (14 tabs)
├── requirements.txt                ← Python dependencies
├── README.md                       ← This file
│
├── src/                            ← AI/ML engine modules
│   ├── config.py                   ← Constants and mappings
│   ├── palette_engine.py           ← KMeans colour extraction
│   ├── logo_engine.py              ← SVG logo generation
│   ├── font_engine.py              ← KNN font recommendation
│   ├── slogan_engine.py            ← NLTK + Gemini tagline engine
│   ├── animation_engine.py         ← Pillow GIF generator (1080×1080)
│   ├── multilingual_engine.py      ← Gemini translation engine
│   ├── campaign_predictor.py       ← ML campaign prediction
│   ├── aesthetics_engine.py        ← Brand scoring
│   ├── feedback_engine.py          ← CSV feedback loop
│   ├── export_engine.py            ← ZIP brand kit builder
│   └── dashboard_engine.py         ← Plotly chart generators
│
├── models/                         ← Trained ML models (.pkl)
│   ├── logo_classifier.pkl         ← KNN on 512-dim CNN embeddings
│   ├── logo_slim_package.pkl       ← 1044 logo embeddings, 50 classes
│   ├── font_category_classifier.pkl← KNN font classifier (91.4% acc)
│   ├── font_personality_classifier.pkl
│   ├── roi_model.pkl               ← Ridge regression (campaign)
│   ├── engagement_model.pkl
│   ├── conversion_model.pkl
│   ├── encoders.pkl
│   └── scaler.pkl
│
├── datasets/
│   ├── raw/
│   │   ├── marketing_campaign_dataset.csv  ← 200,000 campaign records
│   │   ├── startups.csv                    ← 42,038 startup profiles
│   │   └── font_dataset.csv                ← 31 fonts × typographic features
│   └── processed/
│       ├── cleaned_marketing.csv
│       ├── cleaned_slogans.csv
│       ├── cleaned_startups.csv
│       ├── font_features.csv               ← 465 augmented font samples
│       └── campaign_features.csv
│
├── notebooks/                      ← 10 Jupyter notebooks (Colab-ready)
│   ├── 01_eda.ipynb                ← Week 1: EDA all datasets
│   ├── 02_slogan_engine.ipynb      ← Week 4: NLTK + TF-IDF + HuggingFace
│   ├── 03_campaign_prediction.ipynb← Week 7: ML training pipeline
│   ├── 04_palette_engine.ipynb     ← Week 5: KMeans + WCAG
│   ├── 05_integration_tests.ipynb  ← Week 10: End-to-end tests
│   ├── 06_logo_engine.ipynb        ← Week 2: CNN embeddings + KNN
│   ├── 07_font_engine.ipynb        ← Week 3: KNN font classifier
│   ├── 08_animation_studio.ipynb   ← Week 6: 1080×1080 GIF
│   ├── 09_multilingual.ipynb       ← Week 8: 7-language translation
│   └── 10_feedback_intelligence.ipynb ← Week 9: Feedback analytics
│
├── ui_ux/
│   ├── wireframes/                 ← UI/UX design files
│   └── assets/                     ← Static assets
│
├── docs/
│   ├── architecture.md             ← System architecture
│   └── prd_support_content.md      ← Technical design decisions
│
├── deployment/
│   └── streamlit_deployment.yml    ← Streamlit Cloud config
│
└── assets/
    └── sample_exports/             ← Generated brand kit samples
```

---

## ⚙️ Installation Instructions

### Prerequisites
- Python 3.10+
- Git
- A Gemini API key from [Google AI Studio](https://aistudio.google.com)

### Step 1: Clone the repository
```bash
git clone https://github.com/iblamehemer/og.git
cd og
```

### Step 2: Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set your Gemini API key
```bash
# Option A: Environment variable
export GEMINI_API_KEY="your_key_here"

# Option B: Streamlit secrets (create .streamlit/secrets.toml)
echo 'GEMINI_API_KEY = "your_key_here"' > .streamlit/secrets.toml
```

### Step 5: Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

> **Note:** All features work in **Demo Mode** without a Gemini API key. AI-powered features (taglines, narrative, translations) require a key.

---

## 📖 Usage Instructions

1. **Connect your API key** in the API Configuration bar at the top
2. **Tab 1 — Brand Inputs:** Enter your company name, industry, personality, tone, audience
3. **Tab 2 — Logo Studio:** Generate 5 logo styles, download SVG or PNG
4. **Tab 3 — Fonts & Palette:** View KMeans palette, check WCAG accessibility, get font pairings
5. **Tab 4 — Slogans:** Generate taglines, read brand narrative, run A/B scorer
6. **Tab 5 — Campaign Analytics:** Predict CTR/ROI/Engagement, view Plotly dashboard
7. **Tab 6 — Multilingual:** Translate to 7 languages with tone validation
8. **Tab 7 — Animation:** Generate 1080×1080 GIF animation, download
9. **Tabs 8–11:** Trend Radar, Launch Checklist, Competitor Gaps, Audience Personas
10. **Tab 12 — Feedback:** Rate each module (1–5 stars)
11. **Tab 13 — Download Kit:** Export full brand kit as ZIP

---

## 🤝 Contribution Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add: your feature description'`
4. Push to branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure:
- All new features include a test in `notebooks/05_integration_tests.ipynb`
- Code follows PEP 8 style guidelines
- New dependencies are added to `requirements.txt`

---

## 🙏 Acknowledgments

- **Google Gemini API** — Generative AI for taglines, narratives, and translations
- **scikit-learn** — KNN, Random Forest, KMeans, and Ridge regression implementations
- **Streamlit** — Web framework for rapid ML app deployment
- **Plotly** — Interactive data visualisation library
- **NLTK** — Natural language processing and TF-IDF retrieval
- **Pillow (PIL)** — GIF animation generation
- **CRS AI Capstone Programme** — Project framework and guidance
- **Google AI Studio** — Gemini API access and testing

---

## 📊 Screenshots & Demos

| Module | Description |
|---|---|
| Home Tab | Dark-themed dashboard with 10-week roadmap |
| Logo Studio | 5 geometric SVG logo styles with download |
| Fonts & Palette | KMeans colour swatches + WCAG contrast scores |
| Campaign Analytics | Plotly scatter chart + waterfall ROI chart |
| Multilingual Studio | 7-language translation with flag display |
| Animation Preview | 1080×1080 GIF with typewriter/fade/slide |
| Trend Radar | Momentum bars + Plotly bar chart |
| Audience Personas | 3-persona cards with pain points + triggers |

> Live demo: https://dxyqtqy2vmevept6gqz9qe.streamlit.app

---

## 📄 PRD Document

The full Product Requirements Document (PRD) is available in the `docs/` folder and submitted separately as a PDF to the evaluation panel.

---

*BrandSphere AI — CRS AI Capstone 2025–26 · Scenario 1: AI-Powered Automated Branding Assistant*
