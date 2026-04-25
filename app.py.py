import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. CONFIGURATION VISUELLE & "WAOOUH EFFECT"
# ==========================================
st.set_page_config(
    page_title="CardioPanel PRO v1.2 | High-Tech Santé", 
    page_icon="🧬", 
    layout="wide"
)

# Design CSS : Mode Sombre, Glassmorphism et Néons
st.markdown("""
    <style>
    /* Fond de l'application sombre avec lueurs diffuses */
    .stApp {
        background-color: #030a13;
        background-image: radial-gradient(circle at 15% 30%, rgba(26, 82, 118, 0.3) 0%, rgba(0, 0, 0, 0) 40%),
                          radial-gradient(circle at 85% 70%, rgba(192, 57, 43, 0.2) 0%, rgba(0, 0, 0, 0) 40%);
        background-attachment: fixed;
    }
    
    /* Barre latérale High-Tech */
    [data-testid="stSidebar"] {
        background-color: #051426;
        color: #ecf0f1;
        border-right: 1px solid rgba(52, 152, 219, 0.3);
    }
    
    /* Titres avec effet néon */
    h1, h2 {
        color: white !important;
        text-shadow: 0 0 15px rgba(52, 152, 219, 0.8);
        font-family: 'Montserrat', sans-serif;
    }

    /* Texte général en blanc/gris clair pour lisibilité */
    .stMarkdown, p, label {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Cartes en verre translucide (Glassmorphism) */
    .stForm, div[data-testid="stMetricBlock"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important;
    }
    
    /* Bouton d'envoi Premium */
    .stButton>button {
        background: linear-gradient(45deg, #c0392b 0%, #e74c3c 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        height: 50px;
        width: 100%;
        font-weight: bold !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.4s ease !important;
        box-shadow: 0 4px 15px rgba(192, 57, 43, 0.4) !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(192, 57, 43, 0.7) !important;
        background: linear-gradient(45deg, #e74c3c 0%, #ff6b6b 100%) !important;
    }

    /* Style des inputs */
    input, select, .stSlider {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGIQUE DE DONNÉES
# ==========================================
if 'sante_db' not in st.session_state:
    st.session_state.sante_db = pd.DataFrame(columns=[
        "Date", "Patient_ID", "Age", "Tension_Systolique", "Cholesterol", "Glycemie"
    ])

# ==========================================
# 3. INTERFACE UTILISATEUR
# ==========================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
    st.title("CardioPanel PRO")
    st.markdown("---")
    choix = st.radio("SÉLECTIONNER UN MODULE", ["📋 Saisie Constantes", "📊 Analyse High-Tech"])
    st.markdown("---")
    st.info("Système de monitoring en temps réel.")

if choix == "📋 Saisie Constantes":
    st.title("🧬 Enregistrement Patient")
    
    with st.form("form_medical"):
        col1, col2 = st.columns(2)
        with col1:
            pid = st.text_input("🆔 Code Patient", placeholder="ex: CARDIO-001")
            age = st.number_input("📅 Âge", 1, 110, 45)
        with col2:
            tens = st.slider("💓 Tension Systolique", 80, 200, 120)
            chol = st.number_input("🩸 Cholestérol (mg/dL)", 100, 400, 190)
        
        glyc = st.selectbox("🍞 Niveau Glycémie", ["Normal", "Élevé", "Critique"])
        
        submit = st.form_submit_button("🩺 SYNCHRONISER LES DONNÉES")
        
        if submit:
            if pid:
                new_data = {
                    "Date": datetime.now().strftime("%H:%M:%S"),
                    "Patient_ID": pid, "Age": age, 
                    "Tension_Systolique": tens, "Cholesterol": chol, "Glycemie": glyc
                }
                st.session_state.sante_db = pd.concat([st.session_state.sante_db, pd.DataFrame([new_data])], ignore_index=True)
                st.balloons()
                st.success(f"Données de {pid} envoyées au serveur.")
            else:
                st.error("Veuillez saisir un identifiant.")

else:
    st.title("📊 Centre d'Analyse Avancée")
    
    if st.session_state.sante_db.empty:
        st.warning("Base de données vide. Veuillez saisir des patients.")
    else:
        df = st.session_state.sante_db
        
        # Métriques lumineuses
        m1, m2, m3 = st.columns(3)
        m1.metric("PATIENTS", len(df))
        m2.metric("TENSION MOY.", f"{round(df['Tension_Systolique'].mean(),1)}")
        m3.metric("ÂGE MOYEN", f"{round(df['Age'].mean(),1)}")
        
        st.markdown("---")
        
        col_left, col_right = st.columns(2)
        with col_left:
            fig1 = px.histogram(df, x="Tension_Systolique", title="Distribution Tension", color_discrete_sequence=['#e74c3c'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_right:
            fig2 = px.scatter(df, x="Age", y="Cholesterol", title="Corrélation Âge/Cholestérol", color="Glycemie")
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(df.style.highlight_max(axis=0, color='#1a5276'))