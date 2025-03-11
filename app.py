import streamlit as st
import pandas as pd
import plotly.express as px

# Définir le thème Streamlit
st.set_page_config(
    page_title="Dashboard KPIs - Twitter",
    page_icon=":bar_chart:",
    layout="wide",
)

# Ajouter un titre principal
st.title("Tableau de Bord Interactif des KPIs Twitter :chart_with_upwards_trend:")

# Charger les données
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, sep=';')
    return df

file_path = "./output/filtered_tweets_engie_final.csv"
df = load_data(file_path)

# Conversion des dates et gestion des colonnes
if 'created_at' in df.columns:
    df['date'] = pd.to_datetime(df['created_at'], errors='coerce').dt.date
if 'hour' in df.columns:
    df['hour'] = pd.to_numeric(df['hour'], errors='coerce').fillna(0)

# Sidebar pour les filtres
with st.sidebar:
    st.header("Filtres :wrench:")

    # Filtre de la granularité temporelle
    time_granularity = st.selectbox("Granularité Temporelle", ["Heure", "Jour", "Semaine", "Mois"])

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

# KPIs
kpi1, kpi2, kpi3 = st.columns(3)

# KPI 1: Nombre total de tweets
total_tweets = len(df)
kpi1.metric(
    label="Nombre Total de Tweets",
    value=f"{total_tweets:,}",
)

# KPI 2: Nombre de tweets critiques
total_critiques = df['contains_keywords'].sum()
kpi2.metric(
    label="Nombre Total de Tweets Critiques",
    value=f"{total_critiques:,}",
)

# KPI 3: Répartition des sentiments
positive_count = (df['sentiment'] == 'Positif').sum()
negative_count = (df['sentiment'] == 'Négatif').sum()
neutral_count = (df['sentiment'] == 'Neutre').sum()

kpi3.metric(
    label="Répartition des Sentiments",
    value=f"😀 {positive_count} | 😡 {negative_count} | 😐 {neutral_count}"
)

st.markdown("""---""")

# Graphiques
col1, col2 = st.columns(2)

with col1:
    # Graphique 1: Nombre de tweets par granularité temporelle
    if time_granularity == "Heure":
        fig_tweets = px.bar(df, x='hour', y='full_text',
                            title='Nombre de Tweets par Heure',
                            color_discrete_sequence=["#0083B8"])
    elif time_granularity == "Jour":
        fig_tweets = px.line(df, x='date', y='full_text',
                             title='Nombre de Tweets par Jour',
                             color_discrete_sequence=["#0083B8"])
    elif time_granularity == "Semaine":
        df['week'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%U')
        fig_tweets = px.bar(df, x='week', y='full_text',
                            title='Nombre de Tweets par Semaine',
                            color_discrete_sequence=["#0083B8"])
    else:  # Mois
        df['month'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m')
        fig_tweets = px.bar(df, x='month', y='full_text',
                            title='Nombre de Tweets par Mois',
                            color_discrete_sequence=["#0083B8"])
    st.plotly_chart(fig_tweets, use_container_width=True)

with col2:
    # Graphique 2: Nombre de tweets critiques
    if time_granularity == "Heure":
        fig_critiques = px.line(df, x='hour', y='contains_keywords',
                                title='Nombre de Tweets Critiques par Heure',
                                color_discrete_sequence=["#E377C2"])
    elif time_granularity == "Jour":
        fig_critiques = px.line(df, x='date', y='contains_keywords',
                                title='Nombre de Tweets Critiques par Jour',
                                color_discrete_sequence=["#E377C2"])
    elif time_granularity == "Semaine":
        fig_critiques = px.bar(df, x='week', y='contains_keywords',
                                title='Nombre de Tweets Critiques par Semaine',
                                color_discrete_sequence=["#E377C2"])
    else:  # Mois
        fig_critiques = px.bar(df, x='month', y='contains_keywords',
                                title='Nombre de Tweets Critiques par Mois',
                                color_discrete_sequence=["#E377C2"])
    st.plotly_chart(fig_critiques, use_container_width=True)

# Afficher les données brutes (optionnel)
with st.expander("Afficher les Données Brutes"):
    st.dataframe(df)
