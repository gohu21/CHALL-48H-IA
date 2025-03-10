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
    tweets_par_jour = df.groupby('date').size().reset_index(name='nombre_tweets_par_jour')
    df = df.merge(tweets_par_jour, on='date', how='left')

    df['semaine'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%U')
    tweets_par_semaine = df.groupby('semaine').size().reset_index(name='nombre_tweets_par_semaine')
    df = df.merge(tweets_par_semaine, on='semaine', how='left')

    df['mois'] = pd.to_datetime(df['created_at']).dt.to_period('M')
    tweets_par_mois = df.groupby('mois').size().reset_index(name='nombre_tweets_par_mois')
    df = df.merge(tweets_par_mois, on='mois', how='left')

    df['mentions_engie'] = df['full_text'].str.contains('engie', case=False, na=False)
    df['tweets_critiques'] = df['presence_mots_cles_critiques'].astype(int)
    df['tweets_mots_cles'] = df['presence_mots_cles'].astype(int)

    df['heure'] = pd.to_datetime(df['created_at']).dt.hour
    tweets_par_heure = df.groupby('heure').size().reset_index(name='nombre_tweets_par_heure')
    df = df.merge(tweets_par_heure, on='heure', how='left')

    return df
