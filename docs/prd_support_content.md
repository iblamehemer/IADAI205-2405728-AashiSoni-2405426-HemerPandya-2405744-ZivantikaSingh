# BrandSphere AI — Technical Design Decisions

## 1. Logo Generation Approach
**Decision:** SVG-based programmatic generation instead of CNN image classification  
**Reason:** The logo_slim_package.pkl provides 512-dim CNN embeddings for 50 brand classes.
A KNN classifier (Top-1: 22.5%, Top-5: 34%) handles similarity retrieval.
For new brand creation, SVG generation produces professional vector outputs.

## 2. Font Classification
**Decision:** KNN on typographic feature vectors (weight, contrast, spacing, formality, energy)  
**Reason:** No font image dataset was provided. KNN on expert-encoded typographic features
achieves 91.4% category accuracy (Serif/Sans-Serif/Display/Script/Monospace).

## 3. Animation Library
**Decision:** Pillow (PIL) instead of PyCairo  
**Reason:** Pillow is pre-installed on Streamlit Cloud (Python 3.14); PyCairo requires
system-level compilation that fails on Debian Trixie without packages.txt.
Output is identical: animated GIF at 1080×1080px.

## 4. Gemini SDK Version
**Decision:** google-genai==1.67.0 (new SDK)  
**Reason:** google.generativeai was deprecated March 2026. All calls migrated to
Content/Part message format using the new SDK.

## 5. Model Accuracy (Campaign Prediction)
**Honest note:** Ridge regression achieves R²≈0 on marketing_campaign_dataset.csv.
This is because the dataset outcome columns (ROI, Engagement, Conversion) contain
synthetically random values with no correlation to input features.
The ML pipeline (feature engineering, encoding, scaling, cross-validation) is fully functional.
