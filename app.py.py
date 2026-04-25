import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. CONFIGURATION VISUELLE : MÉLANGE DESIGN ÉCLATANT
# ==========================================
st.set_page_config(
    page_title="CardioPanel Elite | High-Tech", 
    page_icon="🏥", 
    layout="wide"
)

# Design CSS : Blanc + Bleu Marine + Orange Douceur + Rouge Vif
st.markdown("""
    <style>
    /* Fond : Blanc pur avec subtil dégradé orange/bleu très clair */
    .stApp {
        background-color: #ffffff;
        background-image: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%); /* Orange très très doux en fond */
        background-attachment: fixed;
    }
    
    /* Barre latérale : Bleu Marine Profond */
    [data-testid="stSidebar"] {
        background-color: #001f3f !important; /* Marine */
        color: white !important;
    }
    
    /* Titres : Bleu Marine */
    h1, h2, h3 {
        color: #001f3f !important;
        font-family: 'Trebuchet MS', sans-serif;
        font-weight: bold;
    }

    /* Cartes de saisie : Blanc avec bordure Orange Doux */
    .stForm {
        background-color: white !important;
        border-radius: 20px !important;
        border: 2px solid #ffb347 !important; /* Orange doux */
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
    }
    
    /* Bouton d'envoi : Rouge Vif Éclatant */
    .stButton>button {
        background: linear-gradient(45deg, #ff0000 0%, #e60000 100%) !important; /* Rouge Vif */
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        height: 60px;
        font-size: 20px !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 20px rgba(230, 0, 0, 0.3) !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 30px rgba(230, 0, 0, 0.5) !important;
        filter: brightness(1.2);
    }

    /* Métriques : Bleu Marine & Rouge */
    [data-testid="stMetricValue"] {
        color: #ff0000 !important; /* Rouge pour les chiffres clés */
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
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=90)
    st.markdown("<h1 style='color:white; font-size:24px;'>CARDIO ELITE</h1>", unsafe_allow_html=True)
    st.markdown("---")
    choix = st.radio("NAVIGATION", ["📥 ENREGISTREMENT", "📊 ANALYSE EXPERTE"])
    st.markdown("---")
    st.warning("Mode : Administrateur Clinique")

if choix == "📥 ENREGISTREMENT":
    st.title("🏥 Dossier Patient Digital")
    st.markdown("<p style='color:#001f3f;'>Saisie des paramètres vitaux de haute précision.</p>", unsafe_allow_html=True)
    
    with st.form("form_vif"):
        col1, col2 = st.columns(2)
        with col1:
            pid = st.text_input("📋 Code Patient Unique", placeholder="ex: PAT-007")
            age = st.number_input("📅 Âge du Patient", 1, 100, 40)
        with col2:
            st.markdown("<span style='color:#ffb347; font-weight:bold;'>💓 Tension Systolique</span>", unsafe_allow_html=True)
            tens = st.slider("", 80, 200, 120)
            chol = st.number_input("🩸 Cholestérol (mg/dL)", 100, 450, 200)
        
        glyc = st.selectbox("🍏 Statut Glycémique", ["Normal", "Élevé", "Alerte Critique"])
        
        # Bouton Rouge Vif
        submit = st.form_submit_button("🔥 ENREGISTRER MAINTENANT")
        
        if submit:
            if pid:
                new_data = {
                    "Date": datetime.now().strftime("%H:%M"),
                    "Patient_ID": pid, "Age": age, 
                    "Tension_Systolique": tens, "Cholesterol": chol, "Glycemie": glyc
                }
                st.session_state.sante_db = pd.concat([st.session_state.sante_db, pd.DataFrame([new_data])], ignore_index=True)
                st.balloons()
                st.success(f"Fiche de {pid} synchronisée !")
            else:
                st.error("L'ID Patient est requis.")

else:
    st.title("📊 Rapport Diagnostique")
    
    if st.session_state.sante_db.empty:
        st.info("Aucune donnée disponible pour l'analyse.")
    else:
        df = st.session_state.sante_db
        
        # Métriques Marine et Rouge
        m1, m2, m3 = st.columns(3)
        m1.metric("COHORTE", len(df))
        m2.metric("MOY. TENSION", f"{round(df['Tension_Systolique'].mean(),1)}")
        m3.metric("MOY. CHOL.", f"{round(df['Cholesterol'].mean(),1)}")
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            # Graphique Bleu Marine
            fig1 = px.histogram(df, x="Tension_Systolique", title="Distribution Tension", color_discrete_sequence=['#001f3f'])
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            # Graphique Orange Doux
            fig2 = px.scatter(df, x="Age", y="Cholesterol", title="Âge vs Cholestérol", color_discrete_sequence=['#ffb347'])
            st.plotly_chart(fig2, use_container_width=True)

        st.table(df)