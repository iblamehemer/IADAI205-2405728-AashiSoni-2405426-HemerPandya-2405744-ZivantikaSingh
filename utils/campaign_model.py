"""
utils/campaign_model.py
BrandSphere AI — Campaign KPI Predictor
Predicts CTR, ROI, and Engagement Score using Random Forest models.
"""

import numpy as np
import pickle
import os

# ─── Label Maps ───────────────────────────────────────────────────────────────
PLATFORM_MAP   = {'Instagram': 0, 'Facebook': 1, 'Twitter/X': 2, 'LinkedIn': 3, 'TikTok': 4}
OBJECTIVE_MAP  = {'Brand Awareness': 0, 'Engagement': 1, 'Conversion': 2, 'Lead Generation': 3}
REGION_MAP     = {'North America': 0, 'Europe': 1, 'Asia': 2, 'Middle East': 3, 'Africa': 4, 'South America': 5}
INDUSTRY_MAP   = {'Tech': 0, 'Fashion': 1, 'Food': 2, 'Finance': 3, 'Health': 4, 'Education': 5}

# ─── Benchmark KPIs (industry averages for reference lines) ──────────────────
BENCHMARKS = {
    'ctr': {'Instagram': 3.8, 'Facebook': 2.9, 'Twitter/X': 1.5, 'LinkedIn': 2.1, 'TikTok': 5.2},
    'roi': {'Brand Awareness': 15, 'Engagement': 40, 'Conversion': 110, 'Lead Generation': 80},
    'engagement': {'Instagram': 65, 'Facebook': 55, 'Twitter/X': 42, 'LinkedIn': 48, 'TikTok': 75},
}

def encode_features(platform, objective, region, industry, budget_usd, duration_days):
    """Encode categorical + numeric features into model input vector."""
    p = PLATFORM_MAP.get(platform, 0)
    o = OBJECTIVE_MAP.get(objective, 0)
    r = REGION_MAP.get(region, 0)
    i = INDUSTRY_MAP.get(industry, 0)
    b = min(budget_usd / 50000.0, 1.0)   # MinMax scale 0–50k
    d = min(duration_days / 90.0, 1.0)   # MinMax scale 0–90 days
    return np.array([[p, o, r, i, b, d]])

def predict_kpis(platform, objective, region, industry, budget_usd, duration_days):
    """
    Predict CTR, ROI, and Engagement Score.
    Uses trained model if available, else uses calibrated formula.
    """
    model_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'campaign_models.pkl')

    # Try loading trained model first
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
            models = data['models']
            X = encode_features(platform, objective, region, industry, budget_usd, duration_days)
            return {
                'ctr':        round(float(models['ctr_percent'].predict(X)[0]), 2),
                'roi':        round(float(models['roi_percent'].predict(X)[0]), 1),
                'engagement': round(float(models['engagement_score'].predict(X)[0]), 1),
                'source': 'trained_model'
            }
        except Exception:
            pass

    # Calibrated formula fallback (always works without trained model)
    base_ctr = BENCHMARKS['ctr'].get(platform, 3.0)
    base_roi = BENCHMARKS['roi'].get(objective, 50)
    base_eng = BENCHMARKS['engagement'].get(platform, 55)

    budget_boost = np.log1p(budget_usd) / np.log1p(50000)
    duration_boost = min(duration_days / 30, 2.0)

    ctr = round(base_ctr * (0.8 + 0.4 * budget_boost), 2)
    roi = round(base_roi * (0.7 + 0.6 * duration_boost), 1)
    eng = round(base_eng * (0.75 + 0.5 * budget_boost), 1)

    return {
        'ctr':        min(max(ctr, 0.5), 12.0),
        'roi':        min(max(roi, -10), 400.0),
        'engagement': min(max(eng, 10), 100.0),
        'source': 'formula'
    }

def get_benchmarks(platform, objective):
    """Return industry benchmark values for comparison."""
    return {
        'ctr_benchmark':        BENCHMARKS['ctr'].get(platform, 3.0),
        'roi_benchmark':        BENCHMARKS['roi'].get(objective, 50),
        'engagement_benchmark': BENCHMARKS['engagement'].get(platform, 55),
    }

def get_performance_label(predicted, benchmark):
    """Return performance label compared to benchmark."""
    ratio = predicted / benchmark if benchmark > 0 else 1
    if ratio >= 1.2:   return '🟢 Above Average'
    elif ratio >= 0.9: return '🟡 On Target'
    else:              return '🔴 Below Average'
