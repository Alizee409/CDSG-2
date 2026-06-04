import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import json
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Défi Bas Carbone Collèges", layout="wide")

# --- GESTION DE LA BASE DE DONNÉES LOCALE (JSON) ---
FICHIER_COLLEGES = "colleges.json"
FICHIER_DONNEES = "donnees.json"

# Données par défaut si les fichiers n'existent pas encore
COLLEGES_PAR_DEFAUT = {
    "Collège Jean Jaurès": "JAURES2024",
    "Collège Marie Curie": "CURIE2024",
    "Collège Victor Hugo": "HUGO2024"
}

DONNEES_PAR_DEFAUT = [
    {"Collège": "Collège Jean Jaurès", "Consommation Électricité (kWh)": 1200.0, "Consommation Gaz (m3)": 450.0, "Consommation Eau (m3)": 30.0, "Déchets Alimentaires (kg)": 25.0, "Pain jeté (kg)": 5.0, "Serviettes papier (kg)": 4.2, "Fruits entamés (kg)": 8.0, "Emballages (kg)": 14.0},
    {"Collège": "Collège Marie Curie", "Consommation Électricité (kWh)": 980.0, "Consommation Gaz (m3)": 380.0, "Consommation Eau (m3)": 22.0, "Déchets Alimentaires (kg)": 18.0, "Pain jeté (kg)": 2.0, "Serviettes papier (kg)": 3.1, "Fruits entamés (kg)": 4.0, "Emballages (kg)": 9.0},
    {"Collège": "Collège Victor Hugo", "Consommation Électricité (kWh)": 1450.0, "Consommation Gaz (m3)": 520.0, "Consommation Eau (m3)": 45.0, "Déchets Alimentaires (kg)": 35.0, "Pain jeté (kg)": 9.0, "Serviettes papier (kg)": 6.5, "Fruits entamés (kg)": 12.0, "Emballages (kg)": 22.0}
]

