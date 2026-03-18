# BrandSphere AI — System Architecture

## Overview
BrandSphere AI is a modular, tab-based Streamlit application integrating five core AI/ML modules.

## Architecture Diagram
```
User Input (Streamlit UI)
    │
    ├── src/config.py           ← Constants, industry mappings
    ├── src/palette_engine.py   ← KMeans colour extraction (scikit-learn)
    ├── src/logo_engine.py      ← SVG logo generation
    ├── src/font_engine.py      ← KNN font classification (scikit-learn)
    ├── src/slogan_engine.py    ← NLTK TF-IDF + Gemini API
    ├── src/animation_engine.py ← Pillow GIF generation
    ├── src/multilingual_engine.py ← Gemini API translation
    ├── src/campaign_predictor.py  ← Ridge regression (scikit-learn)
    ├── src/aesthetics_engine.py   ← Brand scoring
    ├── src/feedback_engine.py     ← CSV-based feedback loop
    ├── src/export_engine.py       ← ZIP brand kit builder
    └── src/dashboard_engine.py    ← Plotly chart generators
    │
    ├── models/
    │   ├── logo_classifier.pkl      ← KNN on 512-dim CNN embeddings
    │   ├── font_category_classifier.pkl ← KNN on font features (91.4% acc)
    │   ├── roi_model.pkl            ← Ridge regression (10 features)
    │   ├── engagement_model.pkl     ← Ridge regression
    │   └── conversion_model.pkl     ← Ridge regression
    │
    └── Streamlit Cloud Deployment
        └── https://dxyqtqy2vmevept6gqz9qe.streamlit.app
```

## Data Flow
1. User enters brand inputs (company, industry, personality, tone)
2. palette_engine generates 5-colour KMeans palette
3. logo_engine produces 5 SVG logo variants
4. font_engine recommends 3 font pairings via KNN classifier
5. slogan_engine generates 6 taglines (NLTK TF-IDF + Gemini)
6. animation_engine creates 1080×1080 GIF animation
7. campaign_predictor forecasts CTR, ROI, engagement
8. multilingual_engine translates content to 7 languages
9. export_engine bundles all assets into downloadable ZIP
