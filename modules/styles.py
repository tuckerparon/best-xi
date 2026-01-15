import streamlit as st

def apply_custom_styles(
    bg_color="#e0e0e0",
    text_color="#222",
    secondary_text="#000",
    alert_bg="#e3f0ff",
    header_text="#fff"
):
    """Applies custom CSS styling with parameterized colors."""
    css = f"""
    <style>
    /* Center the tab navigation and set text color */
    div[data-baseweb="tab-list"] {{
        justify-content: center !important;
    }}
    button[data-baseweb="tab"] p {{
        color: #000 !important;
    }}
    button[data-baseweb="tab"] {{
        color: #000 !important;
    }}

    /* Main app background and text */
    .stApp {{background-color: {bg_color}; color: {text_color} !important;}}
    
    .stMarkdown, .css-10trblm, .css-1v0mbdj, .css-1d391kg, .css-1cpxqw2 {{
        color: {text_color} !important;
    }}
    
    .stMarkdownContainer {{color: {secondary_text} !important;}}
    
    /* Step subtext / Widget labels */
    label[data-testid="stWidgetLabel"] p, label[data-testid="stWidgetLabel"] {{
        color: #000 !important;
    }}
    
    /* Alert/Warning styling */
    .stAlert {{
        background-color: {alert_bg} !important; 
        border-radius: 0.5rem !important;
        overflow: hidden !important;
        border: none !important;
        font-weight: bold !important;
    }}
    .stAlert div {{
        color: #000 !important;
    }}
    .stAlert p {{
        color: #000 !important;
    }}
    
    /* Table headers */
    th[role="columnheader"] {{
        color: {header_text} !important; 
        font-weight: bold !important;
    }}

    /* ... include other styles from app.py here using variables ... */
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)