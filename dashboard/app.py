import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
import sys
import os
import folium
from streamlit_folium import st_folium
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load.postgres import get_connection
from dashboard.statistique import (number_cities, get_cities, display_metrics, load_dashboard_data, filter_data,)

st.set_page_config(
    page_title="Weather Intelligence",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

AVAILABLE_CITIES = get_cities()
nombre_cities = number_cities()


LUCIDE = {
    "cloud-sun": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="M20 12h2"/><path d="m19.07 4.93-1.41 1.41"/><path d="M15.947 12.65a4 4 0 0 0-5.925-4.128"/><path d="M13 22H7a5 5 0 1 1 4.9-6H13a3 3 0 0 1 0 6Z"/></svg>',
    "map-pin": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>',
    "calendar": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>',
    "alert-triangle": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    "thermometer": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/></svg>',
    "droplets": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/></svg>',
    "wind": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.8 19.6A2 2 0 1 0 14 16H2"/><path d="M17.5 8a2.5 2.5 0 1 1 2 4H2"/><path d="M9.8 4.4A2 2 0 1 1 11 8H2"/></svg>',
    "cloud-lightning": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 16.326A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 .5 8.973"/><path d="m13 12-3 5h4l-3 5"/></svg>',
    "bar-chart-3": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
    "shield-alert": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',
    "line-chart": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
    "building-2": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>',
    "zap": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/></svg>',
    "activity": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/></svg>',
    "search": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "inbox": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>',
    "map": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.106 5.553a2 2 0 0 0 1.788 0l3.659-1.83A1 1 0 0 1 21 4.619v12.764a1 1 0 0 1-.553.894l-4.553 2.277a2 2 0 0 1-1.788 0l-4.212-2.106a2 2 0 0 0-1.788 0l-3.659 1.83A1 1 0 0 1 3 19.381V6.618a1 1 0 0 1 .553-.894l4.553-2.277a2 2 0 0 1 1.788 0z"/><path d="M15 5.764v15"/><path d="M9 3.236v15"/></svg>',
    "bar-chart": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>',
}


def ic(name: str) -> str:
    return LUCIDE.get(name, LUCIDE["activity"])


CSS = """
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">

<style>
:root {
    --bg-base:       #f0f7ff;
    --bg-surface:    #ffffff;
    --border-subtle: #dbeafe;
    --border-strong: #93c5fd;
    --accent:        #0ea5e9;
    --accent-soft:   #38bdf8;
    --accent-deep:   #0284c7;
    --text-primary:  #0c4a6e;
    --text-secondary:#64748b;
    --success:       #10b981;
    --warning:       #f59e0b;
    --danger:        #ef4444;
    --radius-sm:     10px;
    --radius-md:     16px;
    --shadow-soft:   0 4px 20px rgba(14,165,233,0.08);
    --shadow-glow:   0 15px 40px rgba(14,165,233,0.20);
    --grad-card:     linear-gradient(145deg, #ffffff, #f0f7ff);
    --grad-sky:      linear-gradient(135deg, #0ea5e9, #06b6d4);
}

html, body, [class*="css"] {
    font-family: "Inter", -apple-system, sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(56,189,248,0.10), transparent 40%),
        radial-gradient(circle at 85% 100%, rgba(251,191,36,0.06), transparent 45%),
        var(--bg-base) !important;
    color: var(--text-primary);
}

/* ── Header ─────────────────────────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

header[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}

button[data-testid="baseButton-headerNoPadding"],
button[kind="header"] {
    color: var(--accent-deep) !important;
    background: rgba(14,165,233,0.1) !important;
    border-radius: 8px !important;
    margin: 8px !important;
}

/* ── Sidebar ────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid var(--border-subtle);
    min-width: 300px !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem 1rem 1rem;
}

/* ── Icônes SVG ─────────────────────────────────────── */
.sidebar-logo-icon svg,
.filter-section-header svg,
.metric-icon-box svg,
.section-title-icon svg,
.sidebar-stats-icon svg,
.empty-state svg {
    width: 18px !important;
    height: 18px !important;
    stroke-width: 2;
    display: block;
    color: inherit;
}
.sidebar-logo-icon svg { width: 22px !important; height: 22px !important; }
.filter-section-header svg { width: 14px !important; height: 14px !important; }
.empty-state svg { width: 42px !important; height: 42px !important; }

/* ── Logo sidebar ───────────────────────────────────── */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 0 18px 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 20px;
}
.sidebar-logo-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    background: var(--grad-sky);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    box-shadow: 0 6px 20px rgba(14,165,233,0.35);
    flex-shrink: 0;
}
.sidebar-logo-text {
    font-size: 15px;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.1;
}
.sidebar-logo-sub {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: var(--text-secondary);
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Section header filtres ────────────────────────── */
.filter-section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 10px;
}
.filter-section-header svg { color: var(--accent); }

/* ── Labels sidebar ────────────────────────────────── */
section[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
}

/* ── Sidebar stats ─────────────────────────────────── */
.sidebar-stats {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    background: linear-gradient(135deg, #e0f2fe, #f0f9ff);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    margin-top: 16px;
}
.sidebar-stats-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: #ffffff;
    color: var(--accent-deep);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(14,165,233,0.12);
    flex-shrink: 0;
}
.sidebar-stats-label {
    font-size: 11px;
    color: var(--text-secondary);
    font-weight: 600;
    text-transform: uppercase;
}
.sidebar-stats-value {
    font-size: 18px;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.1;
}

/* ── Bouton reset sidebar ──────────────────────────── */
div[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: #ffffff !important;
    color: var(--accent-deep) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 700 !important;
    padding: 10px 16px !important;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--accent) !important;
    color: #ffffff !important;
    border-color: var(--accent) !important;
}

/* ═══════════════════════════════════════════════════
   METRIC CARDS
   ═══════════════════════════════════════════════════ */
.metric-card {
    background: var(--grad-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    padding: 22px !important;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-soft);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 8px;
}
.metric-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--grad-sky);
    opacity: 0;
    transition: opacity 0.3s;
}
.metric-card:hover::before { opacity: 1; }
.metric-card:hover {
    transform: translateY(-6px);
    border-color: var(--accent) !important;
    box-shadow: var(--shadow-glow);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.metric-title {
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin: 0;
}
.metric-icon-box {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    flex-shrink: 0;
}
.metric-icon-box.temp  { background: linear-gradient(135deg, #f59e0b, #ef4444); }
.metric-icon-box.humid { background: linear-gradient(135deg, #06b6d4, #0ea5e9); }
.metric-icon-box.wind  { background: linear-gradient(135deg, #38bdf8, #0284c7); }
.metric-icon-box.alert { background: linear-gradient(135deg, #ef4444, #b91c1c); }

.metric-value {
    color: var(--text-primary) !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    margin: 8px 0 4px 0;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.metric-subtitle {
    color: var(--accent-deep) !important;
    font-size: 13px !important;
    font-weight: 600;
    margin: 0;
}

/* ── Section Title ─────────────────────────────────── */
.section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 18px;
    font-weight: 700;
    margin: 30px 0 16px 0;
    color: var(--text-primary) !important;
}
.section-title-icon {
    width: 32px; height: 32px;
    border-radius: 9px;
    background: var(--grad-sky);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(14,165,233,0.25);
    flex-shrink: 0;
}

/* ── Empty state ───────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 50px 20px;
    border: 2px dashed var(--border-strong);
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    background: #ffffff;
}
.empty-state svg {
    color: var(--accent);
    margin: 0 auto 12px auto;
}

/* ── DataFrame ─────────────────────────────────────── */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden;
    box-shadow: var(--shadow-soft);
}

/* ── Texte principal ───────────────────────────────── */
h1, h2, h3, h4, h5, h6,
p, span, label {
    color: var(--text-primary);
}

/* ── Markdown block ────────────────────────────────── */
div[data-testid="stMarkdownContainer"] p {
    color: var(--text-primary);
}
</style>
"""

try:
    st.html(CSS)
except AttributeError:
    st.markdown(CSS, unsafe_allow_html=True)

hero_icon = ic("cloud-sun")
badge_activity = ic("activity")
badge_pin = ic("map-pin")
badge_zap = ic("zap")

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>
    html, body {{
        margin: 0; padding: 0;
        font-family: "Inter", sans-serif;
        background: transparent;
        overflow: hidden;
    }}

    .hero {{
        padding: 38px 35px;
        border-radius: 24px;
        background:
            radial-gradient(circle at 85% 20%, rgba(251,191,36,0.28), transparent 40%),
            radial-gradient(circle at 10% 90%, rgba(56,189,248,0.25), transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(14,165,233,0.08), transparent 60%),
            linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
        border: 1px solid #bae6fd;
        overflow: hidden;
        position: relative;
        box-shadow: 0 10px 40px rgba(14,165,233,0.12);
    }}

    .hero::after {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(120deg,
            transparent 40%,
            rgba(255,255,255,0.6) 50%,
            transparent 60%);
        animation: shimmer 8s infinite;
        pointer-events: none;
    }}

    @keyframes shimmer {{
        0%   {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}

    .hero-top {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        position: relative;
        z-index: 2;
    }}

    .hero-icon {{
        width: 56px; height: 56px;
        border-radius: 16px;
        background: linear-gradient(135deg, #0ea5e9, #06b6d4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(14,165,233,0.4);
    }}

    .hero-icon svg {{
        width: 30px; height: 30px;
        stroke-width: 2;
    }}

    .title {{
        font-size: 40px;
        font-weight: 800;
        color: #0c4a6e;
        margin: 0;
        letter-spacing: -0.02em;
    }}

    .subtitle {{
        color: #475569;
        font-size: 15px;
        text-align: center;
        margin-top: 12px;
        position: relative;
        z-index: 2;
        font-weight: 500;
        line-height: 1.5;
    }}

    .hero-badges {{
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 24px;
        flex-wrap: wrap;
        position: relative;
        z-index: 2;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 8px 15px;
        border-radius: 50px;
        font-size: 12.5px;
        font-weight: 700;
    }}

    .badge svg {{
        width: 14px; height: 14px;
        stroke-width: 2.5;
    }}

    .badge-success {{
        background: rgba(16,185,129,0.14);
        color: #059669;
        border: 1px solid rgba(16,185,129,0.3);
    }}
    .badge-info {{
        background: rgba(14,165,233,0.12);
        color: #0369a1;
        border: 1px solid rgba(14,165,233,0.3);
    }}
    .badge-sun {{
        background: rgba(251,191,36,0.16);
        color: #b45309;
        border: 1px solid rgba(251,191,36,0.35);
    }}

    .dot {{
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 0 0 rgba(16,185,129,0.7);
        animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }}
        70%  {{ box-shadow: 0 0 0 10px rgba(16,185,129,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(16,185,129,0); }}
    }}

    .glow {{
        position: absolute;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: #38bdf8;
        filter: blur(110px);
        opacity: 0.35;
        right: -60px; top: -60px;
        pointer-events: none;
    }}

    .glow-2 {{
        position: absolute;
        width: 180px; height: 180px;
        border-radius: 50%;
        background: #fbbf24;
        filter: blur(100px);
        opacity: 0.25;
        left: -50px; bottom: -50px;
        pointer-events: none;
    }}
</style>
</head>
<body>
    <div class="hero">
        <div class="glow"></div>
        <div class="glow-2"></div>

        <div class="hero-top">
            <div class="hero-icon">{hero_icon}</div>
            <h1 class="title">Weather Intelligence</h1>
        </div>

        <div class="subtitle">
            Weather forecast and risk analysis<br>
            for delivery operations in Morocco.
        </div>

        <div class="hero-badges">
            <div class="badge badge-success">
                <span class="dot"></span>
                {badge_activity}
                <span>Active system</span>
            </div>
            <div class="badge badge-info">
                {badge_pin}
                <span>Cities monitored : {nombre_cities}</span>
            </div>
            <div class="badge badge-sun">
                {badge_zap}
                <span>Real time</span>
            </div>
        </div>
    </div>

    <script>
        gsap.from(".hero",       {{ duration: 1,   y: 40,  opacity: 0, ease: "power3.out" }});
        gsap.from(".hero-icon",  {{ duration: 1,   scale: 0.5, opacity: 0, delay: 0.2, ease: "back.out(1.7)" }});
        gsap.from(".title",      {{ duration: 1,   x: -50, opacity: 0, delay: 0.3, ease: "power3.out" }});
        gsap.from(".subtitle",   {{ duration: 1,   x: -30, opacity: 0, delay: 0.45, ease: "power3.out" }});
        gsap.from(".badge",      {{ duration: 0.8, scale: 0.7, opacity: 0, delay: 0.7, stagger: 0.1, ease: "back.out(1.7)" }});
        gsap.to(".glow",   {{ scale: 1.3, opacity: 0.45, duration: 3, repeat: -1, yoyo: true, ease: "sine.inOut" }});
        gsap.to(".glow-2", {{ scale: 1.4, opacity: 0.35, duration: 4, repeat: -1, yoyo: true, ease: "sine.inOut" }});
    </script>
</body>
</html>
""", height=320)

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">{ic("cloud-sun")}</div>
        <div>
            <div class="sidebar-logo-text">Weather Intel</div>
            <div class="sidebar-logo-sub">Dashboard</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="filter-section-header">
        {ic("map-pin")}
        Cities
    </div>
    """, unsafe_allow_html=True)

    selected_cities = st.multiselect(
        "Select the cities",
        options=AVAILABLE_CITIES,
        default=AVAILABLE_CITIES[:1] if len(AVAILABLE_CITIES) >= 3 else AVAILABLE_CITIES,
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div class="filter-section-header" style="margin-top: 16px;">
        {ic("calendar")}
        Period
    </div>
    """, unsafe_allow_html=True)

    date_range = st.date_input(
        "Period",
        value=(pd.Timestamp.today() - pd.Timedelta(days=7), pd.Timestamp.today()),
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div class="filter-section-header" style="margin-top: 16px;">
        {ic("alert-triangle")}
        Minimum risk level
    </div>
    """, unsafe_allow_html=True)

    risk_options = ["Low", "Medium", "High"]
    selected_risk = st.select_slider(
        "Risk",
        options=risk_options,
        value="Low",
        label_visibility="collapsed",
    )

    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)

    if st.button("Réinitialiser les filtres", use_container_width=True):
        st.rerun()

    st.markdown(f"""
    <div class="sidebar-stats">
        <div class="sidebar-stats-icon">{ic("building-2")}</div>
        <div>
            <div class="sidebar-stats-label">Villes actives</div>
            <div class="sidebar-stats-value">{len(selected_cities)} / {nombre_cities}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def metric_card(title: str, value: str, subtitle: str, icon_name: str = "activity", variant: str = "temp"):
    """Carte KPI custom."""
    html = (
        f'<div class="metric-card">'
        f'  <div class="metric-header">'
        f'    <div class="metric-title">{title}</div>'
        f'    <div class="metric-icon-box {variant}">{ic(icon_name)}</div>'
        f'  </div>'
        f'  <div class="metric-value">{value}</div>'
        f'  <div class="metric-subtitle">{subtitle}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def section_title(text: str, icon_name: str = "activity"):
    html = (
        f'<div class="section-title">'
        f'  <div class="section-title-icon">{ic(icon_name)}</div>'
        f'  {text}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def empty_state(message: str, icon_name: str = "search"):
    html = (
        f'<div class="empty-state">'
        f'  {ic(icon_name)}'
        f'  <div>{message}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

USE_DB = True

try:
    df = load_dashboard_data(USE_DB)
except Exception as e:
    st.error(str(e))
    st.stop()

filtered_df = filter_data(df,selected_cities,selected_risk)

section_title("Key indicators", icon_name="bar-chart-3")
display_metrics(filtered_df, empty_state, metric_card)


section_title("Risk map of Morocco", icon_name="map")

if filtered_df.empty:
    empty_state("No cities to display on the map", icon_name="map")
else:
    map_df = (
        filtered_df.groupby("city", as_index=False)
        .agg({
            "lat": "first",
            "lng": "first",
            "risk_score": "max",
            "risk_level": lambda s: s.value_counts().idxmax(),
        })
    )

    RISK_COLORS = {
        "Low":    "#10b981",
        "Medium": "#f59e0b",
        "High":   "#ef4444",
    }

    m = folium.Map(
        location=[31.7917, -7.0926],
        zoom_start=5,
        tiles="CartoDB positron",
        control_scale=True,
    )

    for _, row in map_df.iterrows():
        if pd.isna(row["lat"]) or pd.isna(row["lng"]):
            continue

        color = RISK_COLORS.get(row["risk_level"], "#64748b")

        # Cercle coloré
        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=9,
            color="#ffffff",
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            tooltip=folium.Tooltip(
                f"<b>{row['city']}</b><br>"
                f"Risk: <b>{row['risk_level']}</b><br>"
                f"Score: {row['risk_score']}"
            ),
        ).add_to(m)

    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px; left: 30px;
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 8px 25px rgba(14,165,233,0.15);
        font-family: Inter, sans-serif;
        font-size: 13px;
        color: #0c4a6e;
        z-index: 9999;
    ">
        <div style="font-weight:800; margin-bottom:8px; font-size:12px; letter-spacing:0.8px; text-transform:uppercase; color:#64748b;">
            Risk level
        </div>
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:5px;">
            <span style="width:12px;height:12px;border-radius:50%;background:#10b981;display:inline-block;"></span>
            Low
        </div>
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:5px;">
            <span style="width:12px;height:12px;border-radius:50%;background:#f59e0b;display:inline-block;"></span>
            Medium
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="width:12px;height:12px;border-radius:50%;background:#ef4444;display:inline-block;"></span>
            High
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    st_folium(m, use_container_width=True, height=520, returned_objects=[])


section_title("Risk analysis by city", icon_name="shield-alert")

if filtered_df.empty:
    empty_state("No cities to display", icon_name="map")
else:
    def color_risk(val):
        return {
            "Low": "color: #10b981; font-weight: 700;",
            "Medium":  "color: #f59e0b; font-weight: 700;",
            "High":  "color: #ef4444; font-weight: 700;",
        }.get(val, "")

    styled = filtered_df.style.map(color_risk, subset=["risk_level"])
    st.dataframe(styled, use_container_width=True, hide_index=True)


section_title("Visualisations", icon_name="line-chart")

if filtered_df.empty:
    empty_state("No data to view", icon_name="bar-chart")
else:
    c1, c2 = st.columns(2, gap="medium")

    with c1:
        st.markdown("**Temperature by city**")
        st.bar_chart(
            filtered_df.set_index("city")["temperature_2m_max"],
            use_container_width=True,
            color="#0ea5e9",
        )

    with c2:
        st.markdown("**Humidity by city**")
        st.line_chart(
            filtered_df.set_index("city")["precipitation_probability_max"],
            use_container_width=True,
            color="#06b6d4",
        )


st.markdown("""
<div style="text-align:center; color:#64748b; font-size:12px; margin-top:40px; padding-top:20px; border-top:1px solid #dbeafe;">
    Weather Intelligence · © 2025 ·
</div>
""", unsafe_allow_html=True)