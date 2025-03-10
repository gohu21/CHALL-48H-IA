import re
import pandas as pd


def nettoyer_texte_sauf_liens(texte):
    liens = re.findall(r'https?://\S+', texte)
    for i, lien in enumerate(liens):
        texte = texte.replace(lien, f'__LIEN_{i}__')
    texte = re.sub(r'\\[nt]', ' ', texte)
    texte = re.sub(r'\s([.,;:])', r'\1', texte)
    texte = texte.replace('\n', ' ').replace('\r', ' ')
    texte = re.sub(r'([!?])(?![!?])', r'\1 ', texte)
    texte = re.sub(r' +', ' ', texte)
    for i, lien in enumerate(liens):
        texte = texte.replace(f'__LIEN_{i}__', lien)
    return texte


def nettoyer_date(df):
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)
    df = df.dropna(subset=['created_at'])
    df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df


def nettoyer_identifiants(df):
    df['tweet_id'] = df['id'].astype(str).str.replace(r'\.0$', '', regex=True)
    df['tweet_id'] = df['tweet_id'].astype(str)
    return df


def extraire_informations(df):
    df['heure'] = pd.to_datetime(df['created_at']).dt.hour
    df['longueur_texte'] = df['full_text'].str.len()
    return df


def ajouter_mots(df, colonne, mots_cles):
    pattern = '|'.join(mots_cles)
    df[colonne] = df['full_text'].str.lower().str.contains(pattern, na=False)
    return df


def calculer_kpis(df):
    df['date'] = pd.to_datetime(df['created_at']).dt.date
    df['semaine'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%U')
    df['mois'] = pd.to_datetime(df['created_at']).dt.to_period('M')
    df['heure'] = pd.to_datetime(df['created_at']).dt.hour

    # Initialisation colonnes critiques et mentions
    df['mentions_engie'] = df['full_text'].str.contains('engie', case=False, na=False).astype(int)
    df['tweets_critiques'] = df['presence_mots_cles_critiques'].astype(int)

    ### KPIs Journaliers ###
    kpi_jour = df.groupby('date').agg(
        nombre_tweets_par_jour=('tweet_id', 'count'),
        nombre_mentions_engie=('mentions_engie', 'sum'),
        nombre_tweets_critiques=('tweets_critiques', 'sum'),
        auteurs_uniques=('screen_name', 'nunique')
    ).reset_index()
    kpi_jour['%_tweets_critiques'] = (kpi_jour['nombre_tweets_critiques'] / kpi_jour['nombre_tweets_par_jour'] * 100).round(2)
    kpi_jour['%_mentions_engie'] = (kpi_jour['nombre_mentions_engie'] / kpi_jour['nombre_tweets_par_jour'] * 100).round(2)

    ### KPIs Hebdomadaires ###
    kpi_semaine = df.groupby('semaine').agg(
        nombre_tweets_par_semaine=('tweet_id', 'count'),
        nombre_mentions_engie=('mentions_engie', 'sum'),
        nombre_tweets_critiques=('tweets_critiques', 'sum'),
        auteurs_uniques=('screen_name', 'nunique')
    ).reset_index()
    kpi_semaine['%_tweets_critiques'] = (kpi_semaine['nombre_tweets_critiques'] / kpi_semaine['nombre_tweets_par_semaine'] * 100).round(2)
    kpi_semaine['%_mentions_engie'] = (kpi_semaine['nombre_mentions_engie'] / kpi_semaine['nombre_tweets_par_semaine'] * 100).round(2)

    ### KPIs Mensuels ###
    kpi_mois = df.groupby('mois').agg(
        nombre_tweets_par_mois=('tweet_id', 'count'),
        nombre_mentions_engie=('mentions_engie', 'sum'),
        nombre_tweets_critiques=('tweets_critiques', 'sum'),
        auteurs_uniques=('screen_name', 'nunique')
    ).reset_index()
    kpi_mois['%_tweets_critiques'] = (kpi_mois['nombre_tweets_critiques'] / kpi_mois['nombre_tweets_par_mois'] * 100).round(2)
    kpi_mois['%_mentions_engie'] = (kpi_mois['nombre_mentions_engie'] / kpi_mois['nombre_tweets_par_mois'] * 100).round(2)

    ### KPIs Horaires ###
    kpi_heure = df.groupby('heure').agg(
        nombre_tweets_par_heure=('tweet_id', 'count'),
        nombre_mentions_engie=('mentions_engie', 'sum'),
        nombre_tweets_critiques=('tweets_critiques', 'sum')
    ).reset_index()

    # Fusionner KPIs pour usage global
    df = df.merge(kpi_jour[['date', 'nombre_tweets_par_jour', 'nombre_mentions_engie', 'nombre_tweets_critiques']], on='date', how='left')
    df = df.merge(kpi_semaine[['semaine', 'nombre_tweets_par_semaine']], on='semaine', how='left')
    df = df.merge(kpi_mois[['mois', 'nombre_tweets_par_mois']], on='mois', how='left')
    df = df.merge(kpi_heure[['heure', 'nombre_tweets_par_heure']], on='heure', how='left')

    return df, kpi_jour, kpi_semaine, kpi_mois, kpi_heure
