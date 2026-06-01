import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Défi Bas Carbone Collèges", layout="wide")

# Liste des collèges autorisés et leurs codes d'accès
COLLEGES_AUTH = {
    "Collège Jean Jaurès": "JAURES2024",
    "Collège Marie Curie": "CURIE2024",
    "Collège Victor Hugo": "HUGO2024"
}

# Données initiales (avec l'Eau ajoutée !)
if 'data_history' not in st.session_state:
    st.session_state.data_history = [
        {
            "Collège": "Collège Jean Jaurès", 
            "Consommation Électricité (kWh)": 1200.0, "Consommation Gaz (m3)": 450.0, "Consommation Eau (m3)": 30.0,
            "Déchets Alimentaires (kg)": 25.0, "Pain jeté (kg)": 5.0, 
            "Serviettes papier (kg)": 4.2, "Fruits entamés (kg)": 8.0, "Emballages (kg)": 14.0
        },
        {
            "Collège": "Collège Marie Curie", 
            "Consommation Électricité (kWh)": 980.0, "Consommation Gaz (m3)": 380.0, "Consommation Eau (m3)": 22.0,
            "Déchets Alimentaires (kg)": 18.0, "Pain jeté (kg)": 2.0, 
            "Serviettes papier (kg)": 3.1, "Fruits entamés (kg)": 4.0, "Emballages (kg)": 9.0
        },
        {
            "Collège": "Collège Victor Hugo", 
            "Consommation Électricité (kWh)": 1450.0, "Consommation Gaz (m3)": 520.0, "Consommation Eau (m3)": 45.0,
            "Déchets Alimentaires (kg)": 35.0, "Pain jeté (kg)": 9.0, 
            "Serviettes papier (kg)": 6.5, "Fruits entamés (kg)": 12.0, "Emballages (kg)": 22.0
        }
    ]

# Gestion du message de succès géant
if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# --- SYSTEME DE CONNEXION ---
if 'auth' not in st.session_state:
    st.session_state.auth = None

st.sidebar.title("🔐 Accès Collège")
if st.session_state.auth is None:
    with st.sidebar:
        college_sel = st.selectbox("Sélectionnez votre établissement", [""] + list(COLLEGES_AUTH.keys()))
        password = st.text_input("Code secret", type="password")
        if st.button("Se connecter"):
            if COLLEGES_AUTH.get(college_sel) == password:
                st.session_state.auth = college_sel
                st.rerun()
            else:
                st.error("Code incorrect")
else:
    st.sidebar.success(f"Connecté : {st.session_state.auth}")
    if st.sidebar.button("Se déconnecter"):
        st.session_state.auth = None
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("🌱 Défi Bas Carbone Inter-Collèges")

# Affichage du message GÉANT si validation
if st.session_state.show_success:
    st.markdown("""
        <div style="text-align: center; padding: 40px; background-color: #d8f3dc; border-radius: 20px; border: 4px solid #52b788; margin-bottom: 30px; animation: pulse 1s infinite;">
            <h1 style="color: #1b4332; font-size: 70px; margin: 0;">🎉 C'est fait ! Merci ! 🌍</h1>
            <p style="color: #2d6a4f; font-size: 20px; margin-top: 10px;">Vos données ont été enregistrées et les graphiques sont à jour.</p>
        </div>
        """, unsafe_allow_html=True)
    st.balloons()
    st.session_state.show_success = False # Réinitialise pour la prochaine fois

tab1, tab2 = st.tabs(["📊 Classement & Comparaisons", "📝 Saisie des consommations"])

with tab1:
    st.header("📈 Tableau de bord comparatif")
    df = pd.DataFrame(st.session_state.data_history)
    
    # 1. SECTION ENERGIE & EAU
    st.subheader("⚡ Zoom sur les Énergies & l'Eau")
    col_en_1, col_en_2, col_en_3 = st.columns(3)
    
    with col_en_1:
        fig_elec = px.bar(df, x="Collège", y="Consommation Électricité (kWh)", color="Collège", 
                          title="Consommation Électricité (kWh)", text_auto=True,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_elec, use_container_width=True)
        
    with col_en_2:
        fig_gaz = px.bar(df, x="Collège", y="Consommation Gaz (m3)", color="Collège", 
                         title="Consommation Gaz (m3)", text_auto=True,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_gaz, use_container_width=True)

    with col_en_3:
        fig_eau = px.bar(df, x="Collège", y="Consommation Eau (m3)", color="Collège", 
                         title="Consommation Eau (m3)", text_auto=True,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_eau, use_container_width=True)
        
    st.divider()
    
    # 2. SECTION CANTINE
    st.subheader("🍽️ Zoom sur la Cantine (Gaspillage et Déchets)")
    df_cantine = df.melt(id_vars=["Collège"], 
                         value_vars=["Déchets Alimentaires (kg)", "Pain jeté (kg)", "Serviettes papier (kg)", "Fruits entamés (kg)", "Emballages (kg)"],
                         var_name="Type de déchet", value_name="Quantité (kg)")
    
    fig_cantine = px.bar(df_cantine, x="Collège", y="Quantité (kg)", color="Type de déchet", barmode="group",
                         title="Comparatif détaillé des pertes à la cantine (en kg)", text_auto=True,
                         color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_cantine, use_container_width=True)
    
    st.divider()
    
    # 3. LE TABLEAU RECAPITULATIF COMPLET
    st.subheader("📋 Tableau récapitulatif complet de toutes les données")
    st.dataframe(df, hide_index=True, use_container_width=True)

with tab2:
    if st.session_state.auth:
        st.header(f"✍️ Formulaire de saisie pour : {st.session_state.auth}")
        
        current_data = next((item for item in st.session_state.data_history if item["Collège"] == st.session_state.auth), None)
        
        with st.form("form_saisie"):
            st.subheader("⚡ Énergie & Fluides")
            c1, c2, c3 = st.columns(3)
            elec = c1.number_input("
