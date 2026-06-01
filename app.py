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

# Données initiales (une seule ligne par collège)
if 'data_history' not in st.session_state:
    st.session_state.data_history = [
        {
            "Collège": "Collège Jean Jaurès", 
            "Électricité (kWh)": 1200.0, "Gaz (m3)": 450.0, 
            "Déchets Alimentaires (kg)": 25.0, "Pain jeté (kg)": 5.0, 
            "Serviettes papier (unités)": 120, "Fruits entamés (kg)": 8.0, "Emballages (kg)": 14.0
        },
        {
            "Collège": "Collège Marie Curie", 
            "Électricité (kWh)": 980.0, "Gaz (m3)": 380.0, 
            "Déchets Alimentaires (kg)": 18.0, "Pain jeté (kg)": 2.0, 
            "Serviettes papier (unités)": 90, "Fruits entamés (kg)": 4.0, "Emballages (kg)": 9.0
        },
        {
            "Collège": "Collège Victor Hugo", 
            "Électricité (kWh)": 1450.0, "Gaz (m3)": 520.0, 
            "Déchets Alimentaires (kg)": 35.0, "Pain jeté (kg)": 9.0, 
            "Serviettes papier (unités)": 200, "Fruits entamés (kg)": 12.0, "Emballages (kg)": 22.0
        }
    ]

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
st.markdown("Mesurez, comparez et mettez à jour les consommations de vos établissements scolaires.")

tab1, tab2 = st.tabs(["📊 Classement & Comparaisons", "📝 Saisie des consommations"])

with tab1:
    st.header("📈 Tableau de bord comparatif")
    df = pd.DataFrame(st.session_state.data_history)
    
    # 1. SECTION ENERGIE
    st.subheader("⚡ Zoom sur les Énergies")
    col_en_1, col_en_2 = st.columns(2)
    
    with col_en_1:
        fig_elec = px.bar(df, x="Collège", y="Électricité (kWh)", color="Collège", 
                          title="Consommation d'Électricité (kWh)", text_auto=True,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_elec, use_container_width=True)
        
    with col_en_2:
        fig_gaz = px.bar(df, x="Collège", y="Gaz (m3)", color="Collège", 
                         title="Consommation de Gaz (m3)", text_auto=True,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_gaz, use_container_width=True)
        
    st.divider()
    
    # 2. SECTION CANTINE
    st.subheader("🍽️ Zoom sur la Cantine (Gaspillage et Déchets)")
    
    df_cantine = df.melt(id_vars=["Collège"], 
                         value_vars=["Déchets Alimentaires (kg)", "Pain jeté (kg)", "Serviettes papier (unités)", "Fruits entamés (kg)", "Emballages (kg)"],
                         var_name="Type de déchet", value_name="Quantité")
    
    fig_cantine = px.bar(df_cantine, x="Collège", y="Quantité", color="Type de déchet", barmode="group",
                         title="Comparatif détaillé des pertes à la cantine", text_auto=True,
                         color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_cantine, use_container_width=True)
    
    st.divider()
    
    # 3. LE TABLEAU RECAPITULATIF COMPLET
    st.subheader("📋 Tableau récapitulatif complet de toutes les données")
    st.dataframe(df, hide_index=True, use_container_width=True)

with tab2:
    if st.session_state.auth:
        st.header(f"✍️ Formulaire de saisie pour : {st.session_state.auth}")
        
        # Trouver les données actuelles de ce collège pour pré-remplir le formulaire
        current_data = next((item for item in st.session_state.data_history if item["Collège"] == st.session_state.auth), None)
        
        with st.form("form_saisie"):
            st.subheader("⚡ Consommation d'Énergie")
            c1, c2 = st.columns(2)
            elec = c1.number_input("Électricité consommée (kWh)", min_value=0.0, step=1.0, value=current_data["Électricité (kWh)"] if current_data else 0.0)
            gaz = c2.number_input("Gaz naturel consommé (m3)", min_value=0.0, step=1.0, value=current_data["Gaz (m3)"] if current_data else 0.0)
            
            st.subheader("🍽️ Pertes et Déchets de la Cantine")
            c3, c4, c5 = st.columns(3)
            dechets = c3.number_input("Déchets alimentaires globaux (kg)", min_value=0.0, step=0.5, value=current_data["Déchets Alimentaires (kg)"] if current_data else 0.0)
            pain = c4.number_input("Pain jeté / restes de pain (kg)", min_value=0.0, step=0.5, value=current_data["Pain jeté (kg)"] if current_data else 0.0)
            serviettes = c5.number_input("Serviettes en papier utilisées (unités)", min_value=0, step=1, value=int(current_data["Serviettes papier (unités)"]) if current_data else 0)
            
            c6, c7 = st.columns(2)
            fruits = c6.number_input("Fruits entamés ou non consommés (kg)", min_value=0.0, step=0.5, value=current_data["Fruits entamés (kg)"] if current_data else 0.0)
            emballages = c7.number_input("Emballages et plastiques jetés (kg)", min_value=0.0, step=0.5, value=current_data["Emballages (kg)"] if current_data else 0.0)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Écraser et mettre à jour les données 🚀")
            
            if submit:
                # 1. Supprimer l'ancienne ligne de CE collège uniquement
                st.session_state.data_history = [item for item in st.session_state.data_history if item["Collège"] != st.session_state.auth]
                
                # 2. Insérer les nouvelles données à la place
                new_data = {
                    "Collège": st.session_state.auth, 
                    "Électricité (kWh)": elec, "Gaz (m3)": gaz, 
                    "Déchets Alimentaires (kg)": dechets, "Pain jeté (kg)": pain, 
                    "Serviettes papier (unités)": serviettes, "Fruits entamés (kg)": fruits, "Emballages (kg)": emballages
                }
                st.session_state.data_history.append(new_data)
                st.success(f"Données du {st.session_state.auth} écrasées et mises à jour avec succès !")
                st.rerun()
    else:
        st.info("👈 Veuillez sélectionner votre collège et entrer son code secret dans la barre latérale pour débloquer le formulaire de saisie.")

st.sidebar.divider()
st.sidebar.caption("Outil développé pour le Défi Bas Carbone 2024")
