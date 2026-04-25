import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="CardioCheck - Analyse Santé", layout="wide")

# Simulation d'une base de données locale (pour le TP)
if 'sante_db' not in st.session_state:
    st.session_state.sante_db = pd.DataFrame(columns=[
        "Date", "Patient_ID", "Age", "Tension_Systolique", "Cholesterol", "Glycemie"
    ])

def interface_collecte():
    st.header("Collecte des Paramètres Vitaux")
    
    with st.form("form_sante"):
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("Identifiant Patient (Anonymisé)")
            age = st.number_input("Âge", min_value=1, max_value=120, value=30)
        with col2:
            tension = st.slider("Tension Systolique (mmHg)", 80, 200, 120)
            chol = st.number_input("Taux de Cholestérol (mg/dL)", 100, 400, 190)
        
        glycemie = st.selectbox("Niveau de Glycémie à jeun", ["Normal", "Élevé"])
        submit = st.form_submit_button("Enregistrer les données")

        if submit:
            nouvelle_entree = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Patient_ID": patient_id,
                "Age": age,
                "Tension_Systolique": tension,
                "Cholesterol": chol,
                "Glycemie": glycemie
            }
            st.session_state.sante_db = pd.concat([st.session_state.sante_db, pd.DataFrame([nouvelle_entree])], ignore_index=True)
            st.success("Données synchronisées avec le serveur.")

def interface_analyse():
    st.header("Tableau de Bord Descriptif")
    
    if st.session_state.sante_db.empty:
        st.info("Aucune donnée disponible pour l'analyse.")
        return

    df = st.session_state.sante_db
    
    # Métriques Clés
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Patients", len(df))
    m2.metric("Tension Moyenne", round(df["Tension_Systolique"].mean(), 1))
    m3.metric("Âge Moyen", round(df["Age"].mean(), 1))

    # Visualisations
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Distribution de la Tension")
        fig_hist = px.histogram(df, x="Tension_Systolique", nbins=10, color_discrete_sequence=['#ff4b4b'])
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        st.subheader("Relation Âge / Cholestérol")
        fig_scatter = px.scatter(df, x="Age", y="Cholesterol", trendline="ols")
        st.plotly_chart(fig_scatter, use_container_width=True)

# Navigation
menu = ["Collecte", "Analyse Descriptive"]
choix = st.sidebar.radio("Navigation", menu)

if choix == "Collecte":
    interface_collecte()
else:
    interface_analyse()