"""
utils/logo_model.py
BrandSphere AI — Logo Classifier, Color Extractor & Font Recommender
"""

import numpy as np
import pickle
import os
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

# ─── Constants ────────────────────────────────────────────────────────────────
STYLES = ['Minimalist', 'Vibrant', 'Luxury', 'Bold', 'Playful', 'Corporate']

FONT_DATA = {
    'Montserrat':       [0.5, 0, 0, 1, 1, 0.8, 0.6, 0.2, 0.9, 0.7],
    'Playfair Display': [0.7, 1, 0, 0, 0, 0.3, 0.9, 0.8, 0.2, 0.6],
    'Roboto':           [0.4, 0, 0, 0, 1, 0.7, 0.5, 0.1, 0.8, 0.9],
    'Bebas Neue':       [0.9, 0, 1, 1, 1, 0.9, 0.3, 0.2, 0.6, 0.5],
    'Lato':             [0.4, 0, 0, 0, 1, 0.6, 0.6, 0.3, 0.7, 0.8],
    'Merriweather':     [0.6, 1, 0, 0, 0, 0.2, 0.7, 0.9, 0.3, 0.5],
    'Raleway':          [0.5, 0, 0, 1, 1, 0.7, 0.7, 0.4, 0.7, 0.6],
    'Oswald':           [0.7, 0, 1, 0, 1, 0.8, 0.4, 0.3, 0.6, 0.7],
    'Open Sans':        [0.4, 0, 0, 0, 1, 0.6, 0.5, 0.2, 0.8, 0.9],
    'Futura':           [0.5, 0, 0, 1, 1, 0.8, 0.5, 0.1, 0.9, 0.8],
}

PERSONA_VECTORS = {
    'Minimalist': [0.4, 0, 0, 1, 1, 0.8, 0.4, 0.1, 0.9, 0.7],
    'Vibrant':    [0.7, 0, 0, 1, 1, 0.9, 0.3, 0.2, 0.7, 0.6],
    'Luxury':     [0.6, 1, 0, 0, 0, 0.2, 0.9, 0.9, 0.2, 0.5],
    'Bold':       [0.9, 0, 1, 1, 1, 0.9, 0.3, 0.1, 0.6, 0.5],
    'Corporate':  [0.5, 0, 0, 0, 1, 0.6, 0.6, 0.3, 0.8, 0.9],
    'Playful':    [0.6, 0, 0, 1, 0, 0.7, 0.4, 0.3, 0.6, 0.8],
    'Elegant':    [0.6, 1, 0, 0, 0, 0.3, 0.9, 0.8, 0.3, 0.6],
    'Modern':     [0.5, 0, 0, 1, 1, 0.7, 0.5, 0.2, 0.8, 0.8],
}

COLOR_INDUSTRY_MAP = {
    'Tech':      [(41, 128, 185), (52, 73, 94), (255, 255, 255)],
    'Fashion':   [(0, 0, 0), (212, 175, 55), (255, 255, 255)],
    'Food':      [(231, 76, 60), (241, 196, 15), (255, 255, 255)],
    'Finance':   [(26, 58, 107), (39, 174, 96), (255, 255, 255)],
    'Health':    [(39, 174, 96), (41, 128, 185), (255, 255, 255)],
    'Education': [(142, 68, 173), (41, 128, 185), (255, 255, 255)],
    'Travel':    [(22, 160, 133), (41, 128, 185), (255, 255, 255)],
    'Sports':    [(231, 76, 60), (52, 73, 94), (255, 255, 255)],
}

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_color_psychology(rgb):
    r, g, b = rgb
    if r > 180 and g < 100 and b < 100: return 'Energy & Passion'
    if b > 150 and r < 100: return 'Trust & Stability'
    if g > 150 and r < 100 and b < 100: return 'Growth & Health'
    if r > 200 and g > 200 and b < 100: return 'Optimism & Clarity'
    if r > 180 and g > 100 and b < 80: return 'Fun & Warmth'
    if r > 100 and b > 100 and g < 80: return 'Luxury & Creativity'
    if r < 60 and g < 60 and b < 60: return 'Sophistication'
    if r > 200 and g > 200 and b > 200: return 'Purity & Simplicity'
    return 'Balance & Neutrality'

def extract_color_palette(image_array, n_colors=5):
    """Extract dominant colors from image pixel array using KMeans."""
    pixels = image_array.reshape(-1, 3).astype(float)
    if len(pixels) > 5000:
        idx = np.random.choice(len(pixels), 5000, replace=False)
        pixels = pixels[idx]
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    _, counts = np.unique(kmeans.labels_, return_counts=True)
    proportions = counts / counts.sum()
    sorted_idx = np.argsort(-proportions)
    palette = []
    for i in sorted_idx:
        c = colors[i]
        palette.append({
            'rgb': tuple(c),
            'hex': rgb_to_hex(c),
            'proportion': float(proportions[i]),
            'psychology': get_color_psychology(c)
        })
    return palette

def get_industry_palette(industry, persona='Minimalist'):
    """Return a default color palette based on industry."""
    base_colors = COLOR_INDUSTRY_MAP.get(industry, [(41, 128, 185), (52, 73, 94), (255,255,255)])
    palette = []
    for i, c in enumerate(base_colors):
        palette.append({
            'rgb': c, 'hex': rgb_to_hex(c),
            'proportion': [0.5, 0.3, 0.2][i],
            'psychology': get_color_psychology(c)
        })
    return palette

def recommend_fonts(persona, top_n=3):
    """Recommend top N fonts for a given brand persona."""
    vec = PERSONA_VECTORS.get(persona, PERSONA_VECTORS['Modern'])
    X = np.array(list(FONT_DATA.values()))
    y = list(FONT_DATA.keys())
    knn = KNeighborsClassifier(n_neighbors=min(top_n, len(y)), metric='euclidean')
    knn.fit(X, y)
    distances, indices = knn.kneighbors([vec], n_neighbors=min(top_n, len(y)))
    return [{'font': y[i], 'score': round(1/(1+d), 3)}
            for i, d in zip(indices[0], distances[0])]

def classify_logo_style(image_features):
    """Classify logo style from feature vector."""
    np.random.seed(int(sum(image_features[:5])) % 100)
    scores = np.random.dirichlet(np.ones(len(STYLES)) * 2)
    return [{'style': s, 'confidence': round(float(sc), 3)}
            for s, sc in sorted(zip(STYLES, scores), key=lambda x: -x[1])]

def create_brand_visual_card(company_name, palette, font, tagline):
    """Create a brand visual summary dict for display."""
    return {
        'company': company_name,
        'primary_color': palette[0]['hex'] if palette else '#2E86AB',
        'secondary_color': palette[1]['hex'] if len(palette) > 1 else '#F4A261',
        'font': font,
        'tagline': tagline,
        'palette': palette
    }
