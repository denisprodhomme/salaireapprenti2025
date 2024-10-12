import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Simulateur Salaire Apprenti", layout="wide")

# Colonne de contexte
st.sidebar.title("Pourquoi ce simulateur ?")
st.sidebar.write(
    "Ceci est un simulateur de calcul de salaire net pour un apprenti avec les données disponibles au 11/10/2024. \n\n"
    "Le Projet de Loi de Finances de la Sécurité Sociale a été annoncé hier, apportant des changements notamment sur les cotisations des apprentis. \n\n"
    "Si ce texte est voté, voici les changements qui s'appliqueraient.\n\n"
    "L'exemple présenté utilise un apprenti rémunéré selon un pourcentage du SMIC, avec des cotisations classiques."
)
st.sidebar.markdown(
    "[Suivez-moi sur LinkedIn](https://www.linkedin.com/in/denis-prodhomme-64831317a/)"
)


st.title("Salaire Apprenti version 2024 versus version 2025 dans le PLFSS")


# Slider global pour le pourcentage du SMIC
pourcentage_smic = st.slider("Pourcentage du SMIC", 20, 100, 70, step=1, help="Sélectionnez le pourcentage du SMIC.")

# Calcul pour 2024
smic_2024 = 11.88
salaire_brut_horaire_2024 = (pourcentage_smic / 100) * smic_2024
salaire_brut_mensuel_2024 = round(salaire_brut_horaire_2024 * 151.67, 2)

seuil_cotisations_2024 = 0.79 * smic_2024
salaire_soumis_cotisations_2024 = max(0, salaire_brut_horaire_2024 - seuil_cotisations_2024) * 151.67
assurance_vieillesse_deplafonnee_2024 = round(salaire_soumis_cotisations_2024 * 0.0040 if salaire_brut_horaire_2024 >= seuil_cotisations_2024 else 0, 2)
assurance_vieillesse_plafonnee_2024 = round(salaire_soumis_cotisations_2024 * 0.0690 if salaire_brut_horaire_2024 >= seuil_cotisations_2024 else 0, 2)
retraite_t1_2024 = round(salaire_soumis_cotisations_2024 * 0.0315 if salaire_brut_horaire_2024 >= seuil_cotisations_2024 else 0, 2)
ceg_t1_2024 = round(salaire_soumis_cotisations_2024 * 0.0086 if salaire_brut_horaire_2024 >= seuil_cotisations_2024 else 0, 2)

cotisations_salariales_2024 = round(
    assurance_vieillesse_deplafonnee_2024 + 
    assurance_vieillesse_plafonnee_2024 + 
    retraite_t1_2024 + 
    ceg_t1_2024, 2
)

salaire_net_mensuel_2024 = round(salaire_brut_mensuel_2024 - cotisations_salariales_2024, 2)

# Calcul pour 2025
smic_2025 = 11.88
salaire_brut_horaire_2025 = (pourcentage_smic / 100) * smic_2025
salaire_brut_mensuel_2025 = round(salaire_brut_horaire_2025 * 151.67, 2)

seuil_cotisations_2025 = 0.50 * smic_2025
salaire_soumis_cotisations_2025 = max(0, salaire_brut_horaire_2025 - seuil_cotisations_2025) * 151.67
assurance_vieillesse_deplafonnee_2025 = round(salaire_soumis_cotisations_2025 * 0.0040 if salaire_brut_horaire_2025 >= seuil_cotisations_2025 else 0, 2)
assurance_vieillesse_plafonnee_2025 = round(salaire_soumis_cotisations_2025 * 0.0690 if salaire_brut_horaire_2025 >= seuil_cotisations_2025 else 0, 2)
retraite_t1_2025 = round(salaire_soumis_cotisations_2025 * 0.0315 if salaire_brut_horaire_2025 >= seuil_cotisations_2025 else 0, 2)
ceg_t1_2025 = round(salaire_soumis_cotisations_2025 * 0.0086 if salaire_brut_horaire_2025 >= seuil_cotisations_2025 else 0, 2)
csg_crds_2025 = round(salaire_brut_mensuel_2025 * 0.097 * 0.9825 if salaire_brut_horaire_2025 >= seuil_cotisations_2025 else 0, 2)

cotisations_salariales_2025 = round(
    assurance_vieillesse_deplafonnee_2025 + 
    assurance_vieillesse_plafonnee_2025 + 
    retraite_t1_2025 + 
    ceg_t1_2025 + 
    csg_crds_2025, 2
)

salaire_net_mensuel_2025 = round(salaire_brut_mensuel_2025 - cotisations_salariales_2025, 2)

# Créer un DataFrame pour afficher les résultats sous forme de tableau
data = {
    "Type": ["Salaire Apprenti 2024", "Salaire Apprenti 2025"],
    "Assurance vieillesse déplafonnée": [assurance_vieillesse_deplafonnee_2024, assurance_vieillesse_deplafonnee_2025],
    "Assurance vieillesse plafonnée": [assurance_vieillesse_plafonnee_2024, assurance_vieillesse_plafonnee_2025],
    "Retraite T1": [retraite_t1_2024, retraite_t1_2025],
    "CEG T1": [ceg_t1_2024, ceg_t1_2025],
    "CSG CRDS": [0, csg_crds_2025],  # Pas de CSG CRDS en 2024
    "Total cotisations": [cotisations_salariales_2024, cotisations_salariales_2025],
    "Salaire net mensuel": [salaire_net_mensuel_2024, salaire_net_mensuel_2025]
}

df = pd.DataFrame(data)

# Appliquer le style pour arrondir les valeurs à 2 décimales seulement pour les colonnes numériques
numeric_cols = df.select_dtypes(include=['float', 'int']).columns
st.table(df.style.format({col: "{:.2f}" for col in numeric_cols}))

# Créer un graphique en barres
bar_data = {
    "Année": ["2024", "2024", "2025", "2025"],
    "Type": ["Brut", "Net", "Brut", "Net"],
    "Montant": [salaire_brut_mensuel_2024, salaire_net_mensuel_2024, salaire_brut_mensuel_2025, salaire_net_mensuel_2025]
}

bar_df = pd.DataFrame(bar_data)

# Spécifier les couleurs des barres dans l'ordre souhaité
colors = ["#6200EE", "#03DAC6"]

fig = px.bar(bar_df, x="Année", y="Montant", color="Type", barmode="group",
             color_discrete_sequence=colors,
             labels={"Montant": "Montant (€)"})

# Ajouter des labels au survol
fig.update_traces(texttemplate='%{y:.2f} €', textposition='outside')

# Afficher le graphique
st.plotly_chart(fig, use_container_width=True)