# Fonctions pour lire/écrire les fichiers
def charger_colleges():
    if not os.path.exists(FICHIER_COLLEGES):
        with open(FICHIER_COLLEGES, "w", encoding="utf-8") as f:
            json.dump(COLLEGES_PAR_DEFAUT, f, ensure_ascii=False, indent=4)
        return COLLEGES_PAR_DEFAUT
    with open(FICHIER_COLLEGES, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_colleges(data):
    with open(FICHIER_COLLEGES, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def charger_donnees():
    if not os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
            json.dump(DONNEES_PAR_DEFAUT, f, ensure_ascii=False, indent=4)
        return DONNEES_PAR_DEFAUT
    with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_donnees(data):
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Chargement initial des données réelles
COLLEGES_AUTH = charger_colleges()
st.session_state.data_history = charger_donnees()

if 'form_success' not in st.session_state:
    st.session_state.form_success = False

if 'auth' not in st.session_state:
    st.session_state.auth = None


# --- DÉFINITION DES PAGES ---

def page_tableau_de_bord():
    """Page principale : Classement, Graphiques et Saisie"""
    st.sidebar.title("🔐 Accès Collège")
    if st.session_state.auth is None:
        with st.sidebar:
            college_sel = st.selectbox("Sélectionnez votre établissement", [""] + list(COLLEGES_AUTH.keys()))
            password = st.text_input("Code secret", type="password")
            if st.button("Se connecter"):
                if COLLEGES_AUTH.get(college_sel) == password:
                    st.session_state.auth = college_sel
                    st.session_state.form_success = False
                    st.rerun()
                else:
                    st.error("Code incorrect")
    else:
        st.sidebar.success(f"Connecté : {st.session_state.auth}")
        if st.sidebar.button("Se déconnecter"):
            st.session_state.auth = None
            st.session_state.form_success = False
            st.rerun()

    st.title("🌱 Défi Bas Carbone Inter-Collèges")
    tab1, tab2 = st.tabs(["📊 Classement & Comparaisons", "📝 Saisie des consommations"])

    with tab1:
        st.header("📈 Tableau de bord comparatif")
        df = pd.DataFrame(st.session_state.data_history)
        
        st.subheader("⚡ Zoom sur les Énergies & l'Eau")
        col_en_1, col_en_2, col_en_3 = st.columns(3)
        
        with col_en_1:
            fig_elec = px.bar(df, x="Collège", y="Consommation Électricité (kWh)", color="Collège", 
                              title="Consommation Électricité (kWh)", text_auto=True, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_elec, use_container_width=True)
            
        with col_en_2:
            fig_gaz = px.bar(df, x="Collège", y="Consommation Gaz (m3)", color="Collège", 
                             title="Consommation Gaz (m3)", text_auto=True, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_gaz, use_container_width=True)

        with col_en_3:
            fig_eau = px.bar(df, x="Collège", y="Consommation Eau (m3)", color="Collège", 
                             title="Consommation Eau (m3)", text_auto=True, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_eau, use_container_width=True)
            
        st.divider()
        
        st.subheader("🍽️ Zoom sur la Cantine")
        df_cantine = df.melt(id_vars=["Collège"], value_vars=["Déchets Alimentaires (kg)", "Pain jeté (kg)", "Serviettes papier (kg)", "Fruits entamés (kg)", "Emballages (kg)"], var_name="Type de déchet", value_name="Quantité (kg)")
        fig_cantine = px.bar(df_cantine, x="Collège", y="Quantité (kg)", color="Type de déchet", barmode="group", title="Comparatif des pertes (kg)", text_auto=True, color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_cantine, use_container_width=True)
        
        st.divider()
        st.subheader("📋 Tableau récapitulatif complet")
        st.dataframe(df, hide_index=True, use_container_width=True)

    with tab2:
        if st.session_state.auth:
            st.header(f"✍️ Formulaire de saisie pour : {st.session_state.auth}")
            current_data = next((item for item in st.session_state.data_history if item["Collège"] == st.session_state.auth), None)
            
            with st.form("form_saisie", clear_on_submit=False):
                st.subheader("⚡ Énergie & Fluides")
                c1, c2, c3 = st.columns(3)
                elec = c1.number_input("Consommation Électricité (kWh)", min_value=0.0, step=1.0, value=current_data["Consommation Électricité (kWh)"] if current_data else 0.0)
                gaz = c2.number_input("Consommation Gaz (m3)", min_value=0.0, step=1.0, value=current_data["Consommation Gaz (m3)"] if current_data else 0.0)
                eau = c3.number_input("Consommation Eau (m3)", min_value=0.0, step=1.0, value=current_data["Consommation Eau (m3)"] if current_data else 0.0)
                
                st.subheader("🍽️ Pertes et Déchets")
                c4, c5, c6 = st.columns(3)
                dechets = c4.number_input("Déchets alimentaires globaux (kg)", min_value=0.0, step=0.5, value=current_data["Déchets Alimentaires (kg)"] if current_data else 0.0)
                pain = c5.number_input("Pain jeté (kg)", min_value=0.0, step=0.5, value=current_data["Pain jeté (kg)"] if current_data else 0.0)
                serviettes = c6.number_input("Serviettes en papier (kg)", min_value=0.0, step=0.1, value=current_data["Serviettes papier (kg)"] if current_data else 0.0)
                
                c7, c8 = st.columns(2)
                fruits = c7.number_input("Fruits entamés (kg)", min_value=0.0, step=0.5, value=current_data["Fruits entamés (kg)"] if current_data else 0.0)
                emballages = c8.number_input("Emballages jetés (kg)", min_value=0.0, step=0.5, value=current_data["Emballages (kg)"] if current_data else 0.0)
                
                # --- AJOUT DU GRAPHIQUE ROND EN TEMPS RÉEL ---
                st.write("---")
                st.subheader("📊 Aperçu en temps réel de la répartition des déchets")
                
                # Création d'un dictionnaire temporaire avec les valeurs en direct des inputs
                dict_direct = {
                    "Type de déchet": ["Déchets Alimentaires", "Pain jeté", "Serviettes papier", "Fruits entamés", "Emballages"],
                    "Quantité (kg)": [dechets, pain, serviettes, fruits, emballages]
                }
                df_direct = pd.DataFrame(dict_direct)
                
                # On s'assure qu'il y a au moins une valeur supérieure à 0 pour afficher le graphique rond
                if df_direct["Quantité (kg)"].sum() > 0:
                    fig_live = px.pie(df_direct, values="Quantité (kg)", names="Type de déchet",
                                      title=f"Répartition des pertes pour {st.session_state.auth}",
                                      color_discrete_sequence=px.colors.qualitative.Set2)
                    # Configuration pour rendre le graphique grand et lisible
                    fig_live.update_layout(height=500)
                    st.plotly_chart(fig_live, use_container_width=True)
                else:
                    st.info("Veuillez saisir des valeurs supérieures à 0 pour voir le graphique circulaire.")
                st.write("---")
                
                submit = st.form_submit_button("Valider les données")
                
                if submit:
                    # Charger les dernières données du fichier pour éviter les conflits
                    donnees_actuelles = charger_donnees()
                    donnees_nettoyees = [item for item in donnees_actuelles if item["Collège"] != st.session_state.auth]
                    
                    new_data = {
                        "Collège": st.session_state.auth, "Consommation Électricité (kWh)": elec, "Consommation Gaz (m3)": gaz, "Consommation Eau (m3)": eau,
                        "Déchets Alimentaires (kg)": dechets, "Pain jeté (kg)": pain, "Serviettes papier (kg)": serviettes, "Fruits entamés (kg)": fruits, "Emballages (kg)": emballages
                    }
                    donnees_nettoyees.append(new_data)
                    
                    # SAUVEGARDE PHYSIQUE DANS LE FICHIER
                    sauvegarder_donnees(donnees_nettoyees)
                    
                    st.session_state.form_success = True
                    st.rerun()

            if st.session_state.form_success:
                st.toast("🌍 Données enregistrées dans le fichier !", icon="🎉")
                st.success("🎉 C'est fait ! Les données sont sauvegardées de manière permanente.", icon="✅")
                st.balloons()
                st.session_state.form_success = False
        else:
            st.info("👈 Veuillez vous connecter dans la barre latérale.")


def page_adhesion():
    """Formulaire de demande d'adhésion"""
    st.title("📝 Demande d'adhésion au Défi")
    
    with st.form("form_adhesion", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nom_etab = st.text_input("Nom de l'établissement *")
            email_etab = st.text_input("Adresse mail de contact *")
            tel_etab = st.text_input("Téléphone de l'établissement *")
        with col2:
            ville = st.text_input("Ville *")
            region = st.text_input("Région *")
        message = st.text_area("Votre message", placeholder="Bonjour...")
        
        envoyer = st.form_submit_button("Envoyer la demande d'adhésion")
        if envoyer:
            if not nom_etab or not email_etab or not tel_etab or not ville or not region:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires.")
            else:
                form_html = f"""
                <form id="hidden_form" action="https://formsubmit.co/atissiercharras@gmail.com" method="POST" style="display:none;">
                    <input type="text" name="Nom Etablissement" value="{nom_etab}"><input type="email" name="Email Contact" value="{email_etab}"><input type="text" name="Telephone" value="{tel_etab}"><input type="text" name="Ville" value="{ville}"><input type="text" name="Region" value="{region}"><textarea name="Message">{message}</textarea><input type="hidden" name="_next" value="https://formsubmit.co/thanks"><input type="hidden" name="_subject" value="Nouvelle inscription : {nom_etab}">
                </form>
                <script>document.getElementById('hidden_form').submit();</script>
                """
                components.html(form_html, height=0, width=0)
                st.success("✉️ Demande envoyée à atissiercharras@gmail.com !")
                st.balloons()


def page_admin():
    """NOUVELLE PAGE : Panneau pour ajouter un collège sans toucher au code"""
    st.title("⚙️ Panneau Administrateur")
    st.subheader("Ajouter manuellement un nouvel établissement autorisé")
    
    # Mot de passe secret pour protéger cette page (Optionnel mais recommandé)
    admin_password = st.text_input("Mot de passe Administrateur", type="password")
    
    if admin_password == "ADMIN2026": # <--- Change ce mot de passe secret si tu veux !
        with st.form("form_admin_add"):
            nouveau_nom = st.text_input("Nom du nouveau collège (Ex: Collège Pasteur)")
            nouveau_code = st.text_input("Code secret à lui attribuer (Ex: PASTEUR2026)")
            
            bouton_creer = st.form_submit_button("➕ Ajouter l'établissement")
            
            if bouton_creer:
                if nouveau_nom and nouveau_code:
                    colleges_actuels = charger_colleges()
                    donnees_actuelles = charger_donnees()
                    
                    if nouveau_nom in colleges_actuels:
                        st.error("❌ Ce collège existe déjà !")
                    else:
                        # 1. Ajouter aux collèges autorisés
                        colleges_actuels[nouveau_nom] = nouveau_code
                        sauvegarder_colleges(colleges_actuels)
                        
                        # 2. Créer une ligne de données vide (initialisée à 0) pour ce collège
                        nouvelle_ligne_vide = {
                            "Collège": nouveau_nom, "Consommation Électricité (kWh)": 0.0, "Consommation Gaz (m3)": 0.0, "Consommation Eau (m3)": 0.0,
                            "Déchets Alimentaires (kg)": 0.0, "Pain jeté (kg)": 0.0, "Serviettes papier (kg)": 0.0, "Fruits entamés (kg)": 0.0, "Emballages (kg)": 0.0
                        }
                        donnees_actuelles.append(nouvelle_ligne_vide)
                        sauvegarder_donnees(donnees_actuelles)
                        
                        st.success(f"🎉 Le {nouveau_nom} a été ajouté avec succès sans effacer les autres !")
                        st.balloons()
                else:
                    st.warning("⚠️ Remplissez les deux champs.")
    elif admin_password != "":
        st.error("Mot de passe administrateur incorrect.")


# --- NAVIGATION ---
p1 = st.Page(page_tableau_de_bord, title="📊 Tableau de bord & Saisie", icon="🌱")
p2 = st.Page(page_adhesion, title="📝 Demander l'adhésion", icon="✉️")
p3 = st.Page(page_admin, title="⚙️ Admin : Ajouter un collège", icon="🔒")

pg = st.navigation([p1, p2, p3])
pg.run()

st.sidebar.divider()
st.sidebar.caption("Outil développé pour le Défi Bas Carbone 2026")
