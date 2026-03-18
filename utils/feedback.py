"""
utils/feedback.py
BrandSphere AI — Feedback Collection, Storage & Sentiment Analysis
"""

import json
import os
import uuid
from datetime import datetime

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

# ─── Feedback Storage Path ────────────────────────────────────────────────────
FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'cleaned', 'feedback_data.json')

def analyze_sentiment(text):
    """Analyze sentiment of feedback comment."""
    if not text or not TEXTBLOB_AVAILABLE:
        return 'Neutral', 0.0
    try:
        polarity = TextBlob(str(text)).sentiment.polarity
        if polarity > 0.1:   return 'Positive', round(polarity, 3)
        elif polarity < -0.1: return 'Negative', round(polarity, 3)
        else:                 return 'Neutral',  round(polarity, 3)
    except Exception:
        return 'Neutral', 0.0

def save_feedback(module, star_rating, comment='', session_id=None):
    """Save a feedback record to local JSON store."""
    sentiment, polarity = analyze_sentiment(comment)
    record = {
        'session_id':  session_id or str(uuid.uuid4())[:8],
        'timestamp':   datetime.utcnow().isoformat(),
        'module':      module,
        'star_rating': int(star_rating),
        'comment':     str(comment),
        'sentiment':   sentiment,
        'polarity':    polarity,
    }
    try:
        os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
        records = load_all_feedback()
        records.append(record)
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(records, f, indent=2)
        return True, record
    except Exception as e:
        return False, str(e)

def load_all_feedback():
    """Load all feedback records from JSON store."""
    try:
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def get_feedback_stats():
    """Return summary statistics for the analytics dashboard."""
    records = load_all_feedback()
    if not records:
        return {
            'total': 0, 'avg_rating': 0,
            'sentiment_counts': {'Positive': 0, 'Neutral': 0, 'Negative': 0},
            'module_averages': {}, 'records': []
        }

    ratings    = [r['star_rating'] for r in records]
    sentiments = [r['sentiment'] for r in records]
    modules    = [r['module'] for r in records]

    module_ratings = {}
    for r in records:
        m = r['module']
        module_ratings.setdefault(m, []).append(r['star_rating'])

    return {
        'total':       len(records),
        'avg_rating':  round(sum(ratings) / len(ratings), 2),
        'sentiment_counts': {
            'Positive': sentiments.count('Positive'),
            'Neutral':  sentiments.count('Neutral'),
            'Negative': sentiments.count('Negative'),
        },
        'module_averages': {
            m: round(sum(v)/len(v), 2) for m, v in module_ratings.items()
        },
        'records': records
    }

def get_high_rated_samples(min_stars=4):
    """Return feedback records with high ratings for model retraining."""
    return [r for r in load_all_feedback() if r['star_rating'] >= min_stars]

def get_low_rated_samples(max_stars=2):
    """Return feedback records with low ratings for model improvement."""
    return [r for r in load_all_feedback() if r['star_rating'] <= max_stars]
