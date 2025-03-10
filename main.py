import pandas as pd
import re
import os

output_dir = './output'
mots_cles = ['énergie', 'transition', 'engie']
mots_cles_critiques = ['délai', 'panne', 'urgence', 'scandale']

def charger_fichier_csv(fichier):
    print("[INFO] Chargement du fichier CSV...")
    return pd.read_csv(fichier, encoding='utf-8', sep=';')

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
    print("[INFO] Nettoyage de la date...")
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)
    df = df.dropna(subset=['created_at'])
    df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

def nettoyer_identifiants(df):
    print("[INFO] Nettoyage des identifiants...")
    df['tweet_id'] = df['id'].astype(str).str.replace(r'\.0$', '', regex=True)
    df['tweet_id'] = df['tweet_id'].astype(str)
    return df

def extraire_informations(df):
    print("[INFO] Extraction des informations...")
    df['heure'] = pd.to_datetime(df['created_at']).dt.hour
    df['longueur_texte'] = df['full_text'].str.len()
    return df

def add_word(df, colonne, mots_cles):
    pattern = '|'.join(mots_cles)
    df[colonne] = df['full_text'].str.lower().str.contains(pattern, na=False)
    return df

def sauvegarder_fichier(df, fichier_csv, fichier_json):
    print("[INFO] Sauvegarde des fichiers nettoyés...")

    df.to_csv(fichier_csv, index=False, encoding='utf-8')
    print(f"[SUCCESS] Fichier CSV '{fichier_csv}' sauvegardé avec succès.")

    df.to_json(fichier_json, orient='records', force_ascii=False, indent=4)
    print(f"[SUCCESS] Fichier JSON '{fichier_json}' sauvegardé avec succès.")

def nettoyer_et_traiter(fichier_entree, fichier_csv_sortie, fichier_json_sortie, mots_cles, mots_cles_critiques):
    df = charger_fichier_csv(fichier_entree)

    print("[INFO] Nettoyage du texte...")
    df['full_text'] = df['full_text'].apply(nettoyer_texte_sauf_liens)

    df = nettoyer_date(df)
    df = nettoyer_identifiants(df)
    df = extraire_informations(df)
    df = add_word(df, 'presence_mots_cles', mots_cles)
    df = add_word(df, 'presence_mots_cles_critiques', mots_cles_critiques)

    sauvegarder_fichier(df, fichier_csv_sortie, fichier_json_sortie)

os.makedirs(output_dir, exist_ok=True)

fichier_csv_sortie = os.path.join(output_dir, 'filtered_tweets_engie_cleaned.csv')
fichier_json_sortie = os.path.join(output_dir, 'filtered_tweets_engie_cleaned.json')

nettoyer_et_traiter(
    'filtered_tweets_engie.csv',
    fichier_csv_sortie,
    fichier_json_sortie,
    mots_cles,
    mots_cles_critiques
)
