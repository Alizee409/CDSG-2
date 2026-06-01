import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(page_title="Défi Bas Carbone Collèges", layout="wide")

# Liste des collèges autorisés et leurs codes d'accès
COLLEGES_AUTH = {
    "Collège Jean Jaurès": "JAURES2024",
    "Collège Marie Curie": "CURIE2024",
    "Collège Victor Hugo": "HUGO2024"
}

# Données fictives pour le tableau comparatif
if 'data_history' not in st.session_state:
    st.session_state.data_history = [
        {"Collège": "Collège Jean Jaurès", "Élec (kWh)": 1200, "Gaz (m3)": 450, "Déchets (kg)": 25, "Pain (kg)": 5, "CO2 (kg)": 312},
        {"Collège": "Collège Marie Curie", "Élec (kWh)": 980, "Gaz (m3)": 380, "Déchets (kg)": 18, "Pain (kg)": 2, "CO2 (kg)": 245}
    ]

# --- CONNEXION ---
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

# --- INTERFACE ---
st.title("🌱 Défi Bas Carbone Inter-Collèges")

tab1, tab2 = st.tabs(["📊 Classement & Comparaisons", "📝 Saisie des consommations"])

with tab1:
    st.header("Résultats actuels")
    df = pd.DataFrame(st.session_state.data_history)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.bar(df, x="Collège", y="CO2 (kg)", color="Collège", title="Impact Carbone Total")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Tableau de bord")
        st.table(df[["Collège", "CO2 (kg)"]].sort_values("CO2 (kg)"))

with tab2:
    if st.session_state.auth:
        st.header(f"Saisie pour {st.session_state.auth}")
        with st.form("form_saisie"):
            st.subheader("⚡ Énergie")
            elec = st.number_input("Électricité (kWh)", min_value=0.0)
            gaz = st.number_input("Gaz (m3)", min_value=0.0)
            
            st.subheader("🍎 Cantine")
            c1, c2 = st.columns(2)
            dechets = c1.number_input("Déchets alimentaires (kg)", min_value=0.0)
            pain = c2.number_input("Pain jeté (kg)", min_value=0.0)
            serviettes = st.number_input("Serviettes papier (unités)", min_value=0)
            fruits = st.number_input("Fruits entamés (kg)", min_value=0.0)
            emballages = st.number_input("Emballages plastiques (kg)", min_value=0.0)
            
            if st.form_submit_button("Valider les données"):
                # Calcul CO2 simplifié
                co2_calc = (elec * 0.1) + (gaz * 2.0) + (dechets * 1.5)
                st.session_state.data_history.append({
                    "Collège": st.session_state.auth, "Élec (kWh)": elec, "Gaz (m3)": gaz, 
                    "Déchets (kg)": dechets, "Pain (kg)": pain, "CO2 (kg)": round(co2_calc, 1)
                })
                st.success("Données enregistrées !")
    else:
        st.info("👈 Veuillez vous connecter dans la barre latérale pour saisir vos données.")
