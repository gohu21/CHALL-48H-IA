import streamlit as st
import pandas as pd
import plotly.express as px

# Définir le thème Streamlit
st.set_page_config(
    page_title="Tableau de Bord Interactif des KPIs Twitter",
    page_icon=":bar_chart:",
    layout="wide",
)

# Ajouter un titre principal avec un style amélioré
st.title("Tableau de Bord Interactif des KPIs Twitter :chart_with_upwards_trend:")

# Ajouter une description
st.markdown("""
    Ce tableau de bord interactif vous permet d'explorer les indicateurs clés de performance (KPIs)
    extraits des données Twitter. Utilisez les filtres ci-dessous pour personnaliser votre analyse.
""")

# Charger les données depuis le fichier CSV
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

file_path = "./output/KPIs_global.csv"
df = load_data(file_path)

# Conversion de la colonne 'date' en format datetime
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Remplacer les valeurs manquantes par 0 dans les colonnes numériques
numeric_columns = ['nombre_tweets_par_jour', 'nombre_mentions_engie', 'nombre_tweets_critiques', 'auteurs_uniques', '%_tweets_critiques', '%_mentions_engie', 'nombre_tweets_par_semaine', 'nombre_tweets_par_mois', 'nombre_tweets_par_heure']
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Sidebar pour les filtres
with st.sidebar:
    st.header("Filtres :wrench:")

    # Filtre pour la granularité temporelle
    time_granularity = st.selectbox("Granularité Temporelle", ["Jour", "Semaine", "Mois"])

    # Filtre pour la plage de dates (uniquement pour la granularité "Jour")
    if time_granularity == "Jour" and 'date' in df.columns:
        min_date = df['date'].min()
        max_date = df['date'].max()
        start_date, end_date = st.date_input(
            "Plage de Dates",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
        )
        df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
    else:
        start_date = None
        end_date = None

# Définir les colonnes pour l'affichage des KPIs
kpi1, kpi2, kpi3 = st.columns(3)

# KPI 1: Nombre total de tweets
if time_granularity == "Jour":
    total_tweets = df['nombre_tweets_par_jour'].sum()
    kpi1_title = "Nombre Total de Tweets par Jour"
elif time_granularity == "Semaine":
    total_tweets = df['nombre_tweets_par_semaine'].sum()
    kpi1_title = "Nombre Total de Tweets par Semaine"
else:  # Mois
    total_tweets = df['nombre_tweets_par_mois'].sum()
    kpi1_title = "Nombre Total de Tweets par Mois"

kpi1.metric(
    label=kpi1_title,
    value=f"{total_tweets:,.0f}",
    delta=None,
)

# KPI 2: Nombre total de mentions Engie
total_mentions = df['nombre_mentions_engie'].sum()

kpi2.metric(
    label="Nombre Total de Mentions Engie",
    value=f"{total_mentions:,.0f}",
    delta=None,
)

# KPI 3: Nombre total de tweets critiques
total_critiques = df['nombre_tweets_critiques'].sum()

kpi3.metric(
    label="Nombre Total de Tweets Critiques",
    value=f"{total_critiques:,.0f}",
    delta=None,
)

st.markdown("""---""")

# Graphiques
col1, col2, col3 = st.columns(3)

with col1:
    # Graphique 1: Nombre de tweets par granularité temporelle
    if time_granularity == "Jour" and 'date' in df.columns:
        fig_tweets = px.line(df, x='date', y='nombre_tweets_par_jour',
                             title='Nombre de Tweets par Jour', color_discrete_sequence=["#0083B8"])
    elif time_granularity == "Semaine":
        fig_tweets = px.bar(df, x='semaine', y='nombre_tweets_par_semaine',
                            title='Nombre de Tweets par Semaine', color_discrete_sequence=["#0083B8"])
    else:  # Mois
        fig_tweets = px.bar(df, x='mois', y='nombre_tweets_par_mois',
                            title='Nombre de Tweets par Mois', color_discrete_sequence=["#0083B8"])
    st.plotly_chart(fig_tweets, use_container_width=True)

with col2:
    # Graphique 2: Fréquence des mentions Engie par granularité temporelle
    if time_granularity == "Jour" and 'date' in df.columns:
        fig_mentions = px.line(df, x='date', y='nombre_mentions_engie',
                                title='Fréquence des Mentions Engie par Jour', color_discrete_sequence=["#E377C2"])
    elif time_granularity == "Semaine":
        fig_mentions = px.bar(df, x='semaine', y='nombre_mentions_engie',
                                title='Fréquence des Mentions Engie par Semaine', color_discrete_sequence=["#E377C2"])
    else:  # Mois
        fig_mentions = px.bar(df, x='mois', y='nombre_mentions_engie',
                                title='Fréquence des Mentions Engie par Mois', color_discrete_sequence=["#E377C2"])
    st.plotly_chart(fig_mentions, use_container_width=True)

with col3:
    # Graphique 3: Détection des tweets critiques par granularité temporelle
    if time_granularity == "Jour" and 'date' in df.columns:
        fig_critiques = px.line(df, x='date', y='nombre_tweets_critiques',
                                title='Détection des Tweets Critiques par Jour', color_discrete_sequence=["#FF7F0E"])
    elif time_granularity == "Semaine":
        fig_critiques = px.bar(df, x='semaine', y='nombre_tweets_critiques',
                                title='Détection des Tweets Critiques par Semaine', color_discrete_sequence=["#FF7F0E"])
    else:  # Mois
        fig_critiques = px.bar(df, x='mois', y='nombre_tweets_critiques',
                                title='Détection des Tweets Critiques par Mois', color_discrete_sequence=["#FF7F0E"])
    st.plotly_chart(fig_critiques, use_container_width=True)

# Afficher les données brutes (optionnel)
with st.expander("Afficher les Données Brutes"):
    st.dataframe(df)
