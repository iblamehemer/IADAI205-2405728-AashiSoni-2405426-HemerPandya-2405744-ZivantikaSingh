"""
app.py
------
BrandSphere AI — Main Streamlit Application
CRS AI Capstone 2025-26 | Scenario 1

Tabs:
  1. 🏠 Home
  2. 🎯 Brand Inputs
  3. 🎨 Logo Studio
  4. 🖋  Fonts & Palette
  5. ✍️  Slogans & Content
  6. 📣  Campaign Analytics
  7. 🌍  Multilingual Studio
  8. 🎬  Animation Preview
  9. ⭐  Feedback
  10. 📦  Download Kit
"""

import os, sys, uuid, json, re, time, datetime, logging
from typing import List, Dict, Optional
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ── Path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Streamlit page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="BrandSphere AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');
:root {
  --bg:#0C0D0F; --surface:#141518; --surface2:#1C1E22; --border:#2A2C31;
  --accent:#C9A84C; --accent2:#E8C97A; --teal:#3ECFB2; --red:#E05A5A;
  --text:#F0EDE8; --muted:#7A7A85;
  --font-head:'Cormorant Garamond',Georgia,serif;
  --font-body:'DM Sans',sans-serif;
  --font-mono:'Space Mono',monospace;
}
*, *::before, *::after { box-sizing:border-box; }
html, body, .stApp { background:var(--bg) !important; color:var(--text) !important; font-family:var(--font-body); }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:0 !important; max-width:100% !important; }
section[data-testid="stSidebar"] { display:none; }
::-webkit-scrollbar { width:4px; } ::-webkit-scrollbar-track { background:var(--bg); } ::-webkit-scrollbar-thumb { background:var(--accent); border-radius:2px; }
.nav-bar { display:flex; align-items:center; justify-content:space-between; padding:16px 48px; background:var(--surface); border-bottom:1px solid var(--border); }
.nav-logo { font-family:var(--font-head); font-size:1.6rem; font-weight:700; color:var(--accent); letter-spacing:0.03em; }
.nav-logo span { color:var(--text); font-weight:300; }
.nav-tag  { font-family:var(--font-mono); font-size:0.62rem; color:var(--muted); letter-spacing:0.15em; text-transform:uppercase; }
.hero { background:linear-gradient(135deg,#0C0D0F 0%,#141518 60%,#0f1015 100%); padding:80px 48px 56px; border-bottom:1px solid var(--border); position:relative; overflow:hidden; }
.hero::before { content:''; position:absolute; top:-60px; right:-60px; width:500px; height:500px; background:radial-gradient(circle,rgba(201,168,76,0.08) 0%,transparent 70%); pointer-events:none; }
.hero-eyebrow { font-family:var(--font-mono); font-size:0.7rem; letter-spacing:0.25em; color:var(--accent); text-transform:uppercase; margin-bottom:16px; }
.hero-title { font-family:var(--font-head); font-size:clamp(2.6rem,5vw,4.6rem); font-weight:300; line-height:1.08; margin-bottom:12px; }
.hero-title em { font-style:italic; color:var(--accent); }
.hero-sub { font-size:1rem; font-weight:300; color:var(--muted); max-width:540px; line-height:1.72; margin-bottom:36px; }
.badge-row { display:flex; gap:10px; flex-wrap:wrap; }
.badge { display:inline-block; padding:5px 14px; border:1px solid var(--border); border-radius:20px; font-family:var(--font-mono); font-size:0.6rem; color:var(--muted); letter-spacing:0.1em; }
.stTabs [data-baseweb="tab-list"] { background:var(--surface) !important; border-bottom:1px solid var(--border) !important; padding:0 48px !important; gap:0 !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; border:none !important; color:var(--muted) !important; font-family:var(--font-mono) !important; font-size:0.65rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; padding:15px 18px !important; margin:0 !important; transition:color 0.2s !important; }
.stTabs [aria-selected="true"] { color:var(--accent) !important; border-bottom:2px solid var(--accent) !important; }
.stTabs [data-baseweb="tab-panel"] { padding:36px 48px !important; background:var(--bg) !important; }
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div { background:var(--surface2) !important; border:1px solid var(--border) !important; border-radius:6px !important; color:var(--text) !important; font-family:var(--font-body) !important; font-size:0.92rem !important; }
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus { border-color:var(--accent) !important; box-shadow:0 0 0 2px rgba(201,168,76,0.15) !important; }
label, .stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label, .stRadio label { color:var(--muted) !important; font-family:var(--font-mono) !important; font-size:0.62rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; }
.stButton>button { background:var(--accent) !important; color:#0C0D0F !important; border:none !important; border-radius:4px !important; font-family:var(--font-mono) !important; font-size:0.68rem !important; font-weight:700 !important; letter-spacing:0.15em !important; text-transform:uppercase !important; padding:11px 26px !important; transition:all 0.2s !important; }
.stButton>button:hover { background:var(--accent2) !important; transform:translateY(-1px) !important; box-shadow:0 4px 18px rgba(201,168,76,0.3) !important; }
.stDownloadButton>button { background:transparent !important; color:var(--accent) !important; border:1px solid var(--accent) !important; border-radius:4px !important; font-family:var(--font-mono) !important; font-size:0.68rem !important; font-weight:700 !important; letter-spacing:0.15em !important; text-transform:uppercase !important; padding:11px 26px !important; }
.stDownloadButton>button:hover { background:rgba(201,168,76,0.1) !important; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:26px; margin-bottom:14px; }
.card:hover { border-color:rgba(201,168,76,0.35); }
.card-title { font-family:var(--font-head); font-size:1.25rem; font-weight:600; color:var(--text); margin-bottom:5px; }
.card-sub { font-size:0.82rem; color:var(--muted); line-height:1.65; margin-bottom:16px; }
.sec-label { font-family:var(--font-mono); font-size:0.6rem; letter-spacing:0.25em; color:var(--accent); text-transform:uppercase; margin-bottom:7px; }
.sec-title { font-family:var(--font-head); font-size:1.9rem; font-weight:300; color:var(--text); margin-bottom:5px; }
.sec-title em { font-style:italic; color:var(--accent); }
.divider { height:1px; background:var(--border); margin:28px 0; }
.metric-card { background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:20px; text-align:center; }
.metric-val { font-family:var(--font-head); font-size:2.2rem; font-weight:700; color:var(--accent); display:block; }
.metric-lbl { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.15em; color:var(--muted); text-transform:uppercase; margin-top:3px; }
.swatch-row { display:flex; gap:8px; margin:14px 0; }
.swatch { flex:1; height:50px; border-radius:6px; display:flex; align-items:flex-end; padding:5px 8px; font-family:var(--font-mono); font-size:0.52rem; color:rgba(255,255,255,0.75); }
.tagline-card { background:var(--surface2); border-left:3px solid var(--accent); padding:15px 18px; border-radius:0 8px 8px 0; margin:7px 0; font-family:var(--font-head); font-size:1.1rem; font-style:italic; color:var(--text); line-height:1.55; }
.lang-card { background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:14px 18px; margin:5px 0; }
.lang-name { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.15em; color:var(--accent); text-transform:uppercase; margin-bottom:4px; }
.lang-text { font-family:var(--font-head); font-size:1rem; font-style:italic; color:var(--text); }
.pill { display:inline-block; padding:3px 11px; border-radius:20px; font-family:var(--font-mono); font-size:0.57rem; letter-spacing:0.1em; text-transform:uppercase; }
.pill-g { background:rgba(62,207,178,0.15); color:#3ECFB2; border:1px solid rgba(62,207,178,0.3); }
.pill-a { background:rgba(201,168,76,0.15); color:#C9A84C; border:1px solid rgba(201,168,76,0.3); }
.pill-r { background:rgba(224,90,90,0.15); color:#E05A5A; border:1px solid rgba(224,90,90,0.3); }
.prog-wrap { background:var(--surface2); border-radius:4px; height:8px; overflow:hidden; margin:7px 0; }
.prog-bar { height:100%; border-radius:4px; background:linear-gradient(90deg,var(--accent),var(--teal)); transition:width 0.6s ease; }
.check-item { display:flex; align-items:flex-start; gap:10px; padding:9px 0; border-bottom:1px solid var(--border); }
.logo-svg-wrap { border:2px solid var(--border); border-radius:10px; padding:16px; background:var(--surface2); cursor:pointer; transition:border-color 0.2s; display:flex; flex-direction:column; align-items:center; gap:8px; }
.logo-svg-wrap:hover { border-color:var(--accent); }
.logo-svg-wrap.selected { border-color:var(--accent); background:rgba(201,168,76,0.06); }
.nltk-pill { display:inline-block; padding:3px 10px; border-radius:14px; font-family:var(--font-mono); font-size:0.55rem; background:rgba(201,168,76,0.12); color:var(--accent); border:1px solid rgba(201,168,76,0.25); margin:2px; }
.stAlert { background:var(--surface2) !important; border:1px solid var(--border) !important; }
.stSpinner>div { border-top-color:var(--accent) !important; }
@media (max-width:640px) { .stTabs [data-baseweb="tab-panel"] { padding:20px !important; } .hero { padding:40px 20px 36px; } }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
def _init():
    defaults = {
        "session_id":    str(uuid.uuid4())[:8],
        "brand_inputs":  {},
        "logos":         [],
        "selected_logo": 0,
        "palette":       {},
        "fonts":         [],
        "slogans":       [],
        "retrieved":     [],
        "brand_story":   "",
        "translations":  {},
        "campaigns":     {},
        "kpis":          {},
        "aesthetics":    {},
        "gif_bytes":     None,
        "feedback_log":  [],
        "gemini_ok":     False,
        "api_key":       "",
        "chat_history":  [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ── Gemini config ──────────────────────────────────────────────────────────
def configure_gemini(key: str) -> bool:
    """Accept any non-empty key — validation happens on first real API call."""
    key = (key or "").strip()
    if not key:
        return False
    st.session_state.gemini_ok  = True
    st.session_state.api_key    = key
    os.environ["GEMINI_API_KEY"] = key
    return True

def gemini_call(prompt: str, system: str = "") -> str:
    """Call Gemini API using google-genai SDK v1.x"""
    if not st.session_state.gemini_ok:
        return ""
    try:
        from google import genai as _genai
        from google.genai import types as _types

        client = _genai.Client(api_key=st.session_state.api_key)

        # Build contents — prepend system as a user message if provided
        contents = []
        if system:
            contents.append(_types.Content(
                role="user",
                parts=[_types.Part(text="[System context]: " + system)]
            ))
            contents.append(_types.Content(
                role="model",
                parts=[_types.Part(text="Understood. I will follow those instructions.")]
            ))
        contents.append(_types.Content(
            role="user",
            parts=[_types.Part(text=prompt)]
        ))

        resp = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=_types.GenerateContentConfig(
                temperature=0.8,
                max_output_tokens=1500,
            ),
        )
        # Extract text safely from response
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()
        # Fallback extraction
        for candidate in getattr(resp, "candidates", []):
            for part in getattr(candidate.content, "parts", []):
                if hasattr(part, "text") and part.text:
                    return part.text.strip()
        return ""
    except Exception as e:
        return ""


# ── Import src modules ─────────────────────────────────────────────────────
from src.config import (
    INDUSTRIES, PERSONALITIES, TONES, PLATFORMS,
    REGIONS, LANGUAGES_SUPPORTED, CAMPAIGN_OBJECTIVES, COLOR_NAMES,
    COLOR_PSYCHOLOGY,
)
from src.palette_engine    import generate_palette, score_palette_harmony
from src.font_engine       import recommend_fonts
from src.logo_engine       import generate_all_logos, svg_to_png_bytes
from src.slogan_engine     import generate_slogans, nltk_analyze
from src.aesthetics_engine import score_brand, gemini_recommendations
from src.multilingual_engine import translate_slogan, validate_translations
from src.animation_engine  import create_brand_gif
from src.feedback_engine   import save_feedback, load_feedback, get_summary
from src.export_engine     import build_brand_kit_zip
from src.dashboard_engine  import (
    kpi_bar_chart, regional_engagement_map,
    personality_radar, feedback_bar, feedback_pie, campaign_scatter,
)


@st.cache_resource
def get_predictor():
    from src.campaign_predictor import predictor
    predictor._load()
    return predictor

# ── Campaign content helper ────────────────────────────────────────────────
DEMO_CAMPAIGN = {
    "caption": "Introducing {company} — where {industry} meets intelligent design.\nBuilt for the future. Crafted for you. {tag}\n👉 Tap the link.",
    "hashtags": ["#{co}", "#BrandStrategy", "#AIBranding", "#Innovation", "#DigitalMarketing",
                 "#BrandIdentity", "#StartupLife", "#MarketingAI", "#GrowthHacking", "#ProductLaunch"],
    "regional_strategy": "Focus on culturally resonant visuals and localized CTAs for {region}.",
}

def generate_campaign_content(bi, platform, region, objective):
    co  = bi.get("company", "Brand")
    ind = bi.get("industry", "Technology")
    tag = st.session_state.slogans[0]["text"] if st.session_state.slogans else f"Discover {co}"
    if st.session_state.gemini_ok:
        prompt = (
            f"Create a {platform} marketing campaign.\n"
            f"Company: {co} | Industry: {ind} | Objective: {objective} | Region: {region}\n"
            f"Tagline: \"{tag}\"\n\n"
            "Return JSON only: {\"caption\":\"...\",\"hashtags\":[\"...\"],\"regional_strategy\":\"...\"}"
        )
        raw = gemini_call(prompt)
        try:
            return json.loads(re.sub(r"```json|```", "", raw).strip())
        except Exception:
            pass
    return {
        "caption": DEMO_CAMPAIGN["caption"].format(company=co, industry=ind.lower(), tag=tag),
        "hashtags": [h.replace("{co}", co.replace(" ","")) for h in DEMO_CAMPAIGN["hashtags"]],
        "regional_strategy": DEMO_CAMPAIGN["regional_strategy"].format(region=region),
    }

def generate_brand_story(bi):
    co  = bi.get("company","Your Brand")
    ind = bi.get("industry","your industry")
    tone= bi.get("tone","professional")
    aud = bi.get("audience","modern professionals")

    # Always-ready fallback (shown when Gemini is off or returns empty)
    fallback = (
        co + " was built with one conviction: that great brands don't happen by accident — "
        "they are engineered with intention.\n\n"
        "In the competitive " + ind.lower() + " landscape, standing out requires more than a logo. "
        "It demands a voice that resonates, a visual identity that commands attention, "
        "and a message that converts.\n\n"
        "Every design decision, every word, every colour choice is a deliberate act of "
        "strategic storytelling. Built for " + (aud or "the people who matter most") + ".\n\n"
        "This is " + co + ". This is your story. Tell it boldly."
    )

    if st.session_state.gemini_ok:
        result = gemini_call(
            "Write a 110-word brand narrative for " + co + " in the " + ind + " industry. "
            "Tone: " + tone + ". Target audience: " + (aud or "modern consumers") + ". "
            "Write in second person ('Your brand...'). Be specific and inspiring.",
            system="You are an expert brand narrative writer. Be vivid and specific, never generic."
        )
        if result and len(result) > 20:   # only use if we got real content
            return result

    return fallback  # always returns non-empty string

# ══════════════════════════════════════════════════════════════════════════════
#  NEW FEATURE HELPERS
# ══════════════════════════════════════════════════════════════════════════════

# ── Brand Name Generator ───────────────────────────────────────────────────────
def generate_brand_names(industry: str, personality: str, keywords: str) -> List[Dict]:
    """Generate creative brand name suggestions."""
    if st.session_state.gemini_ok:
        pers_lower = personality.lower()
        kw_str     = keywords or "none"
        prompt_bn  = (
            f"Generate 8 creative, memorable brand names for a {pers_lower} {industry} company. "
            f"Keywords to consider: {kw_str}. "
            "For each name give: the name, a 1-line rationale, and a domain availability note. "
            "Return JSON only: array of objects with keys name, rationale, domain."
        )
        raw = gemini_call(prompt_bn)
        try:
            import re as _re
            data = json.loads(_re.sub(r"```json|```","",raw).strip())
            return data if isinstance(data, list) else []
        except Exception:
            pass
    # Offline fallback
    prefixes = {"Minimalist":["Clear","Pure","Axe","Arc","Mono"],
                "Luxury":["Lumé","Auré","Velux","Prism","Onyx"],
                "Bold":["Apex","Forge","Blaze","Titan","Surge"],
                "Vibrant":["Zest","Spark","Vivid","Nova","Flare"],
                "Professional":["Nexus","Vector","Axiom","Core","Strata"],
                "Playful":["Poppy","Ziggy","Bubbl","Whirl","Sunny"],
                "Elegant":["Seré","Luma","Crest","Elara","Muse"]}
    import random
    pfx = prefixes.get(personality, prefixes["Professional"])
    ind_short = industry.split("/")[0].strip().replace(" ","")[:5]
    names = []
    for p in random.sample(pfx, min(5, len(pfx))):
        names.append({"name": p + ind_short[:3].title(),
                      "rationale": f"Combines '{p}' energy with {industry.split('/')[0].strip().lower()} identity.",
                      "domain": f"{p.lower()}{ind_short.lower()}.com — check availability"})
    return names


# ── Color Accessibility Checker (WCAG) ────────────────────────────────────────
def check_wcag(palette: dict) -> List[Dict]:
    """Check WCAG contrast ratios between palette color pairs."""
    from src.palette_engine import hex_to_rgb

    def relative_luminance(rgb):
        r, g, b = [v/255 for v in rgb]
        def linearize(c):
            return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
        return 0.2126*linearize(r) + 0.7152*linearize(g) + 0.0722*linearize(b)

    def contrast_ratio(l1, l2):
        lighter, darker = max(l1,l2), min(l1,l2)
        return round((lighter+0.05)/(darker+0.05), 2)

    colors = list(palette.items())
    results = []
    pairs = [(0,3),(0,2),(1,3),(1,4),(0,4)]  # primary/bg, primary/accent etc
    for i, j in pairs:
        if i < len(colors) and j < len(colors):
            n1, v1 = colors[i]; n2, v2 = colors[j]
            l1 = relative_luminance(hex_to_rgb(v1["hex"]))
            l2 = relative_luminance(hex_to_rgb(v2["hex"]))
            cr = contrast_ratio(l1, l2)
            aa   = "✅ Pass" if cr >= 4.5 else "⚠️ Fail"
            aaa  = "✅ Pass" if cr >= 7.0 else "⚠️ Fail"
            results.append({"pair": f"{n1} on {n2}",
                             "hex1": v1["hex"], "hex2": v2["hex"],
                             "ratio": cr, "AA": aa, "AAA": aaa})
    return results


# ── A/B Tagline Tester ─────────────────────────────────────────────────────────
def ab_test_taglines(taglines: List[Dict], industry: str, audience: str) -> List[Dict]:
    """Score taglines across 5 brand dimensions."""
    if st.session_state.gemini_ok and taglines:
        texts_str = " | ".join([s["text"] for s in taglines[:4]])
        aud_str   = audience or "general consumers"
        prompt_ab = (
            "Score these brand taglines for a " + industry + " brand targeting " + aud_str + ". "
            "Taglines: " + texts_str + ". "
            "Score each tagline from 1-10 on: Memorability, Clarity, Emotional Impact, Brand Fit, Uniqueness. "
            "Return a JSON array only. Each item must have keys: tagline, memorability, clarity, "
            "emotional_impact, brand_fit, uniqueness, overall (average of the 5 scores)."
        )
        raw = gemini_call(prompt_ab)
        try:
            import re as _re
            data = json.loads(_re.sub(r"```json|```", "", raw).strip())
            return data if isinstance(data, list) else []
        except Exception:
            pass
    import hashlib
    results = []
    for s in taglines[:4]:
        text = s["text"]
        h    = int(hashlib.md5(text.encode()).hexdigest(), 16) % 100
        mem  = min(10, max(5, 7 + (h % 4) - 1))
        cla  = min(10, max(5, 6 + (h % 5) - 1))
        emo  = min(10, max(5, 7 + (h % 3)))
        fit  = min(10, max(5, 8 + (h % 2) - 1))
        uni  = min(10, max(5, 6 + (h % 4)))
        results.append({"tagline": text[:50],
                        "memorability": mem, "clarity": cla,
                        "emotional_impact": emo, "brand_fit": fit,
                        "uniqueness": uni, "overall": round((mem+cla+emo+fit+uni)/5, 1)})
    return sorted(results, key=lambda x: -x["overall"])

# ── Social Media Post Previewer ────────────────────────────────────────────────
def generate_post_preview(company, industry, personality, platform, slogan, palette):
    """Generate platform-specific post content and preview data."""
    platforms_meta = {
        "Instagram": {"char_limit": 2200, "best_format": "Square image + carousel",
                      "cta": "👉 Link in bio", "hashtag_count": "10-15"},
        "LinkedIn":  {"char_limit": 3000, "best_format": "Article or document post",
                      "cta": "See more in comments", "hashtag_count": "3-5"},
        "Twitter/X": {"char_limit": 280,  "best_format": "Text + image",
                      "cta": "RT if you agree", "hashtag_count": "2-3"},
        "Facebook":  {"char_limit": 500,  "best_format": "Video or link post",
                      "cta": "Share with your network", "hashtag_count": "5-10"},
        "TikTok":    {"char_limit": 150,  "best_format": "Short vertical video 9:16",
                      "cta": "Sound on", "hashtag_count": "5-8"},
        "YouTube":   {"char_limit": 5000, "best_format": "Long-form video",
                      "cta": "Subscribe for more", "hashtag_count": "3-5"},
    }
    meta    = platforms_meta.get(platform, platforms_meta["Instagram"])
    colors  = list(palette.values())
    primary = colors[0]["hex"] if colors else "#1B3A6B"
    accent  = colors[1]["hex"] if len(colors) > 1 else "#C9A84C"

    if st.session_state.gemini_ok:
        char_lim = str(meta["char_limit"])
        prompt_post = (
            "Write a " + platform + " marketing post for " + company + " (" + industry + ", " + personality + " brand). "
            "Tagline: " + slogan + ". Character limit: " + char_lim + ". "
            "Include a caption, 5 relevant hashtags, a CTA, and a scroll-stopping hook. "
            "Return JSON only with keys: caption, hashtags (array), cta, hook."
        )
        raw = gemini_call(prompt_post)
        try:
            import re as _re
            data = json.loads(_re.sub(r"```json|```", "", raw).strip())
            data.update(meta)
            data["primary"] = primary
            data["accent"]  = accent
            return data
        except Exception:
            pass

    co_tag  = company.replace(" ", "")
    ind_tag = industry.split("/")[0].strip().replace(" ", "")
    return {
        "caption":  "Introducing " + company + " — " + slogan + "\n\nBuilt for tomorrow. Designed for today. " +
                    "Discover why leaders in " + industry.lower() + " trust us.\n\n" + meta["cta"],
        "hashtags": ["#" + co_tag, "#" + ind_tag, "#BrandLaunch", "#Innovation", "#AI"],
        "cta":      meta["cta"],
        "hook":     "What if " + industry.lower() + " could work smarter for you?",
        "primary":  primary,
        "accent":   accent,
        **meta,
    }

# ── Nano Banana Pro Logo Generator ───────────────────────────────────────────
# ── Nano Banana Pro Logo Generator ───────────────────────────────────────────
def generate_logo_nano_banana(company: str, industry: str, personality: str,
                               palette: dict, style: str = "minimalist") -> Optional[bytes]:
    """
    Generate an AI logo image using Nano Banana / Gemini Image models.
    Tries all known model IDs in order. Returns PNG bytes or None.

    Model priority (March 2026):
      1. gemini-2.5-flash-preview-05-20  (Nano Banana 2 — widest availability)
      2. gemini-2.0-flash-preview-image-generation  (Nano Banana original)
      3. gemini-2.0-flash-exp  (experimental flash with image output)
      4. imagen-3.0-generate-002  (Imagen 3 fallback)
    """
    if not st.session_state.gemini_ok:
        return None

    colors    = list(palette.values())
    primary   = colors[0]["hex"] if colors else "#1B3A6B"
    secondary = colors[1]["hex"] if len(colors) > 1 else "#C9A84C"

    prompt = (
        "Create a professional " + style + " brand logo for '"
        + company + "'. Industry: " + industry + ". "
        "Brand personality: " + personality + ". "
        "Use primary color " + primary + " and accent " + secondary + ". "
        "White or transparent background. Clean vector-style design. "
        "Include the company name '" + company + "' with elegant typography. "
        "No decorative elements other than the logo mark and name. "
        "Output a single logo on a plain white background."
    )

    # All known Gemini image model IDs as of March 2026
    models_to_try = [
        "gemini-2.5-flash-preview-05-20",           # Nano Banana 2 (newest, fastest, widest availability)
        "gemini-2.0-flash-preview-image-generation", # Nano Banana original
        "gemini-2.0-flash-exp",                      # Experimental flash
        "imagen-3.0-generate-002",                   # Imagen 3
    ]

    try:
        from google import genai as _gi
        from google.genai import types as _gt
        client = _gi.Client(api_key=st.session_state.api_key)

        for model_name in models_to_try:
            try:
                resp = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=_gt.GenerateContentConfig(
                        response_modalities=["IMAGE", "TEXT"],
                    ),
                )
                # Extract image bytes — handle both bytes and base64 string
                for candidate in getattr(resp, "candidates", []):
                    for part in getattr(candidate.content, "parts", []):
                        if hasattr(part, "inline_data") and part.inline_data:
                            import base64 as _b64
                            data = part.inline_data.data
                            if isinstance(data, (bytes, bytearray)):
                                return bytes(data)
                            if isinstance(data, str):
                                return _b64.b64decode(data)
            except Exception:
                continue  # model unavailable in this region — try next

    except Exception:
        pass

    return None




# ── Dark / Light Palette Switcher ────────────────────────────────────────────
def switch_palette_mode(palette: dict, mode: str) -> dict:
    """Convert palette to dark or light mode variant."""
    from src.palette_engine import hex_to_rgb, rgb_to_hex, adjust_saturation
    import colorsys

    def lighten(hex_c, amount=0.4):
        r, g, b = [v/255 for v in hex_to_rgb(hex_c)]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        v2 = min(1.0, v + amount)
        r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v2)
        return rgb_to_hex([r2*255, g2*255, b2*255])

    def darken(hex_c, amount=0.4):
        r, g, b = [v/255 for v in hex_to_rgb(hex_c)]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        v2 = max(0.0, v - amount)
        r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v2)
        return rgb_to_hex([r2*255, g2*255, b2*255])

    new_palette = {}
    for name, v in palette.items():
        hex_c = v["hex"]
        if mode == "Dark Mode":
            if name in ["Background", "Text / CTA"]:
                new_hex = darken(hex_c, 0.5) if name == "Background" else lighten(hex_c, 0.5)
            else:
                new_hex = adjust_saturation(hex_c, 1.15)
        else:  # Light Mode
            if name == "Background":
                new_hex = "#F8F6F2"
            elif name == "Text / CTA":
                new_hex = "#1A1A1A"
            else:
                new_hex = adjust_saturation(hex_c, 0.9)
        new_palette[name] = {**v, "hex": new_hex}
    return new_palette


# ── Campaign ROI Calculator ──────────────────────────────────────────────────
def calculate_roi(budget: float, platform: str, objective: str,
                   audience_size: int, personality: str) -> dict:
    """
    Project campaign ROI from budget input.
    Uses industry benchmark CPMs and conversion rates.
    """
    cpm_benchmarks = {
        "Instagram": 8.5, "Facebook": 6.2, "Twitter/X": 5.8,
        "LinkedIn": 28.0, "TikTok": 9.0, "YouTube": 12.0,
    }
    conv_benchmarks = {
        "Brand Awareness": 0.008, "Engagement": 0.025,
        "Lead Generation": 0.045, "Conversion": 0.032, "Retention": 0.055,
    }
    pers_mult = {
        "Vibrant": 1.22, "Bold": 1.18, "Minimalist": 0.95,
        "Luxury": 1.08, "Elegant": 1.05, "Playful": 1.15, "Professional": 1.0,
    }

    cpm  = cpm_benchmarks.get(platform, 8.0)
    cr   = conv_benchmarks.get(objective, 0.02)
    mult = pers_mult.get(personality, 1.0)

    impressions     = int((budget / cpm) * 1000 * mult)
    clicks          = int(impressions * 0.028 * mult)
    conversions     = int(clicks * cr)
    revenue_est     = conversions * 45  # avg $45 revenue per conversion
    roi_pct         = round(((revenue_est - budget) / budget) * 100, 1)
    cost_per_click  = round(budget / max(clicks, 1), 2)
    cost_per_conv   = round(budget / max(conversions, 1), 2)

    breakeven_budget = round(revenue_est / max(1 + roi_pct/100, 0.01), 2)

    return {
        "impressions":      impressions,
        "clicks":           clicks,
        "conversions":      conversions,
        "revenue_est":      revenue_est,
        "roi_pct":          roi_pct,
        "cost_per_click":   cost_per_click,
        "cost_per_conv":    cost_per_conv,
        "breakeven":        breakeven_budget,
        "budget":           budget,
        "platform":         platform,
        "note":             "Estimates based on industry benchmark CPMs. Actual results vary.",
    }



# ── Trend Radar ───────────────────────────────────────────────────────────────
def generate_trend_radar(industry: str, personality: str, company: str) -> dict:
    """
    Scan industry trends and generate brand-specific response strategies.
    Returns structured trend data with actionable brand recommendations.
    """
    # Rich offline fallback — curated by industry
    TRENDS = {
        "Technology / Software": [
            {"trend": "AI-Native Products", "momentum": 95, "direction": "↑",
             "insight": "Users expect AI built-in, not bolted on. Position your brand as intelligence-first."},
            {"trend": "Privacy-First Design", "momentum": 82, "direction": "↑",
             "insight": "GDPR fatigue is shifting to trust marketing. Make privacy a feature, not a footnote."},
            {"trend": "No-Code / Low-Code", "momentum": 78, "direction": "↑",
             "insight": "Democratisation of tech is your opportunity to lead the 'accessible innovation' narrative."},
            {"trend": "Subscription Fatigue", "momentum": 71, "direction": "↓",
             "insight": "Offer transparent value bundling. Brands winning here lead with outcomes, not features."},
        ],
        "Fashion / Apparel": [
            {"trend": "Slow Fashion Movement", "momentum": 88, "direction": "↑",
             "insight": "Quality over quantity is the new luxury signal. Lead with craftsmanship and longevity."},
            {"trend": "Digital Fashion / NFT Wearables", "momentum": 65, "direction": "↑",
             "insight": "Early adopters are building digital wardrobes. A digital capsule collection could differentiate."},
            {"trend": "Size Inclusivity", "momentum": 91, "direction": "↑",
             "insight": "Inclusivity is no longer optional — it is a baseline brand expectation for Gen Z buyers."},
            {"trend": "Fast Fashion Backlash", "momentum": 84, "direction": "↑",
             "insight": "Transparency in supply chain is your biggest trust builder. Show your process."},
        ],
        "Food & Beverage": [
            {"trend": "Functional Foods & Drinks", "momentum": 89, "direction": "↑",
             "insight": "Consumers want food that does more — energy, immunity, mood. Lead with benefit-first messaging."},
            {"trend": "Plant-Based Mainstream", "momentum": 85, "direction": "↑",
             "insight": "Plant-based is no longer niche. Frame your brand in the 'better choices' conversation."},
            {"trend": "Hyper-Local Sourcing", "momentum": 76, "direction": "↑",
             "insight": "Local origin stories drive premium pricing. Your geography is a brand asset."},
            {"trend": "Alcohol-Free Alternatives", "momentum": 80, "direction": "↑",
             "insight": "'Mindful drinking' is a growth category. If relevant, stake your claim early."},
        ],
        "Healthcare": [
            {"trend": "Preventive Health Tech", "momentum": 92, "direction": "↑",
             "insight": "Consumers are shifting from reactive to proactive care. Lead with empowerment messaging."},
            {"trend": "Mental Health Mainstreaming", "momentum": 94, "direction": "↑",
             "insight": "Mental wellness is the fastest-growing health segment. Destigmatise in your brand language."},
            {"trend": "Telehealth Normalisation", "momentum": 87, "direction": "↑",
             "insight": "Digital-first healthcare is the expectation now. Position around accessibility and convenience."},
            {"trend": "Wearable Health Data", "momentum": 79, "direction": "↑",
             "insight": "Consumers own their health data. Build brand trust around data transparency."},
        ],
        "Finance": [
            {"trend": "Embedded Finance", "momentum": 86, "direction": "↑",
             "insight": "Finance is moving into every app. Position your brand around seamless integration."},
            {"trend": "ESG Investing", "momentum": 83, "direction": "↑",
             "insight": "Impact investing is mainstream. Lead with values alignment, not just returns."},
            {"trend": "Gen Z Financial Literacy", "momentum": 88, "direction": "↑",
             "insight": "The next generation wants education with their banking. Build a brand that teaches."},
            {"trend": "Crypto & DeFi Maturity", "momentum": 68, "direction": "→",
             "insight": "Volatility fatigue is real. Brands winning here lead with stability and education."},
        ],
        "Education": [
            {"trend": "Micro-Credentials & Nano-Degrees", "momentum": 91, "direction": "↑",
             "insight": "Short, stackable qualifications beat long degrees for working adults. Lead with speed-to-skill."},
            {"trend": "AI Tutoring", "momentum": 93, "direction": "↑",
             "insight": "Personalised learning at scale is the new standard. Position your brand as adaptive."},
            {"trend": "Skills Gap Economy", "momentum": 89, "direction": "↑",
             "insight": "Employers care about skills, not just degrees. Frame outcomes in career ROI language."},
            {"trend": "Gamification Fatigue", "momentum": 62, "direction": "↓",
             "insight": "Shallow gamification is losing trust. Go deeper — build genuine engagement loops."},
        ],
        "Retail / E-commerce": [
            {"trend": "Social Commerce", "momentum": 92, "direction": "↑",
             "insight": "TikTok Shop and Instagram checkout are changing where purchase decisions happen."},
            {"trend": "Hyper-Personalisation", "momentum": 88, "direction": "↑",
             "insight": "Generic recommendations are dead. Brand loyalty now requires 1:1 personalisation at scale."},
            {"trend": "Recommerce / Resale", "momentum": 84, "direction": "↑",
             "insight": "Secondary markets are a brand loyalty tool. Build a trade-in or resale programme."},
            {"trend": "Same-Day Delivery Expectation", "momentum": 79, "direction": "↑",
             "insight": "Speed is table stakes. Your brand story must include logistics transparency."},
        ],
        "Sustainability / Green Tech": [
            {"trend": "Carbon Accountability", "momentum": 94, "direction": "↑",
             "insight": "Carbon claims without data are liability. Lead with verified, third-party measurement."},
            {"trend": "Green Hydrogen", "momentum": 71, "direction": "↑",
             "insight": "Industrial decarbonisation is the next frontier. Early positioning here builds thought leadership."},
            {"trend": "Circular Economy", "momentum": 87, "direction": "↑",
             "insight": "End-of-life product thinking is becoming a purchase criterion for B2B buyers."},
            {"trend": "Greenwashing Backlash", "momentum": 90, "direction": "↑",
             "insight": "Vague eco-claims are now a legal and reputational risk. Specificity is your brand moat."},
        ],
    }

    fallback_trends = TRENDS.get(industry, [
        {"trend": "AI Integration", "momentum": 91, "direction": "↑",
         "insight": "Every industry is being reshaped by AI. Lead with intelligent automation narrative."},
        {"trend": "Experience Economy", "momentum": 85, "direction": "↑",
         "insight": "Customers buy experiences, not just products. Invest in brand touchpoint design."},
        {"trend": "Creator Economy", "momentum": 82, "direction": "↑",
         "insight": "Micro-influencers outperform celebrities for authenticity. Build a creator partnership strategy."},
        {"trend": "Community-Led Growth", "momentum": 80, "direction": "↑",
         "insight": "The brands winning in 2026 are communities first, products second."},
    ])

    # Try Gemini for live, richer analysis
    if st.session_state.gemini_ok:
        prompt_tr = (
            "Identify the top 4 industry trends for " + industry + " brands in 2026. "
            "For each trend give: trend name, momentum score 0-100, direction as up/down/flat, "
            "and a 1-sentence brand insight for a " + personality + " brand called " + company + ". "
            "Return JSON array only. Each object must have keys: trend, momentum, direction, insight."
        )
        result = gemini_call(prompt_tr)
        if result:
            import json as _j, re as _r
            try:
                data = _j.loads(_r.sub(r"```json|```", "", result).strip())
                if isinstance(data, list) and len(data) >= 3:
                    return {"trends": data[:4], "source": "gemini", "industry": industry}
            except Exception:
                pass

    return {"trends": fallback_trends, "source": "curated", "industry": industry}


# ── Brand Launch Checklist ────────────────────────────────────────────────────
def generate_launch_checklist(bi: dict) -> list:
    """
    Generate a personalised 30-step go-to-market brand launch checklist.
    Tailored to company name, industry, platform, audience, and personality.
    """
    co   = bi.get("company",    "Your Brand")
    ind  = bi.get("industry",   "your industry")
    pers = bi.get("personality","Professional")
    aud  = bi.get("audience",   "your target customers")
    plat = bi.get("platform",   "Instagram")
    tone = bi.get("tone",       "professional")

    # Try Gemini first for fully personalised checklist
    if st.session_state.gemini_ok:
        prompt_cl = (
            "Create a personalised 30-step brand launch checklist for " + co + ", "
            "a " + pers.lower() + " brand in the " + ind + " industry targeting " + (aud or "modern consumers") + ". "
            "Primary launch platform: " + (plat or "Instagram") + ". "
            "Group steps into 5 phases: Foundation, Visual Identity, Digital Presence, Launch Week, Post-Launch. "
            "Each step must be specific to this brand. "
            "Return a JSON array only. Each object must have keys: phase, step (number), task, priority (high/medium/low), done (false)."
        )
        result = gemini_call(prompt_cl)
        if result:
            import json as _j, re as _r
            try:
                data = _j.loads(_r.sub(r"```json|```", "", result).strip())
                if isinstance(data, list) and len(data) >= 15:
                    return data
            except Exception:
                pass

    # Rich offline fallback — personalised with f-strings
    return [
        # ── Phase 1: Foundation ──
        {"phase": "Foundation",      "step": 1,  "task": f"Register {co} as a business entity and secure trademark for brand name", "priority": "high",   "done": False},
        {"phase": "Foundation",      "step": 2,  "task": f"Purchase domain: {co.lower().replace(' ','-')}.com and relevant variants (.co, .io)", "priority": "high",   "done": False},
        {"phase": "Foundation",      "step": 3,  "task": f"Define {co}'s mission statement, vision, and core values in writing", "priority": "high",   "done": False},
        {"phase": "Foundation",      "step": 4,  "task": f"Map your target audience: create 2 detailed personas for {aud or 'your ideal customers'}", "priority": "high",   "done": False},
        {"phase": "Foundation",      "step": 5,  "task": f"Conduct competitive analysis: identify top 5 competitors in {ind}", "priority": "high",   "done": False},
        {"phase": "Foundation",      "step": 6,  "task": f"Define your unique value proposition — what makes {co} different in {ind.lower()}", "priority": "high",   "done": False},
        # ── Phase 2: Visual Identity ──
        {"phase": "Visual Identity", "step": 7,  "task": f"Finalise {co} logo (primary + secondary variants) from brand kit", "priority": "high",   "done": False},
        {"phase": "Visual Identity", "step": 8,  "task": f"Lock in brand colour palette (primary: from your {pers.lower()} palette) and document hex codes", "priority": "high",   "done": False},
        {"phase": "Visual Identity", "step": 9,  "task": "Set typography hierarchy: heading font, body font, accent font — document sizing rules", "priority": "high",   "done": False},
        {"phase": "Visual Identity", "step": 10, "task": f"Create brand style guide PDF documenting {co}'s visual rules", "priority": "medium", "done": False},
        {"phase": "Visual Identity", "step": 11, "task": f"Design branded business cards, letterhead, and email signature for {co}", "priority": "medium", "done": False},
        {"phase": "Visual Identity", "step": 12, "task": f"Create {plat or 'social media'} profile picture, cover photo, and story highlight icons", "priority": "high",   "done": False},
        # ── Phase 3: Digital Presence ──
        {"phase": "Digital Presence","step": 13, "task": f"Launch {co} website with brand colours, typography, and logo — minimum 3 pages", "priority": "high",   "done": False},
        {"phase": "Digital Presence","step": 14, "task": f"Set up Google Analytics 4 and Search Console for {co}.com", "priority": "medium", "done": False},
        {"phase": "Digital Presence","step": 15, "task": f"Claim and set up {plat or 'social media'} business profile for {co}", "priority": "high",   "done": False},
        {"phase": "Digital Presence","step": 16, "task": f"Write 10 SEO-optimised blog posts or landing pages targeting {ind.lower()} keywords", "priority": "medium", "done": False},
        {"phase": "Digital Presence","step": 17, "task": f"Set up email marketing platform and create branded {co} email templates", "priority": "medium", "done": False},
        {"phase": "Digital Presence","step": 18, "task": f"Create 30-day content calendar for {plat or 'social media'} launch", "priority": "high",   "done": False},
        # ── Phase 4: Launch Week ──
        {"phase": "Launch Week",     "step": 19, "task": f"Send launch announcement email to founding subscribers of {co}", "priority": "high",   "done": False},
        {"phase": "Launch Week",     "step": 20, "task": f"Post launch content using your AI-generated tagline across all {plat or 'social'} channels", "priority": "high",   "done": False},
        {"phase": "Launch Week",     "step": 21, "task": f"Reach out to 10 micro-influencers in {ind.lower()} for launch-week partnerships", "priority": "medium", "done": False},
        {"phase": "Launch Week",     "step": 22, "task": f"Run paid launch campaign on {plat or 'Instagram'} with your campaign kit creative assets", "priority": "high",   "done": False},
        {"phase": "Launch Week",     "step": 23, "task": f"Issue a press release announcing {co}'s launch to {ind.lower()} publications", "priority": "medium", "done": False},
        {"phase": "Launch Week",     "step": 24, "task": f"Host a live Q&A or launch event (virtual or in-person) for {co}", "priority": "low",    "done": False},
        # ── Phase 5: Post-Launch ──
        {"phase": "Post-Launch",     "step": 25, "task": f"Monitor brand mentions and sentiment for {co} across social and news", "priority": "high",   "done": False},
        {"phase": "Post-Launch",     "step": 26, "task": f"Run weekly KPI review: CTR, engagement, follower growth, website traffic for {co}", "priority": "high",   "done": False},
        {"phase": "Post-Launch",     "step": 27, "task": f"Collect first 50 customer reviews and testimonials for {co}", "priority": "high",   "done": False},
        {"phase": "Post-Launch",     "step": 28, "task": f"A/B test 2 tagline variants from your brand kit to see which resonates more", "priority": "medium", "done": False},
        {"phase": "Post-Launch",     "step": 29, "task": f"Refine {co} brand messaging based on first 30 days of audience feedback", "priority": "medium", "done": False},
        {"phase": "Post-Launch",     "step": 30, "task": f"Plan Month 2 campaign using KPI predictions from your BrandSphere Analytics dashboard", "priority": "medium", "done": False},
    ]


# ── Competitor Gap Finder ─────────────────────────────────────────────────────
def find_competitor_gaps(company: str, industry: str, personality: str,
                          competitor_desc: str) -> dict:
    """
    Analyse a competitor description and identify strategic gaps
    that the user's brand can own.
    """
    FALLBACK_GAPS = {
        "Technology / Software": [
            {"gap": "Human-Centred Design", "opportunity": "Most tech brands lead with features. Lead with feelings — position around how the product makes users feel, not what it does.",         "strength": 92},
            {"gap": "Transparent Pricing",  "opportunity": "Complexity and hidden fees are industry norms. A radically transparent pricing model becomes a trust differentiator.",                 "strength": 87},
            {"gap": "Community & Education","opportunity": "Competitors ship products but neglect community. A brand-owned learning hub or community creates defensible loyalty.",                 "strength": 84},
            {"gap": "Ethical AI Narrative", "opportunity": "Most AI brands avoid the ethics conversation. Owning it proactively builds institutional trust with enterprise buyers.",               "strength": 81},
        ],
        "Fashion / Apparel": [
            {"gap": "Radical Transparency",  "opportunity": "Supply chain opacity is the norm. Showing your factories, workers, and costs builds deep brand loyalty with conscious consumers.", "strength": 90},
            {"gap": "Size-Inclusive Fit Tech","opportunity": "Most brands still use standard sizing. AI-powered fit recommendations reduce returns and increase brand affinity.",                  "strength": 85},
            {"gap": "Repair & Longevity",    "opportunity": "Competitors focus on new purchases. A free repair programme becomes a viral loyalty loop and sustainability signal.",               "strength": 83},
            {"gap": "Cultural Co-creation",  "opportunity": "Most brands market TO consumers. Involving your community in design decisions creates advocacy that money can't buy.",              "strength": 80},
        ],
        "Food & Beverage": [
            {"gap": "Ingredient Storytelling","opportunity": "Competitors list ingredients. Bring suppliers to life — named farms, origin stories, and farmer faces build premium perception.",  "strength": 91},
            {"gap": "Personalised Nutrition", "opportunity": "One-size-fits-all nutrition is being disrupted. A quiz-to-product recommendation engine sets you apart immediately.",             "strength": 88},
            {"gap": "Zero-Waste Packaging",   "opportunity": "Most brands greenwash. Fully compostable or refillable packaging is still rare and highly shareable on social.",                 "strength": 85},
            {"gap": "Ritual & Occasion",      "opportunity": "Competitors sell products. Build consumption rituals — morning routines, evening wind-downs — that make your brand essential.",  "strength": 82},
        ],
        "Healthcare": [
            {"gap": "Preventive Positioning", "opportunity": "Most healthcare brands are reactive. Own the 'stay well' conversation before symptoms emerge — your audience is healthier for it.", "strength": 93},
            {"gap": "Plain-Language Comms",   "opportunity": "Medical jargon alienates patients. Radical clarity in brand language is a massive trust builder in a fear-driven category.",     "strength": 89},
            {"gap": "Mental + Physical Unity","opportunity": "Competitors silo mental and physical health. An integrated wellbeing brand narrative resonates with whole-person health seekers.", "strength": 86},
            {"gap": "Outcome Guarantees",     "opportunity": "Healthcare brands make vague claims. Specific, measurable outcome commitments backed by data build unmatched credibility.",       "strength": 83},
        ],
        "Finance": [
            {"gap": "Financial Empowerment",  "opportunity": "Banks talk about products. Build a brand around financial confidence — education-first marketing attracts and retains Gen Z.",    "strength": 92},
            {"gap": "Real-Time Transparency", "opportunity": "Competitors hide fees in fine print. Live fee tracking and zero-surprise billing become viral brand moments.",                    "strength": 88},
            {"gap": "Life Goals Alignment",   "opportunity": "Finance brands talk money. Lead with life outcomes — first home, sabbatical, starting a business — and map products to dreams.", "strength": 85},
            {"gap": "Community Wealth",       "opportunity": "Most fintech is individual-focused. A community savings or investment product creates network effects and shared loyalty.",        "strength": 80},
        ],
    }

    gaps = FALLBACK_GAPS.get(industry, [
        {"gap": "Authentic Storytelling",  "opportunity": "Competitors communicate features. Lead with authentic founder and customer stories that create emotional connection.",        "strength": 89},
        {"gap": "Community-First Brand",   "opportunity": "Most brands broadcast. Build a brand that listens, co-creates, and amplifies its community voice instead.",                 "strength": 85},
        {"gap": "Values Clarity",          "opportunity": "Industry brands are vague on values. A clear, specific values statement that drives every decision builds trust rapidly.", "strength": 82},
        {"gap": "Radical Accessibility",   "opportunity": "Competitors focus on premium. Democratising access to quality in your category is both ethical and commercially powerful.", "strength": 78},
    ])

    if st.session_state.gemini_ok and competitor_desc.strip():
        result = gemini_call(
            "Competitor description: " + competitor_desc + "\n"
            "My brand: " + company + " in " + industry + " (" + personality + " personality).\n\n"
            "Identify 4 strategic gaps this competitor has that " + company + " can own. "
            "For each gap: gap name, a specific opportunity sentence for " + company + ", and a strength score 0-100. "
            "Return JSON array only. Keys: gap, opportunity, strength.",
        )
        if result:
            import json as _j, re as _r
            try:
                data = _j.loads(_r.sub(r"```json|```", "", result).strip())
                if isinstance(data, list) and len(data) >= 3:
                    return {"gaps": data[:4], "source": "gemini"}
            except Exception:
                pass

    return {"gaps": gaps, "source": "curated"}


# ── Audience Persona Builder ──────────────────────────────────────────────────
def build_audience_personas(company: str, industry: str, personality: str,
                             audience: str, tone: str) -> list:
    """
    Generate 3 detailed buyer personas tailored to the brand.
    Each persona includes demographics, psychographics, pain points,
    buying triggers, and preferred channels.
    """
    PERSONA_TEMPLATES = {
        "Technology / Software": [
            {"name": "The Efficiency-Obsessed Founder",   "age": "32-42", "role": "Startup CEO / Co-founder",
             "income": "$85K-$200K", "location": "Urban tech hub",
             "pain_points": ["Tool overload and context-switching fatigue", "Can't scale processes fast enough", "Afraid of choosing the wrong platform long-term"],
             "triggers":    ["Peer recommendation from trusted network", "ROI calculator showing time saved", "Free trial with immediate 'aha' moment"],
             "channels":    ["LinkedIn", "Product Hunt", "Tech podcasts", "Twitter/X"],
             "quote":       '"I need it to just work — and I need it today."'},
            {"name": "The Cautious IT Decision-Maker",    "age": "38-52", "role": "CTO / IT Director",
             "income": "$120K-$250K", "location": "Enterprise environment",
             "pain_points": ["Security and compliance concerns", "Integration with legacy systems", "Justifying budget to board"],
             "triggers":    ["Case studies from similar-size companies", "Security certifications visible upfront", "Dedicated enterprise onboarding"],
             "channels":    ["Gartner reports", "LinkedIn", "Industry conferences", "Direct sales"],
             "quote":       '"Show me it scales and I will listen."'},
            {"name": "The Ambitious Solo Builder",        "age": "24-34", "role": "Freelancer / Indie developer",
             "income": "$40K-$80K", "location": "Remote / anywhere",
             "pain_points": ["Budget constraints vs. quality tools", "No IT support — must be self-serve", "Fear of vendor lock-in"],
             "triggers":    ["Generous free tier", "Active community and tutorials", "Built by people who understand the problem"],
             "channels":    ["YouTube tutorials", "Reddit", "Discord communities", "GitHub"],
             "quote":       '"If it has a free plan and works, I am in."'},
        ],
        "Fashion / Apparel": [
            {"name": "The Conscious Style Seeker",        "age": "26-38", "role": "Marketing / Creative professional",
             "income": "$55K-$95K", "location": "Urban / semi-urban",
             "pain_points": ["Greenwashing makes trust hard", "Fast fashion guilt", "Difficulty finding quality at fair price"],
             "triggers":    ["Visible supply chain transparency", "Social proof from style-aligned influencers", "Limited edition drops creating urgency"],
             "channels":    ["Instagram", "TikTok", "Pinterest", "Substack newsletters"],
             "quote":       '"I want to look great and feel good about where it came from."'},
            {"name": "The Status-Driven Achiever",        "age": "30-45", "role": "Finance / Law / Consulting",
             "income": "$100K-$300K", "location": "Major city",
             "pain_points": ["Inconsistent quality at luxury price points", "Brand saturation — everyone wears the same logos", "Time-poor — no patience for poor experience"],
             "triggers":    ["Exclusivity signals", "Personalised styling service", "Investment-grade quality narrative"],
             "channels":    ["Editorial media", "LinkedIn", "Email", "Private shopping events"],
             "quote":       '"I buy fewer things, but they have to be exceptional."'},
            {"name": "The Trend-Forward Gen Z Explorer",  "age": "18-27", "role": "Student / Entry-level creative",
             "income": "$15K-$40K", "location": "Diverse, digital-first",
             "pain_points": ["Brand inauthenticity is instantly spotted", "Wants individuality but budgets are tight", "Overwhelmed by choice online"],
             "triggers":    ["Viral UGC content", "Brand activism alignment", "Affordable entry product with upsell path"],
             "channels":    ["TikTok", "Instagram Reels", "YouTube", "Depop", "Discord"],
             "quote":       '"If it is not on TikTok, it is not real."'},
        ],
    }

    fallback = PERSONA_TEMPLATES.get(industry, [
        {"name": "The Pragmatic Professional",    "age": "30-45", "role": "Mid-senior manager",
         "income": "$60K-$120K", "location": "Urban or suburban",
         "pain_points": ["Too many options, hard to choose", "Budget justification pressure", "Fear of making the wrong decision"],
         "triggers":    ["Social proof and reviews", "Clear ROI demonstration", "Risk-free trial or guarantee"],
         "channels":    ["LinkedIn", "Google Search", "Industry publications", "Email"],
         "quote":       '"Prove the value and I will commit."'},
        {"name": "The Ambitious Early Adopter",   "age": "22-35", "role": "Entrepreneur / Creative",
         "income": "$30K-$70K", "location": "Remote or urban",
         "pain_points": ["Undiscovered gems get overlooked", "Wants innovation, not iteration", "Community and belonging matter as much as product"],
         "triggers":    ["Founder story and mission alignment", "Early access or beta programmes", "Strong community"],
         "channels":    ["Twitter/X", "TikTok", "Product Hunt", "Newsletters"],
         "quote":       '"I want to find it before everyone else does."'},
        {"name": "The Value-Conscious Buyer",     "age": "35-55", "role": "Family decision-maker / SMB owner",
         "income": "$45K-$90K", "location": "Suburban / regional",
         "pain_points": ["Doesn't want to overpay", "Trust is hard to build", "Needs reliability over novelty"],
         "triggers":    ["Word-of-mouth from trusted peers", "Long-term value over short-term cost", "Excellent customer service"],
         "channels":    ["Facebook", "Google Reviews", "Email newsletters", "Local community groups"],
         "quote":       '"Give me reliability and treat me fairly."'},
    ])

    if st.session_state.gemini_ok:
        aud_str = audience or "modern consumers"
        result = gemini_call(
            "Create 3 detailed buyer personas for " + company + ", a " + personality.lower() +
            " brand in " + industry + " targeting " + aud_str + " with a " + tone + " tone.\n"
            "Each persona must have: name (creative persona label), age range, role/occupation, "
            "income range, location type, 3 pain points (list), 3 buying triggers (list), "
            "preferred channels (list), and a one-line quote in their voice.\n"
            "Return JSON array only. Keys: name, age, role, income, location, pain_points, triggers, channels, quote.",
        )
        if result:
            import json as _j, re as _r
            try:
                data = _j.loads(_r.sub(r"```json|```", "", result).strip())
                if isinstance(data, list) and len(data) >= 2:
                    return data[:3]
            except Exception:
                pass

    return fallback[:3]

# ══════════════════════════════════════════════════════════════════════════════
#  NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nav-bar">
  <div>
    <div class="nav-logo">Brand<span>Sphere</span> AI</div>
    <div class="nav-tag">Automated Branding Intelligence Platform</div>
  </div>
  <div class="nav-tag">Scenario 1 &nbsp;|&nbsp; CRS AI Capstone 2025–26</div>
</div>
""", unsafe_allow_html=True)

# ── API Key config ────────────────────────────────────────────────────────
with st.expander("⚙️  API Configuration", expanded=not st.session_state.gemini_ok):
    c1, c2 = st.columns([4, 1])
    with c1:
        api_inp = st.text_input("Gemini API Key", type="password",
                                placeholder="AIza...", label_visibility="collapsed")
    with c2:
        if st.button("Connect"):
            if api_inp:
                if configure_gemini(api_inp):
                    st.success("✓ Gemini connected")
                else:
                    st.error("Invalid key")
    if not st.session_state.gemini_ok:
        st.info("💡 **Demo mode** — all features work with AI-simulated outputs. Connect Gemini for live generation.")
    else:
        st.success(f"✓ Gemini 2.0 Flash connected — Session {st.session_state.session_id}")

# ── HERO ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI-Powered Branding Intelligence</div>
  <div class="hero-title">Your brand identity,<br><em>engineered by AI.</em></div>
  <div class="hero-sub">
    Generate logos, taglines, color palettes, campaigns, and complete brand kits in minutes.
    Powered by Computer Vision, Generative AI, NLP, and Predictive Analytics.
  </div>
  <div class="badge-row">
    <span class="badge">Logo Studio</span>
    <span class="badge">KMeans Palette</span>
    <span class="badge">NLTK NLP</span>
    <span class="badge">Random Forest KPIs</span>
    <span class="badge">Gemini API</span>
    <span class="badge">Multilingual</span>
    <span class="badge">Streamlit Cloud</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "🏠 Home",
    "🎯 Brand Inputs",
    "🎨 Logo Studio",
    "🖋 Fonts & Palette",
    "✍️ Slogans & Content",
    "📣 Campaign Analytics",
    "🌍 Multilingual Studio",
    "🎬 Animation Preview",

    "📡 Trend Radar",
    "✅ Launch Checklist",
    "🔍 Competitor Gaps",
    "👥 Audience Personas",
    "⭐ Feedback",
    "📦 Download Kit",
])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="sec-label">Overview</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Welcome to <em>BrandSphere AI</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    modules = [
        ("🎨", "AI Logo & Design Studio", "5 SVG logo concepts generated from your brand personality and color palette."),
        ("✍️", "Creative Content & GenAI Hub", "NLTK-powered tagline analysis + Gemini-enhanced slogan generation."),
        ("📣", "Smart Campaign Studio", "Random Forest model trained on 200K real marketing records predicts CTR, ROI & Engagement."),
        ("🌍", "Multilingual Engine", "Gemini-powered translation into 5 languages with tone preservation."),
        ("⭐", "Feedback Intelligence", "Star ratings saved to CSV; Plotly dashboards visualize patterns."),
        ("📦", "Export Engine", "Complete brand kit: logos, palette, fonts, taglines, campaigns, animation — all in one ZIP."),
    ]
    for i, (icon, title, desc) in enumerate(modules):
        col = [c1, c2, c3][i % 3]
        with col:
            st.markdown(f"""
            <div class="card">
              <div style="font-size:1.8rem;margin-bottom:8px">{icon}</div>
              <div class="card-title">{title}</div>
              <div class="card-sub">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-label">10-Week Roadmap</p>', unsafe_allow_html=True)
    weeks = [
        ("Week 1", "EDA & Data Understanding", "✅ Completed"),
        ("Week 2", "Logo Classification & Extraction", "✅ SVG Engine"),
        ("Week 3", "Font Recommendation Engine", "✅ Completed"),
        ("Week 4", "Tagline & Slogan Generation", "✅ NLTK + Gemini"),
        ("Week 5", "Color Palette Engine", "✅ KMeans"),
        ("Week 6", "Animated Visuals Studio", "✅ Pillow GIF"),
        ("Week 7", "Smart Campaign Studio", "✅ Random Forest"),
        ("Week 8", "Multilingual Generator", "✅ Gemini / Fallback"),
        ("Week 9", "Feedback Intelligence", "✅ CSV + Plotly"),
        ("Week 10","Integration & Deployment", "✅ Streamlit Cloud"),
    ]
    for wk, task, status in weeks:
        st.markdown(f"""
        <div class="check-item">
          <span style="color:var(--teal);font-size:0.95rem">✓</span>
          <div>
            <span style="font-family:var(--font-mono);font-size:0.62rem;color:var(--accent);letter-spacing:0.1em">{wk}</span>
            <span style="font-size:0.88rem;color:var(--text);margin-left:12px">{task}</span>
            <span style="margin-left:10px" class="pill pill-g">{status}</span>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — BRAND INPUTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="sec-label">Step 01 — Foundation</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Brand <em>Input Form</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        company    = st.text_input("Company Name *", placeholder="e.g. NovaTech Solutions")
        industry   = st.selectbox("Industry *", INDUSTRIES)
        personality= st.selectbox("Brand Personality *", PERSONALITIES)
        audience   = st.text_input("Target Audience", placeholder="e.g. Millennials aged 25–40")
    with col2:
        tone       = st.selectbox("Communication Tone", TONES)
        tag_hint   = st.text_input("Tagline Hint (optional)", placeholder="e.g. Focus on innovation and speed")
        description= st.text_area("Product / Service Description",
                                   placeholder="What does your business do? What makes it unique?", height=108)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.button("🚀  Generate Full Brand Kit", width='content'):
        if not company:
            st.warning("Please enter a company name.")
        else:
            bi = {"company": company, "industry": industry, "personality": personality,
                  "audience": audience, "tone": tone, "tag_hint": tag_hint, "description": description}
            st.session_state.brand_inputs = bi

            with st.spinner("Building brand identity…"):
                st.session_state.palette  = generate_palette(industry, personality)
                st.session_state.logos    = generate_all_logos(company, st.session_state.palette)
                st.session_state.fonts    = recommend_fonts(industry, personality)
                slogans, retrieved = generate_slogans(company, industry, tone, audience, tag_hint)
                st.session_state.slogans   = slogans
                st.session_state.retrieved = retrieved
                st.session_state.aesthetics = score_brand(personality, industry, tone,
                                                           slogans[0]["text"] if slogans else "",
                                                           st.session_state.palette)

            st.success(f"✓ Brand kit generated for **{company}**. Navigate the tabs to explore your assets.")

    if st.session_state.brand_inputs:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Current Brand Profile</p>', unsafe_allow_html=True)
        bi = st.session_state.brand_inputs
        cols = st.columns(4)
        for col, (lbl, val) in zip(cols, [
            ("Company", bi.get("company","")), ("Industry", bi.get("industry","")),
            ("Personality", bi.get("personality","")), ("Tone", bi.get("tone",""))
        ]):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <span class="metric-lbl">{lbl}</span>
                  <span style="font-family:var(--font-head);font-size:1.1rem;color:var(--text);display:block;margin-top:5px">{val}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-label">✨ Brand Name Generator</p>', unsafe_allow_html=True)
    st.markdown('<h3 style="font-family:var(--font-head);font-weight:300;color:var(--text);margin-bottom:12px">No name yet? <em style="color:var(--accent)">Let AI suggest one.</em></h3>', unsafe_allow_html=True)
    ng1, ng2, ng3 = st.columns([1,1,1], gap="large")
    with ng1:
        ng_industry = st.selectbox("Industry", INDUSTRIES, key="ng_ind")
    with ng2:
        ng_pers = st.selectbox("Personality", PERSONALITIES, key="ng_pers")
    with ng3:
        ng_kw = st.text_input("Keywords (optional)", placeholder="e.g. speed, clarity, trust", key="ng_kw")
    if st.button("🎲  Generate Brand Names"):
        with st.spinner("Generating names…"):
            names = generate_brand_names(ng_industry, ng_pers, ng_kw)
            if names:
                name_cols = st.columns(min(4, len(names)))
                for i, n in enumerate(names[:8]):
                    with name_cols[i % 4]:
                        st.markdown(f"""
                        <div class="card" style="text-align:center;padding:16px">
                          <div style="font-family:var(--font-head);font-size:1.3rem;color:var(--accent);margin-bottom:5px">{n.get('name','')}</div>
                          <div style="font-size:0.76rem;color:var(--muted);line-height:1.55">{n.get('rationale','')}</div>
                          <div style="font-family:var(--font-mono);font-size:0.55rem;color:var(--text2) ;margin-top:8px;opacity:0.5">{n.get('domain','')}</div>
                        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — LOGO STUDIO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="sec-label">Module 01 — Visual Identity</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Logo <em>Studio</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.logos:
        st.info("👈 Complete Brand Inputs first to generate logos.")
    else:
        bi = st.session_state.brand_inputs
        st.markdown(f'<p class="sec-label">5 Concepts for {bi.get("company","")}</p>', unsafe_allow_html=True)
        st.caption("⚠️ ")

        logo_cols = st.columns(5)
        for i, logo in enumerate(st.session_state.logos):
            with logo_cols[i]:
                selected_cls = "selected" if st.session_state.selected_logo == i else ""
                st.markdown(f"""
                <div class="logo-svg-wrap {selected_cls}" id="logo_{i}">
                  {logo["svg"]}
                  <div style="font-family:var(--font-mono);font-size:0.55rem;color:var(--accent);letter-spacing:0.08em;text-align:center">{logo["style"]}</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Select", key=f"sel_logo_{i}"):
                    st.session_state.selected_logo = i
                    st.rerun()

        sel = st.session_state.logos[st.session_state.selected_logo]
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f'<p class="sec-label">Selected: {sel["style"]}</p>', unsafe_allow_html=True)
            st.markdown(sel["svg"], unsafe_allow_html=True)
            st.download_button("⬇ Download SVG", data=sel["svg"].encode(),
                               file_name=f"{bi.get('company','brand')}_logo_{sel['index']}.svg",
                               mime="image/svg+xml")
            png = svg_to_png_bytes(sel["svg"], 300)
            if png:
                st.download_button("⬇ Download PNG", data=png,
                                   file_name=f"{bi.get('company','brand')}_logo_{sel['index']}.png",
                                   mime="image/png")
        with c2:
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">Design Rationale</p>
              <p style="font-size:0.9rem;line-height:1.7;color:var(--text)">{sel["description"]}</p>
              <br/>
              <p class="sec-label">All Concepts</p>
              {"".join([f'<div style="font-size:0.83rem;color:var(--muted);padding:4px 0;border-bottom:1px solid var(--border)"><span style="color:var(--accent)">#{l["index"]+1}</span> {l["style"]} — {l["description"][:60]}…</div>' for l in st.session_state.logos])}
            </div>""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — FONTS & PALETTE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="sec-label">Module 02 — Visual System</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Fonts & <em>Colour Palette</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.palette:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs

        # Palette
        st.markdown('<p class="sec-label">KMeans-Extracted Color Palette (Week 5)</p>', unsafe_allow_html=True)
        st.caption("KMeans(k=5) run on noise-augmented seed colors from industry color psychology mapping.")
        swatch_html = '<div class="swatch-row">'
        for name, v in st.session_state.palette.items():
            swatch_html += f'<div class="swatch" style="background:{v["hex"]}">{v["hex"]}</div>'
        swatch_html += "</div>"
        st.markdown(swatch_html, unsafe_allow_html=True)

        pc1, pc2 = st.columns(2, gap="large")
        with pc1:
            for name, v in st.session_state.palette.items():
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin:7px 0">
                  <div style="width:32px;height:32px;background:{v['hex']};border-radius:5px;flex-shrink:0"></div>
                  <div>
                    <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--accent);letter-spacing:0.1em">{name}</span>
                    <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--muted);margin-left:8px">{v['hex']}</span>
                    <div style="font-size:0.78rem;color:var(--muted)">{v['psychology']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with pc2:
            harmony = score_palette_harmony(st.session_state.palette)
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:14px">
              <span class="metric-val">{harmony}/100</span>
              <span class="metric-lbl">Palette Harmony Score</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">Personality</p>
              <p style="font-family:var(--font-head);font-size:1.05rem;font-style:italic;color:var(--text)">
                {bi.get("personality","")} palette for {bi.get("industry","")}
              </p>
              <p style="font-size:0.82rem;color:var(--muted);margin-top:8px;line-height:1.6">
                Follow the 60-30-10 rule: 60% Primary · 30% Secondary · 10% Accent.
              </p>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Dark / Light Mode Switcher
        st.markdown('<p class="sec-label">🌗 Dark / Light Mode Switcher</p>', unsafe_allow_html=True)
        dm1, dm2 = st.columns([1, 2], gap="large")
        with dm1:
            mode_choice = st.radio("Palette Mode", ["Original", "Dark Mode", "Light Mode"], horizontal=True, key="palette_mode")
            if st.button("↺  Apply Mode"):
                if mode_choice == "Original":
                    from src.palette_engine import generate_palette as regen_pal
                    bi3 = st.session_state.brand_inputs
                    st.session_state.palette = regen_pal(bi3.get("industry",""), bi3.get("personality",""))
                else:
                    switched = switch_palette_mode(st.session_state.palette, mode_choice)
                    st.session_state.palette = switched
                st.rerun()
        with dm2:
            if st.session_state.palette:
                colors = list(st.session_state.palette.values())
                sw_html = '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">'
                for v in colors:
                    sw_html += f'<div style="text-align:center"><div style="width:50px;height:50px;background:{v["hex"]};border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.3)"></div><div style="font-family:var(--font-mono);font-size:0.52rem;color:var(--muted);margin-top:4px">{v["hex"]}</div></div>'
                sw_html += '</div>'
                st.markdown(f'<p style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);letter-spacing:0.1em">CURRENT MODE: {mode_choice.upper()}</p>{sw_html}', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # WCAG Accessibility
        st.markdown('<p class="sec-label">♿ WCAG Accessibility Check</p>', unsafe_allow_html=True)
        wcag_results = check_wcag(st.session_state.palette)
        if wcag_results:
            wc1, wc2 = st.columns(2, gap="large")
            for i, r in enumerate(wcag_results):
                with [wc1, wc2][i % 2]:
                    aa_color  = "#3ECFB2" if "Pass" in r["AA"]  else "#E05A5A"
                    aaa_color = "#3ECFB2" if "Pass" in r["AAA"] else "#E05A5A"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;background:var(--surface2);border-radius:8px;padding:12px 14px;margin-bottom:8px;border:1px solid var(--border)">
                      <div style="display:flex;gap:4px;flex-shrink:0">
                        <div style="width:24px;height:24px;background:{r['hex1']};border-radius:4px"></div>
                        <div style="width:24px;height:24px;background:{r['hex2']};border-radius:4px"></div>
                      </div>
                      <div style="flex:1;min-width:0">
                        <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--muted)">{r['pair']}</div>
                        <div style="font-family:var(--font-mono);font-size:0.68rem;color:var(--accent)">Ratio: {r['ratio']}:1</div>
                      </div>
                      <div style="text-align:right;font-family:var(--font-mono);font-size:0.6rem">
                        <div style="color:{aa_color}">AA {r['AA'].split()[0]}</div>
                        <div style="color:{aaa_color}">AAA {r['AAA'].split()[0]}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Fonts
        st.markdown('<p class="sec-label">Font Recommendations (Week 3)</p>', unsafe_allow_html=True)
        st.caption("Rule-based engine mapping industry × personality → curated font pairings. No font image dataset required.")
        fcols = st.columns(3)
        for i, font in enumerate(st.session_state.fonts):
            with fcols[i]:
                st.markdown(f"""
                <div class="card">
                  <div style="font-family:var(--font-mono);font-size:0.56rem;color:var(--accent);letter-spacing:0.12em;margin-bottom:6px">{font['rank']}</div>
                  <div class="card-title">{font['heading']}</div>
                  <div style="font-size:0.8rem;color:var(--muted);margin-bottom:8px">Body: {font['body']}<br>Alt: {font['alternate']}</div>
                  <div style="font-size:0.78rem;color:var(--text);line-height:1.55">{font['rationale']}</div>
                  <br>
                  <span class="pill pill-a">{font['classification']}</span>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — SLOGANS & CONTENT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<p class="sec-label">Module 03 — Generative AI</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Slogans & <em>Content Hub</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs

        sc1, sc2 = st.columns([1, 1], gap="large")

        with sc1:
            st.markdown('<p class="sec-label">AI-Generated Taglines</p>', unsafe_allow_html=True)
            if st.button("✨  Regenerate Taglines"):
                with st.spinner("Generating…"):
                    slogans, retrieved = generate_slogans(
                        bi["company"], bi["industry"], bi["tone"],
                        bi.get("audience",""), bi.get("tag_hint",""))
                    st.session_state.slogans   = slogans
                    st.session_state.retrieved = retrieved

            if st.session_state.slogans:
                for s in st.session_state.slogans:
                    src_pill = "pill-g" if s["source"] == "gemini" else "pill-a"
                    st.markdown(f"""
                    <div class="tagline-card">"{s['text']}"
                      <div style="margin-top:5px">
                        <span class="pill {src_pill}">{s['source']}</span>
                        <span class="pill pill-a" style="margin-left:4px">{s['tone']}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

            if st.session_state.retrieved:
                st.markdown('<p class="sec-label" style="margin-top:18px">TF-IDF Retrieved Inspiration</p>', unsafe_allow_html=True)
                for r in st.session_state.retrieved[:3]:
                    st.markdown(f'<div style="font-style:italic;color:var(--muted);font-size:0.84rem;padding:4px 0">"{r}"</div>', unsafe_allow_html=True)

            # NLTK Analysis
            if st.session_state.slogans:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                with st.expander("🔬 NLTK Text Analysis (Week 4 — NLP Preprocessing)"):
                    top = st.session_state.slogans[0]["text"]
                    analysis = st.session_state.slogans[0].get("analysis") or nltk_analyze(top)
                    st.markdown(f"""
                    <div style="background:var(--surface2);border-radius:8px;padding:14px 16px;border:1px solid var(--border)">
                      <p class="sec-label">Analysed: "{top[:50]}"</p>
                      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:10px 0">
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['word_count']}</span><span class="metric-lbl">Tokens</span></div>
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['unique_words']}</span><span class="metric-lbl">Unique</span></div>
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['lexical_density']}</span><span class="metric-lbl">Lex Density</span></div>
                      </div>
                      <p style="font-family:var(--font-mono);font-size:0.56rem;color:var(--accent);letter-spacing:0.1em;text-transform:uppercase;margin-top:10px">Clean tokens</p>
                      <div>{"".join([f'<span class="nltk-pill">{t}</span>' for t in analysis["clean_tokens"]])}</div>
                      <p style="font-family:var(--font-mono);font-size:0.56rem;color:var(--muted);letter-spacing:0.1em;text-transform:uppercase;margin-top:10px">Stems (Porter)</p>
                      <div>{"".join([f'<span class="nltk-pill" style="opacity:0.6">{s}</span>' for s in analysis["stems"]])}</div>
                    </div>""", unsafe_allow_html=True)

        with sc2:
            st.markdown('<p class="sec-label">Brand Narrative</p>', unsafe_allow_html=True)
            if st.button("📖  Generate Brand Story"):
                with st.spinner("Writing…"):
                    result = generate_brand_story(bi)
                    if result:
                        st.session_state.brand_story = result
                    else:
                        # Absolute last resort fallback
                        co2 = bi.get("company","Brand")
                        st.session_state.brand_story = (
                            co2 + " exists to redefine what is possible in "
                            + bi.get("industry","your industry").lower() + ". "
                            "Built with intention, designed for impact, and crafted for the people who expect more. "
                            "Every product, every interaction, every detail — made to matter. "
                            "This is " + co2 + ". Welcome to the future of your brand."
                        )

            if st.session_state.brand_story:
                st.markdown(f"""
                <div class="card">
                  <p class="sec-label">Brand Narrative</p>
                  <p style="font-family:var(--font-head);font-size:1rem;font-style:italic;line-height:1.85;color:var(--text)">{st.session_state.brand_story}</p>
                </div>""", unsafe_allow_html=True)

            # Aesthetics score
            if st.session_state.aesthetics:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="sec-label">Brand Consistency Score</p>', unsafe_allow_html=True)
                aes = st.session_state.aesthetics
                overall = aes["overall"]
                grade   = aes["grade"]
                pill    = "pill-g" if overall >= 88 else "pill-a" if overall >= 75 else "pill-r"
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:14px">
                  <span class="metric-val">{overall}/100</span>
                  <span class="metric-lbl">Brand Cohesion <span class="pill {pill}">{grade}</span></span>
                </div>""", unsafe_allow_html=True)
                for dim, score in list(aes["dimensions"].items())[:4]:
                    color = "#3ECFB2" if score >= 85 else "#C9A84C" if score >= 72 else "#E05A5A"
                    st.markdown(f"""
                    <div style="margin:8px 0">
                      <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                        <span style="font-family:var(--font-mono);font-size:0.58rem;color:var(--muted);letter-spacing:0.08em">{dim.upper()}</span>
                        <span style="font-family:var(--font-mono);font-size:0.62rem;color:{color}">{score}/100</span>
                      </div>
                      <div class="prog-wrap"><div class="prog-bar" style="width:{score}%;background:{color}"></div></div>
                    </div>""", unsafe_allow_html=True)

# ── A/B Tagline Tester ───────────────────────────────────────────────────────
if st.session_state.get("slogans"):
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.expander("🧪 A/B Tagline Scorer — Compare Your Taglines"):
        st.caption("AI scores each tagline across 5 brand dimensions: Memorability, Clarity, Emotional Impact, Brand Fit, Uniqueness.")
        if st.button("▶  Run A/B Scorer"):
            bi2 = st.session_state.brand_inputs
            with st.spinner("Scoring…"):
                ab_results = ab_test_taglines(
                    st.session_state.slogans,
                    bi2.get("industry",""), bi2.get("audience",""))
            if ab_results:
                dims = ["memorability","clarity","emotional_impact","brand_fit","uniqueness"]
                dim_labels = ["Memory","Clarity","Emotion","Brand Fit","Unique"]
                medals = ["🥇","🥈","🥉","4️⃣"]
                for rank, r in enumerate(ab_results, 1):
                    score_color = "#3ECFB2" if r["overall"] >= 8 else "#C9A84C" if r["overall"] >= 6 else "#E05A5A"
                    dim_html = ""
                    for d, dl in zip(dims, dim_labels):
                        c = "#3ECFB2" if r[d] >= 8 else "#C9A84C" if r[d] >= 6 else "#E05A5A"
                        dim_html += f'<div style="text-align:center"><div style="font-family:var(--font-mono);font-size:0.5rem;color:var(--muted);text-transform:uppercase">{dl}</div><div style="font-size:1rem;color:{c};font-weight:700">{r[d]}</div></div>'
                    st.markdown(f'''
                    <div class="card" style="margin-bottom:10px">
                      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                        <div style="font-family:var(--font-head);font-size:1rem;font-style:italic;color:var(--text)">{medals[min(rank-1,3)]} &ldquo;{r["tagline"]}&rdquo;</div>
                        <div style="font-family:var(--font-mono);font-size:0.95rem;color:{score_color};font-weight:700">{r["overall"]}/10</div>
                      </div>
                      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px">{dim_html}</div>
                    </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — CAMPAIGN ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<p class="sec-label">Module 04 — Campaign Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Smart Campaign <em>Analytics</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs
        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            platform  = st.selectbox("Platform", PLATFORMS)
        with ca2:
            region    = st.selectbox("Region", REGIONS)
        with ca3:
            objective = st.selectbox("Objective", CAMPAIGN_OBJECTIVES)

        if st.button("🚀  Predict KPIs & Generate Campaign"):
            with st.spinner("Running ML model…"):
                pred = get_predictor()
                kpis = pred.predict(platform, region, objective,
                                    bi["personality"],
                                    duration_days=30, budget=5000)
                st.session_state.kpis = kpis
                camp_data = generate_campaign_content(bi, platform, region, objective)
                st.session_state.campaigns[platform] = camp_data

        if st.session_state.kpis:
            kpis = st.session_state.kpis
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            kc1, kc2, kc3, kc4 = st.columns(4)
            for col, (lbl, val, unit) in zip([kc1, kc2, kc3, kc4], [
                ("CTR",        kpis["CTR"],        "%"),
                ("ROI",        kpis["ROI"],        "×"),
                ("Engagement", kpis["Engagement"], "/10"),
                ("Best Time",  kpis["Best_Time"],  ""),
            ]):
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                      <span class="metric-val" style="font-size:1.7rem">{val}{unit}</span>
                      <span class="metric-lbl">{lbl}</span>
                    </div>""", unsafe_allow_html=True)

            st.caption(f"Source: {kpis.get('Source','')}")
            if kpis.get("Tip"):
                st.markdown(f"""
                <div style="background:rgba(201,168,76,0.07);border-left:3px solid var(--accent);padding:14px 16px;border-radius:0 8px 8px 0;font-size:0.86rem;line-height:1.65;color:var(--muted);margin-top:12px">
                  💡 {kpis["Tip"]}
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.plotly_chart(kpi_bar_chart(kpis), width='stretch')

            region_scores = {r: np.random.randint(58, 86) for r in REGIONS[:-1]}
            region_scores[region] = max(region_scores.values()) + 3
            st.plotly_chart(regional_engagement_map(region_scores), width='stretch')

        if st.session_state.campaigns:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<p class="sec-label">Generated Campaign Content</p>', unsafe_allow_html=True)
            for plat, data in st.session_state.campaigns.items():
                with st.expander(f"📱  {plat} Campaign"):
                    st.markdown(f"""
                    <div class="card">
                      <p class="sec-label">Caption</p>
                      <p style="color:var(--text);line-height:1.75;font-size:0.9rem">{data.get("caption","")}</p>
                    </div>""", unsafe_allow_html=True)
                    tags = data.get("hashtags", [])
                    html = " ".join([f'<span class="pill pill-a">{h}</span>' for h in tags])
                    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0">{html}</div>', unsafe_allow_html=True)
                    if data.get("regional_strategy"):
                        st.markdown(f"""
                        <div class="card">
                          <p class="sec-label">Regional Strategy — {region}</p>
                          <p style="color:var(--muted);font-size:0.87rem;line-height:1.7">{data["regional_strategy"]}</p>
                        </div>""", unsafe_allow_html=True)


        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">💰 Campaign ROI Calculator</p>', unsafe_allow_html=True)
        roi_c1, roi_c2, roi_c3 = st.columns(3, gap="large")
        with roi_c1:
            roi_budget   = st.number_input("Budget (USD $)", min_value=100, max_value=500000,
                                            value=5000, step=500, key="roi_budget")
            roi_platform = st.selectbox("Platform", PLATFORMS, key="roi_plat")
        with roi_c2:
            roi_obj      = st.selectbox("Objective", CAMPAIGN_OBJECTIVES, key="roi_obj")
            roi_aud      = st.number_input("Est. Audience Size", min_value=1000,
                                            max_value=10000000, value=100000,
                                            step=10000, key="roi_aud")
        with roi_c3:
            roi_pers     = st.selectbox("Brand Personality", PERSONALITIES, key="roi_pers",
                                         index=PERSONALITIES.index(
                                             (st.session_state.brand_inputs or {}).get("personality","Minimalist")
                                         ) if st.session_state.brand_inputs else 0)
            roi_btn      = st.button("📊  Calculate ROI Projection", key="roi_btn")

        if roi_btn:
            roi_data = calculate_roi(roi_budget, roi_platform, roi_obj, roi_aud, roi_pers)
            roi_color = "#3ECFB2" if roi_data["roi_pct"] > 50 else "#C9A84C" if roi_data["roi_pct"] > 0 else "#E05A5A"

            r1, r2, r3, r4 = st.columns(4)
            for col, (lbl, val, unit) in zip([r1,r2,r3,r4], [
                ("Est. Impressions",  f"{roi_data['impressions']:,}",   ""),
                ("Est. Clicks",       f"{roi_data['clicks']:,}",        ""),
                ("Est. Conversions",  f"{roi_data['conversions']:,}",   ""),
                ("Projected ROI",     f"{roi_data['roi_pct']:+.1f}",    "%"),
            ]):
                with col:
                    color = roi_color if lbl == "Projected ROI" else "var(--accent)"
                    st.markdown(f"""
                    <div class="metric-card">
                      <span class="metric-val" style="font-size:1.6rem;color:{color}">{val}{unit}</span>
                      <span class="metric-lbl">{lbl}</span>
                    </div>""", unsafe_allow_html=True)

            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            rc1, rc2 = st.columns(2, gap="large")
            with rc1:
                st.markdown(f"""
                <div class="card">
                  <p class="sec-label">Cost Breakdown</p>
                  <div style="font-size:0.86rem;color:var(--text);line-height:1.9">
                    💵 Budget: <strong>${roi_data['budget']:,}</strong><br>
                    🖱  Cost per click: <strong>${roi_data['cost_per_click']}</strong><br>
                    🎯 Cost per conversion: <strong>${roi_data['cost_per_conv']}</strong><br>
                    📈 Est. revenue: <strong>${roi_data['revenue_est']:,}</strong>
                  </div>
                </div>""", unsafe_allow_html=True)
            with rc2:
                import plotly.graph_objects as go_roi
                fig_roi = go_roi.Figure(go_roi.Waterfall(
                    name="ROI", orientation="v",
                    x=["Budget", "Revenue", "Net Return"],
                    y=[-roi_data["budget"], roi_data["revenue_est"],
                       roi_data["revenue_est"] - roi_data["budget"]],
                    connector={"line": {"color": "#2A2C31"}},
                    increasing={"marker": {"color": "#3ECFB2"}},
                    decreasing={"marker": {"color": "#E05A5A"}},
                    totals={"marker":   {"color": "#C9A84C"}},
                ))
                fig_roi.update_layout(
                    paper_bgcolor="#141518", plot_bgcolor="#141518",
                    font_color="#F0EDE8", font_family="DM Sans",
                    height=240, margin=dict(t=20,b=20,l=20,r=20),
                    showlegend=False,
                    xaxis=dict(gridcolor="#2A2C31"),
                    yaxis=dict(gridcolor="#2A2C31"),
                )
                st.plotly_chart(fig_roi, width='stretch')
            st.caption(f"ℹ️  {roi_data['note']}")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — MULTILINGUAL STUDIO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<p class="sec-label">Module 05 — Global Reach</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Multilingual <em>Studio</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi    = st.session_state.brand_inputs
        langs = st.multiselect("Target Languages", LANGUAGES_SUPPORTED,
                               default=["Hindi", "Spanish", "French", "German", "Gujarati"])

        slogan_to_translate = (st.session_state.slogans[0]["text"]
                                if st.session_state.slogans
                                else f"{bi.get('company','Brand')} — Excellence by Design")

        st.markdown(f"""
        <div style="background:var(--surface2);border-radius:8px;padding:12px 16px;margin-bottom:16px">
          <span style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);letter-spacing:0.1em;text-transform:uppercase">Original Tagline</span>
          <div style="font-family:var(--font-head);font-size:1.05rem;font-style:italic;color:var(--text);margin-top:4px">"{slogan_to_translate}"</div>
        </div>""", unsafe_allow_html=True)

        if st.button("🌍  Translate to Selected Languages"):
            with st.spinner("Translating…"):
                results = translate_slogan(slogan_to_translate, bi.get("company","Brand"), langs)
                results = validate_translations(results)
                st.session_state.translations = results

        if st.session_state.translations:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            ml_cols = st.columns(min(len(st.session_state.translations), 3))
            for i, (lang, data) in enumerate(st.session_state.translations.items()):
                with ml_cols[i % 3]:
                    src_pill = "pill-g" if data.get("source") == "gemini" else "pill-a"
                    st.markdown(f"""
                    <div class="lang-card">
                      <div class="lang-name">{data['flag']} {lang} ({data['native']})</div>
                      <div class="lang-text">{data['text']}</div>
                      <div style="margin-top:8px;font-size:0.74rem;color:var(--muted)">{data.get('tone_note','')}</div>
                      <div style="margin-top:6px"><span class="pill {src_pill}">{data.get('source','')}</span></div>
                    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 8 — ANIMATION PREVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<p class="sec-label">Module 06 — Animated Visuals</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Animation <em>Preview</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs
        ac1, ac2 = st.columns([1, 2], gap="large")
        with ac1:
            style  = st.selectbox("Animation Style", ["typewriter", "fade", "slide"])
            frames = st.slider("Frames", 12, 30, 20)
        with ac2:
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">About this animation</p>
              <p style="font-size:0.85rem;color:var(--muted);line-height:1.65">
                Pillow-based GIF animation combining your brand logo initials, 
                colour palette, and tagline. Supports typewriter, fade-in, and slide-in effects.
                Output: 600×338px, optimised GIF.
              </p>
            </div>""", unsafe_allow_html=True)

        if st.button("🎬  Generate Brand Animation"):
            if not st.session_state.palette:
                st.warning("Generate brand kit first.")
            else:
                tag = (st.session_state.slogans[0]["text"]
                       if st.session_state.slogans else f"{bi['company']} — Excellence by Design")
                svg = (st.session_state.logos[st.session_state.selected_logo]["svg"]
                       if st.session_state.logos else "")
                with st.spinner("Rendering animation…"):
                    gif = create_brand_gif(svg, tag, st.session_state.palette,
                                           bi["company"], style, frames)
                    st.session_state.gif_bytes = gif

        if st.session_state.gif_bytes:
            st.image(st.session_state.gif_bytes, width=560)
            st.download_button("⬇ Download GIF",
                               data=st.session_state.gif_bytes,
                               file_name=f"{bi.get('company','brand')}_animation.gif",
                               mime="image/gif")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 8 — TREND RADAR
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<p class="sec-label">AI Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Industry <em>Trend Radar</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    bi = st.session_state.brand_inputs or {}
    ind_tr  = bi.get("industry",    "Technology / Software")
    pers_tr = bi.get("personality", "Professional")
    co_tr   = bi.get("company",     "Your Brand")

    st.markdown(f"""
    <div class="card">
      <div class="card-title">What is Trend Radar?</div>
      <div class="card-sub">
        AI-powered scan of the top industry trends shaping <strong>{ind_tr}</strong> in 2026.
        Each trend includes a momentum score and a specific brand strategy recommendation for <strong>{co_tr}</strong>.
      </div>
    </div>""", unsafe_allow_html=True)

    if st.button("📡  Scan Industry Trends", key="trend_scan_btn"):
        with st.spinner("Scanning trends for " + ind_tr + "…"):
            trend_data = generate_trend_radar(ind_tr, pers_tr, co_tr)
            st.session_state["trend_data"] = trend_data

    if st.session_state.get("trend_data"):
        td     = st.session_state["trend_data"]
        trends = td["trends"]
        source = td["source"]
        st.caption(f"Source: {'Gemini AI — live analysis' if source=='gemini' else 'Curated intelligence database'}")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Top Trends in ' + ind_tr + ' — 2026</p>', unsafe_allow_html=True)

        for i, t in enumerate(trends):
            momentum   = t.get("momentum", 75)
            direction  = t.get("direction", "up")
            arrow      = "↑" if "up" in str(direction).lower() else ("↓" if "down" in str(direction).lower() else "→")
            bar_color  = "#3ECFB2" if momentum >= 80 else "#C9A84C" if momentum >= 60 else "#E05A5A"
            border_col = "#C9A84C" if i == 0 else "var(--border)"

            st.markdown(f"""
            <div class="card" style="border-color:{border_col};margin-bottom:14px">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
                <div>
                  <span style="font-family:var(--font-mono);font-size:0.62rem;color:var(--accent);letter-spacing:0.1em">TREND {i+1}</span>
                  <div style="font-family:var(--font-head);font-size:1.2rem;font-weight:600;color:var(--text)">{t.get("trend","Trend")}</div>
                </div>
                <div style="text-align:right">
                  <div style="font-family:var(--font-head);font-size:2rem;font-weight:700;color:{bar_color}">{arrow}</div>
                  <div style="font-family:var(--font-mono);font-size:0.6rem;color:var(--muted)">MOMENTUM</div>
                </div>
              </div>
              <div style="background:var(--surface2);border-radius:4px;height:8px;overflow:hidden;margin-bottom:12px">
                <div style="width:{momentum}%;height:100%;background:{bar_color};border-radius:4px;transition:width 0.8s ease"></div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:10px">
                <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--muted)">MOMENTUM SCORE</span>
                <span style="font-family:var(--font-mono);font-size:0.68rem;color:{bar_color};font-weight:700">{momentum}/100</span>
              </div>
              <div style="background:rgba(201,168,76,0.06);border-left:3px solid var(--accent);padding:12px 14px;border-radius:0 8px 8px 0">
                <div style="font-family:var(--font-mono);font-size:0.56rem;color:var(--accent);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px">Brand Strategy for {co_tr}</div>
                <div style="font-size:0.88rem;line-height:1.65;color:var(--text)">{t.get("insight","")}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Radar chart using plotly
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Momentum Visualisation</p>', unsafe_allow_html=True)
        import plotly.graph_objects as go
        trend_names  = [t.get("trend","")[:20] + ("…" if len(t.get("trend","")) > 20 else "") for t in trends]
        trend_scores = [t.get("momentum", 75) for t in trends]
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Bar(
            x=trend_names, y=trend_scores,
            marker_color=["#C9A84C" if s >= 80 else "#3ECFB2" if s >= 60 else "#E05A5A" for s in trend_scores],
            text=[str(s) for s in trend_scores],
            textposition="outside",
        ))
        fig_tr.update_layout(
            paper_bgcolor="#141518", plot_bgcolor="#141518",
            font_color="#F0EDE8", font_family="DM Sans",
            height=280, margin=dict(t=20,b=20,l=20,r=20),
            yaxis=dict(range=[0,100], gridcolor="#2A2C31"),
            xaxis=dict(gridcolor="#2A2C31"),
            title=dict(text="Industry Trend Momentum Scores", font_color="#C9A84C", font_size=13),
        )
        st.plotly_chart(fig_tr, width="stretch")

        # Strategic summary
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Your Strategic Position</p>', unsafe_allow_html=True)
        top_trend = max(trends, key=lambda x: x.get("momentum", 0))
        st.markdown(f"""
        <div class="card">
          <p class="sec-label">Priority Action for {co_tr}</p>
          <p style="font-family:var(--font-head);font-size:1.1rem;font-style:italic;color:var(--text);line-height:1.7">
            "{top_trend.get('insight','')}"
          </p>
          <div style="margin-top:12px">
            <span class="pill pill-a">Top Trend: {top_trend.get('trend','')}</span>
            <span class="pill pill-g" style="margin-left:6px">Momentum: {top_trend.get('momentum',0)}/100</span>
          </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 9 — LAUNCH CHECKLIST
# ══════════════════════════════════════════════════════════════════════════════
with tabs[9]:
    st.markdown('<p class="sec-label">Go-To-Market</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Brand <em>Launch Checklist</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    bi = st.session_state.brand_inputs or {}

    st.markdown(f"""
    <div class="card">
      <div class="card-title">Personalised 30-Step Go-To-Market Plan</div>
      <div class="card-sub">A tailored brand launch checklist built specifically for {bi.get("company","your brand")} — covering Foundation, Visual Identity, Digital Presence, Launch Week, and Post-Launch phases.</div>
    </div>""", unsafe_allow_html=True)

    if st.button("✅  Generate My Launch Checklist", key="checklist_gen_btn"):
        if not bi:
            st.warning("Complete Brand Inputs first to personalise your checklist.")
        else:
            with st.spinner("Building your personalised checklist…"):
                checklist = generate_launch_checklist(bi)
                st.session_state["launch_checklist"] = checklist

    if "launch_checklist" not in st.session_state:
        st.session_state["launch_checklist"] = []

    if st.session_state["launch_checklist"]:
        checklist = st.session_state["launch_checklist"]
        done_count = sum(1 for t in checklist if t.get("done", False))
        total      = len(checklist)
        pct        = int(done_count / total * 100) if total > 0 else 0

        # Progress bar
        st.markdown(f"""
        <div style="margin:16px 0 24px">
          <div style="display:flex;justify-content:space-between;margin-bottom:6px">
            <span style="font-family:var(--font-mono);font-size:0.68rem;color:var(--muted)">LAUNCH PROGRESS — {done_count}/{total} STEPS</span>
            <span style="font-family:var(--font-mono);font-size:0.72rem;color:var(--accent);font-weight:700">{pct}%</span>
          </div>
          <div class="prog-wrap" style="height:12px"><div class="prog-bar" style="width:{pct}%"></div></div>
        </div>""", unsafe_allow_html=True)

        # Group by phase
        phases = ["Foundation", "Visual Identity", "Digital Presence", "Launch Week", "Post-Launch"]
        phase_icons = {"Foundation":"🏗", "Visual Identity":"🎨", "Digital Presence":"🌐", "Launch Week":"🚀", "Post-Launch":"📈"}

        for phase in phases:
            phase_items = [t for t in checklist if t.get("phase","") == phase]
            if not phase_items:
                continue
            phase_done = sum(1 for t in phase_items if t.get("done", False))
            icon = phase_icons.get(phase, "✦")

            with st.expander(f"{icon} {phase}  —  {phase_done}/{len(phase_items)} done", expanded=(phase == "Foundation")):
                for i, task in enumerate(phase_items):
                    priority = task.get("priority", "medium")
                    p_color  = "#E05A5A" if priority == "high" else "#C9A84C" if priority == "medium" else "#7A7A85"
                    done     = task.get("done", False)
                    step_num = task.get("step", i+1)

                    # Checkbox to mark done
                    checked = st.checkbox(
                        task.get("task",""),
                        value=done,
                        key=f"chk_{phase}_{step_num}",
                    )
                    # Update done state
                    task["done"] = checked

                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:-8px 0 10px 28px">
                      <span style="font-family:var(--font-mono);font-size:0.55rem;color:{p_color};border:1px solid {p_color};padding:1px 7px;border-radius:10px;text-transform:uppercase">{priority}</span>
                      <span style="font-family:var(--font-mono);font-size:0.52rem;color:var(--muted)">Step {step_num}</span>
                    </div>""", unsafe_allow_html=True)

        # Download checklist as text
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        checklist_txt = f"# {bi.get('company','Brand')} — Brand Launch Checklist\n\n"
        for phase in phases:
            items = [t for t in checklist if t.get("phase","") == phase]
            if items:
                checklist_txt += f"## {phase}\n"
                for t in items:
                    tick = "[x]" if t.get("done") else "[ ]"
                    checklist_txt += f"{tick} Step {t.get('step','')}: {t.get('task','')} [{t.get('priority','')}]\n"
                checklist_txt += "\n"

        st.download_button(
            "⬇ Download Checklist",
            data=checklist_txt,
            file_name=f"{bi.get('company','Brand').replace(' ','_')}_launch_checklist.txt",
            mime="text/plain",
            key="dl_checklist",
        )


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 10 — COMPETITOR GAP FINDER
# ══════════════════════════════════════════════════════════════════════════════
with tabs[10]:
    st.markdown('<p class="sec-label">Strategic Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Competitor <em>Gap Finder</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    bi = st.session_state.brand_inputs or {}
    co_cg   = bi.get("company",     "Your Brand")
    ind_cg  = bi.get("industry",    "Technology / Software")
    pers_cg = bi.get("personality", "Professional")

    st.markdown(f"""
    <div class="card">
      <div class="card-title">Find What Competitors Are Missing</div>
      <div class="card-sub">
        Describe a competitor and AI will identify their strategic blind spots —
        the gaps that <strong>{co_cg}</strong> can own in the <strong>{ind_cg}</strong> market.
        Works with or without a Gemini key.
      </div>
    </div>""", unsafe_allow_html=True)

    comp_desc = st.text_area(
        "Describe your competitor",
        placeholder='e.g. "They are the market leader in CRM software, known for complex enterprise solutions, high pricing, and a steep learning curve. Their brand feels corporate and cold."',
        height=120,
        key="comp_desc_input",
    )

    cg1, cg2 = st.columns(2, gap="large")
    with cg1:
        comp_name = st.text_input("Competitor name (optional)", placeholder="e.g. Salesforce", key="comp_name")
    with cg2:
        st.markdown('<div style="margin-top:28px"></div>', unsafe_allow_html=True)
        scan_btn = st.button("🔍  Find Strategic Gaps", key="gap_scan_btn", use_container_width=True)

    if scan_btn:
        with st.spinner("Analysing competitive landscape…"):
            gap_data = find_competitor_gaps(co_cg, ind_cg, pers_cg, comp_desc)
            st.session_state["gap_data"] = gap_data

    if st.session_state.get("gap_data"):
        gd     = st.session_state["gap_data"]
        gaps   = gd["gaps"]
        source = gd["source"]

        st.caption(f"Analysis: {'Gemini AI — live competitive intelligence' if source=='gemini' else 'Curated strategic framework for ' + ind_cg}")
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if comp_name:
            st.markdown(f'<p class="sec-label">Strategic gaps in {comp_name} that {co_cg} can own</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="sec-label">Strategic gaps {co_cg} can own in {ind_cg}</p>', unsafe_allow_html=True)

        for i, gap in enumerate(gaps):
            strength  = gap.get("strength", 80)
            bar_color = "#3ECFB2" if strength >= 85 else "#C9A84C" if strength >= 70 else "#E05A5A"
            rank_label = ["🥇 Highest Priority", "🥈 High Priority", "🥉 Medium Priority", "4️⃣ Opportunity"][min(i, 3)]

            st.markdown(f"""
            <div class="card" style="margin-bottom:14px">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:8px">
                <div>
                  <span style="font-family:var(--font-mono);font-size:0.56rem;color:var(--muted)">{rank_label}</span>
                  <div style="font-family:var(--font-head);font-size:1.15rem;font-weight:600;color:var(--text);margin-top:2px">{gap.get("gap","")}</div>
                </div>
                <div style="font-family:var(--font-head);font-size:1.6rem;font-weight:700;color:{bar_color};flex-shrink:0;margin-left:16px">{strength}</div>
              </div>
              <div style="background:var(--surface2);border-radius:4px;height:6px;overflow:hidden;margin-bottom:12px">
                <div style="width:{strength}%;height:100%;background:{bar_color};border-radius:4px"></div>
              </div>
              <div style="background:rgba(62,207,178,0.06);border-left:3px solid {bar_color};padding:12px 14px;border-radius:0 8px 8px 0">
                <div style="font-family:var(--font-mono);font-size:0.55rem;color:{bar_color};letter-spacing:0.1em;text-transform:uppercase;margin-bottom:5px">Your Opportunity</div>
                <div style="font-size:0.88rem;line-height:1.65;color:var(--text)">{gap.get("opportunity","")}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Summary call to action
        top_gap = max(gaps, key=lambda x: x.get("strength", 0))
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card" style="background:linear-gradient(135deg,#1B3A2A,#0C1A10);border:1px solid rgba(62,207,178,0.3)">
          <p class="sec-label" style="color:var(--teal)">Recommended First Move for {co_cg}</p>
          <p style="font-family:var(--font-head);font-size:1.1rem;font-style:italic;color:var(--text);line-height:1.7">
            Own <strong style="color:var(--teal)">{top_gap.get("gap","")}</strong> before your competitors respond.
          </p>
          <p style="font-size:0.84rem;color:var(--muted);margin-top:8px;line-height:1.6">{top_gap.get("opportunity","")}</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 11 — AUDIENCE PERSONA BUILDER
# ══════════════════════════════════════════════════════════════════════════════
with tabs[11]:
    st.markdown('<p class="sec-label">Market Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Audience <em>Persona Builder</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    bi = st.session_state.brand_inputs or {}
    co_pb   = bi.get("company",     "Your Brand")
    ind_pb  = bi.get("industry",    "Technology / Software")
    pers_pb = bi.get("personality", "Professional")
    aud_pb  = bi.get("audience",    "")
    tone_pb = bi.get("tone",        "professional")

    st.markdown(f"""
    <div class="card">
      <div class="card-title">3 Detailed Buyer Personas</div>
      <div class="card-sub">
        AI builds three research-grade customer profiles for <strong>{co_pb}</strong> —
        each with demographics, psychographics, pain points, buying triggers, and preferred channels.
        Use these to sharpen every piece of campaign copy and product decision.
      </div>
    </div>""", unsafe_allow_html=True)

    if st.button("👥  Build My Audience Personas", key="persona_gen_btn"):
        with st.spinner("Building buyer personas for " + co_pb + "…"):
            personas = build_audience_personas(co_pb, ind_pb, pers_pb, aud_pb, tone_pb)
            st.session_state["personas"] = personas

    if st.session_state.get("personas"):
        personas = st.session_state["personas"]
        PERSONA_COLORS = ["#C9A84C", "#3ECFB2", "#A29BFE"]

        for idx, persona in enumerate(personas):
            color = PERSONA_COLORS[idx % len(PERSONA_COLORS)]

            with st.expander(
                f"{'🥇' if idx==0 else '🥈' if idx==1 else '🥉'} Persona {idx+1}: {persona.get('name',f'Persona {idx+1}')}",
                expanded=(idx == 0)
            ):
                p1, p2 = st.columns([1, 1], gap="large")

                with p1:
                    # Demographics card
                    st.markdown(f"""
                    <div class="card" style="border-left:3px solid {color}">
                      <p class="sec-label" style="color:{color}">Demographics</p>
                      <div style="font-size:0.86rem;line-height:2;color:var(--text)">
                        <strong>Age:</strong> {persona.get("age","—")}<br>
                        <strong>Role:</strong> {persona.get("role","—")}<br>
                        <strong>Income:</strong> {persona.get("income","—")}<br>
                        <strong>Location:</strong> {persona.get("location","—")}
                      </div>
                    </div>""", unsafe_allow_html=True)

                    # Quote
                    st.markdown(f"""
                    <div style="background:rgba(201,168,76,0.06);border-left:3px solid {color};padding:14px 16px;border-radius:0 8px 8px 0;margin-top:14px">
                      <div style="font-family:var(--font-mono);font-size:0.55rem;color:{color};letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px">Their Voice</div>
                      <div style="font-family:var(--font-head);font-size:1.05rem;font-style:italic;color:var(--text);line-height:1.6">"{persona.get("quote","")}"</div>
                    </div>""", unsafe_allow_html=True)

                    # Channels
                    channels = persona.get("channels", [])
                    if channels:
                        ch_html = " ".join([f'<span class="pill pill-a">{ch}</span>' for ch in channels])
                        st.markdown(f"""
                        <div style="margin-top:14px">
                          <p class="sec-label">Preferred Channels</p>
                          <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px">{ch_html}</div>
                        </div>""", unsafe_allow_html=True)

                with p2:
                    # Pain points
                    pain_points = persona.get("pain_points", [])
                    if pain_points:
                        pp_html = "".join([
                            f'<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid var(--border)">'
                            f'<span style="color:#E05A5A;flex-shrink:0">✗</span>'
                            f'<span style="font-size:0.84rem;color:var(--text);line-height:1.5">{pp}</span></div>'
                            for pp in pain_points
                        ])
                        st.markdown(f"""
                        <div class="card">
                          <p class="sec-label" style="color:#E05A5A">Pain Points</p>
                          {pp_html}
                        </div>""", unsafe_allow_html=True)

                    # Buying triggers
                    triggers = persona.get("triggers", [])
                    if triggers:
                        tr_html = "".join([
                            f'<div style="display:flex;gap:10px;padding:8px 0;border-bottom:1px solid var(--border)">'
                            f'<span style="color:#3ECFB2;flex-shrink:0">✓</span>'
                            f'<span style="font-size:0.84rem;color:var(--text);line-height:1.5">{tr}</span></div>'
                            for tr in triggers
                        ])
                        st.markdown(f"""
                        <div class="card" style="margin-top:14px">
                          <p class="sec-label" style="color:#3ECFB2">Buying Triggers</p>
                          {tr_html}
                        </div>""", unsafe_allow_html=True)

        # Insight summary
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">How to Use These Personas</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card">
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;font-size:0.83rem;color:var(--text);line-height:1.65">
            <div>
              <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Campaign Copy</div>
              Address each persona's pain points directly in your ad headlines and captions.
            </div>
            <div>
              <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Channel Strategy</div>
              Allocate {co_pb}'s budget toward the channels where your primary persona spends time.
            </div>
            <div>
              <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Product Decisions</div>
              Let the top buying trigger guide your next feature launch or pricing decision.
            </div>
          </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 12 — FEEDBACK
# ══════════════════════════════════════════════════════════════════════════════
with tabs[12]:
    st.markdown('<p class="sec-label">Module 07 — Feedback Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Rate & <em>Refine</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    MODULES = ["Logo & Design Studio", "Creative Content Hub",
               "Campaign Analytics", "Multilingual Studio", "Overall Brand Kit"]
    fb_module = st.selectbox("Rate Module", MODULES)
    fb1, fb2  = st.columns([1, 2], gap="large")
    with fb1:
        rating = st.slider("Rating (1–5)", 1, 5, 4, label_visibility="collapsed")
        stars  = "⭐" * rating + "☆" * (5 - rating)
        quality = {1:"Poor",2:"Below Average",3:"Average",4:"Good",5:"Excellent"}[rating]
        pill   = "pill-r" if rating <= 2 else "pill-a" if rating == 3 else "pill-g"
        st.markdown(f'<div style="font-size:1.8rem;letter-spacing:4px;margin:10px 0">{stars}</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="pill {pill}">{quality}</span>', unsafe_allow_html=True)
    with fb2:
        comment   = st.text_area("Feedback", placeholder="What worked? What could be better?", height=90)
        preferred = st.text_input("Preferred Alternative (optional)", placeholder="e.g. More vibrant palette…")

    bi = st.session_state.brand_inputs
    if st.button("📤  Submit Feedback"):
        save_feedback(st.session_state.session_id,
                      bi.get("company",""), bi.get("industry",""),
                      fb_module, rating, comment, preferred)
        record = {"timestamp": datetime.datetime.now().isoformat(),
                  "module": fb_module, "rating": rating,
                  "sentiment": "positive" if rating >= 4 else "neutral" if rating == 3 else "negative",
                  "comment": comment}
        st.session_state.feedback_log.append(record)
        st.success(f"✓ Feedback saved — Rating {rating}/5 (written to feedback_data.csv)")

    if st.session_state.feedback_log:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Session Feedback Log</p>', unsafe_allow_html=True)
        df_log = pd.DataFrame(st.session_state.feedback_log)
        st.dataframe(df_log[["timestamp","module","rating","sentiment","comment"]]
                     .rename(columns={"timestamp":"Time","module":"Module",
                                      "rating":"Rating","sentiment":"Sentiment","comment":"Comment"}),
                     width='stretch', hide_index=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Feedback Analytics</p>', unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        with fc1:
            st.plotly_chart(feedback_bar(df_log), width='stretch')
        with fc2:
            st.plotly_chart(feedback_pie(df_log), width='stretch')

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 13 — DOWNLOAD KIT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[13]:
    st.markdown('<p class="sec-label">Module 08 — Export Engine</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Download Brand <em>Kit</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    bi = st.session_state.brand_inputs
    if not bi:
        st.info("👈 Complete Brand Inputs first.")
    else:
        # Progress checklist
        checks = [
            ("Brand Inputs",        bool(bi)),
            ("Logos Generated",     bool(st.session_state.logos)),
            ("Colour Palette",      bool(st.session_state.palette)),
            ("Font Recommendations",bool(st.session_state.fonts)),
            ("Taglines Created",    bool(st.session_state.slogans)),
            ("Brand Story",         bool(st.session_state.brand_story)),
            ("Translations",        bool(st.session_state.translations)),
            ("Campaign Content",    bool(st.session_state.campaigns)),
            ("KPI Predictions",     bool(st.session_state.kpis)),
            ("Animation",           bool(st.session_state.gif_bytes)),
        ]
        done = sum(1 for _, v in checks if v)
        pct  = int(done / len(checks) * 100)

        st.markdown(f"""
        <div style="margin-bottom:20px">
          <div style="display:flex;justify-content:space-between;margin-bottom:5px">
            <span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--muted)">KIT COMPLETENESS — {done}/{len(checks)}</span>
            <span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--accent)">{pct}%</span>
          </div>
          <div class="prog-wrap" style="height:12px"><div class="prog-bar" style="width:{pct}%"></div></div>
        </div>""", unsafe_allow_html=True)

        for label, done_flag in checks:
            icon  = "✓" if done_flag else "○"
            color = "var(--teal)" if done_flag else "var(--muted)"
            st.markdown(f"""
            <div class="check-item">
              <span style="color:{color}">{icon}</span>
              <span style="font-size:0.87rem;color:{'var(--text)' if done_flag else 'var(--muted)'}">{label}</span>
              {'<span class="pill pill-g" style="margin-left:auto">done</span>' if done_flag else ''}
            </div>""", unsafe_allow_html=True)

