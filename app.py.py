import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. CONFIGURATION : ORANGE GÉOMÉTRIQUE & MATÉRIEL MÉDICAL
# ==========================================
st.set_page_config(
    page_title="CardioPanel Elite | Équipement Clinique", 
    page_icon="🩺", 
    layout="wide"
)

# Design CSS : Orange Brûlé + Motifs Cubes + Style Matériel
st.markdown("""
    <style>
    /* Fond Orange avec motifs géométriques (Cubes) */
    .stApp {
        background-color: #d35400;
        background-image: url("https://www.transparenttextures.com/patterns/cubes.png");
        background-attachment: fixed;
    }
    
    /* Barre latérale Bleu Marine */
    [data-testid="stSidebar"] {
        background-color: #001f3f !important;
        border-right: 3px solid #ff0000;
    }
    
    /* Titres avec lueur blanche */
    h1, h2 {
        color: white !important;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        font-family: 'Trebuchet MS', sans-serif;
        text-transform: uppercase;
    }

    /* Cartes de saisie : Style "Laboratoire" */
    .stForm {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 25px !important;
        border-left: 10px solid #001f3f !important;
        padding: 40px !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
    }
    
    /* Bouton Rouge Vif Hyper-Visible */
    .stButton>button {
        background: linear-gradient(90deg, #ff0000 0%, #cc0000 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 60px;
        font-size: 22px !important;
        font-weight: 900 !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(255, 0, 0, 0.4) !important;
    }
    .stButton>button:hover {
        transform: translateY(-5px);
        filter: brightness(1.2);
    }

    /* Métriques blanches */
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 40px !important;
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
    st.image("https://cdn-icons-png.flaticon.com/512/822/822118.png", width=120) # Icône Hôpital
    st.markdown("<h2 style='color:white; text-align:center;'>CARDIO ELITE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    choix = st.radio("SÉLECTIONNER UN MODULE", ["📋 SAISIE MATÉRIEL", "📊 ANALYSE EXPERTE"])
    st.markdown("---")
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=50)

if choix == "📋 SAISIE MATÉRIEL":
    # En-tête avec matériel médical
    c_titre, c_materiel = st.columns([0.7, 0.3])
    with c_titre:
        st.title("🩺 Unité de Mesures Vitales")
        st.markdown("<p style='color:white; font-size:20px;'>Enregistrement via terminaux cliniques</p>", unsafe_allow_html=True)
    with c_materiel:
        st.image("https://cdn-icons-png.flaticon.com/512/1040/1040237.png", width=150) # Image Stéthoscope

    with st.form("form_ultra"):
        st.markdown("### 🧬 Paramètres de Diagnostic")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.image("https://cdn-icons-png.flaticon.com/512/4807/4807695.png", width=40) # Icône ID
            pid = st.text_input("IDENTIFIANT PATIENT UNIQUE", placeholder="PAT-XXXX")
            
            st.image("https://cdn-icons-png.flaticon.com/512/3063/3063201.png", width=40) # Icône Tension
            tens = st.slider("TENSION SYSTOLIQUE (mmHg)", 80, 200, 120)
            
        with col_b:
            st.image("https://cdn-icons-png.flaticon.com/512/3004/3004458.png", width=40) # Icône Age
            age = st.number_input("ÂGE ACTUEL", 1, 105, 40)
            
            st.image("https://cdn-icons-png.flaticon.com/512/4334/4334130.png", width=40) # Icône Sang
            chol = st.number_input("TAUX DE CHOLESTÉROL (mg/dL)", 100, 450, 190)
        
        st.markdown("---")
        st.image("https://cdn-icons-png.flaticon.com/512/2864/2864261.png", width=40) # Icône Glycémie
        glyc = st.selectbox("STATUT DE LA GLYCÉMIE", ["Normal", "Élevé", "Critique"])
        
        # Le gros bouton Rouge
        submit = st.form_submit_button("🔥 SYNCHRONISER AVEC LE SERVEUR")
        
        if submit:
            if pid:
                new_entry = {
                    "Date": datetime.now().strftime("%H:%M"),
                    "Patient_ID": pid, "Age": age, 
                    "Tension_Systolique": tens, "Cholesterol": chol, "Glycemie": glyc
                }
                st.session_state.sante_db = pd.concat([st.session_state.sante_db, pd.DataFrame([new_entry])], ignore_index=True)
                st.balloons()
                st.success(f"Données du patient {pid} sécurisées avec succès.")
            else:
                st.error("Erreur : L'Identifiant est obligatoire.")

else:
    st.title("📊 Centre de Monitoring")
    st.image("https://cdn-icons-png.flaticon.com/512/2785/2785239.png", width=100) # Icône Stats
    
    if st.session_state.sante_db.empty:
        st.info("Aucune donnée enregistrée.")
    else:
        df = st.session_state.sante_db
        
        # Métriques avec colonnes
        m1, m2, m3 = st.columns(3)
        m1.metric("COHORTE", f"{len(df)}")
        m2.metric("TENSION MOY.", f"{round(df['Tension_Systolique'].mean(),1)}")
        m3.metric("CHOL. MOY.", f"{round(df['Cholesterol'].mean(),1)}")
        
        st.markdown("---")
        
        # Graphiques
        ca, cb = st.columns(2)
        with ca:
            fig1 = px.histogram(df, x="Tension_Systolique", color_discrete_sequence=['#001f3f'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig1, use_container_width=True)
        with cb:
            fig2 = px.scatter(df, x="Age", y="Cholesterol", color_discrete_sequence=['#ff0000'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig2, use_container_width=True)

        st.table(df)