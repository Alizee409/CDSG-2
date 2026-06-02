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

# Données initiales
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

# Initialisation d'une variable pour suivre le succès de la soumission
if 'form_success' not in st.session_state:
    st.session_state.form_success = False

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
                st.session_state.form_success = False # Reset le message de succès au changement de session
                st.rerun()
            else:
                st.error("Code incorrect")
else:
    st.sidebar.success(f"Connecté : {st.session_state.auth}")
    if st.sidebar.button("Se déconnecter"):
        st.session_state.auth = None
        st.session_state.form_success = False
        st.rerun()

# --- INTERFACE PRINCIPALE ---
st.title("Défi Bas Carbone Inter-Collèges")

tab1, tab2 = st.tabs(["📊 Classement & Comparaisons", "📝 Saisie des consommations"])

with tab1:
    st.header("📈 Tableau de bord comparatif")
    df = pd.DataFrame(st.session_state.data_history)
    
    # 1. SECTION ENERGIE & EAU
    st.subheader("Zoom sur les Énergies & l'Eau")
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
        
        # Le formulaire reste sur place sans recharger toute la page
        with st.form("form_saisie", clear_on_submit=False):
            st.subheader("⚡ Énergie & Fluides")
            c1, c2, c3 = st.columns(3)
            elec = c1.number_input("Consommation Électricité (kWh)", min_value=0.0, step=1.0, value=current_data["Consommation Électricité (kWh)"] if current_data else 0.0)
            gaz = c2.number_input("Consommation Gaz (m3)", min_value=0.0, step=1.0, value=current_data["Consommation Gaz (m3)"] if current_data else 0.0)
            eau = c3.number_input("Consommation Eau (m3)", min_value=0.0, step=1.0, value=current_data["Consommation Eau (m3)"] if current_data else 0.0)
            
            st.subheader("🍽️ Pertes et Déchets de la Cantine")
            c4, c5, c6 = st.columns(3)
            dechets = c4.number_input("Déchets alimentaires globaux (kg)", min_value=0.0, step=0.5, value=current_data["Déchets Alimentaires (kg)"] if current_data else 0.0)
            pain = c5.number_input("Pain jeté / restes de pain (kg)", min_value=0.0, step=0.5, value=current_data["Pain jeté (kg)"] if current_data else 0.0)
            serviettes = c6.number_input("Serviettes en papier utilisées (kg)", min_value=0.0, step=0.1, value=current_data["Serviettes papier (kg)"] if current_data else 0.0)
            
            c7, c8 = st.columns(2)
            fruits = c7.number_input("Fruits entamés ou non consommés (kg)", min_value=0.0, step=0.5, value=current_data["Fruits entamés (kg)"] if current_data else 0.0)
            emballages = c8.number_input("Emballages et plastiques jetés (kg)", min_value=0.0, step=0.5, value=current_data["Emballages (kg)"] if current_data else 0.0)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Valider les données")
            
            if submit:
                # 1. Supprimer l'ancienne ligne du collège
                st.session_state.data_history = [item for item in st.session_state.data_history if item["Collège"] != st.session_state.auth]
                
                # 2. Insérer les nouvelles données dans le tableau
                new_data = {
                    "Collège": st.session_state.auth, 
                    "Consommation Électricité (kWh)": elec, "Consommation Gaz (m3)": gaz, "Consommation Eau (m3)": eau,
                    "Déchets Alimentaires (kg)": dechets, "Pain jeté (kg)": pain, 
                    "Serviettes papier (kg)": serviettes, "Fruits entamés (kg)": fruits, "Emballages (kg)": emballages
                }
                st.session_state.data_history.append(new_data)
                
                # On active le flag de succès et on recharge la page pour actualiser l'onglet 1
                st.session_state.form_success = True
                st.rerun()

        # 3. Affichage des messages de succès à l'EXTÉRIEUR du formulaire
        if st.session_state.form_success:
            st.toast("🌍 Données mises à jour avec succès !", icon="🎉")
            st.success("🎉 C'est fait ! Les graphiques ont été mis à jour dans l'autre onglet. Merci !", icon="✅")
            st.balloons()
            # On repasse à False pour éviter que les ballons reviennent en boucle si on clique ailleurs
            st.session_state.form_success = False

    else:
        st.info("👈 Veuillez sélectionner votre collège et entrer son code secret dans la barre latérale pour débloquer le formulaire de saisie.")

st.sidebar.divider()
st.sidebar.caption("Outil développé pour le Défi Bas Carbone 2026")
