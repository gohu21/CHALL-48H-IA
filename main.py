from src.data_loader import load_data, save_data
from src.data_cleaning import clean_data
from src.text_cleaning import clean_text
from src.sentiment_analysis import get_sentiment
from src.kpi_extraction import prepare_date_features, extract_kpi

# 🔹 Étape 1 : Chargement des données brutes
file_path = "Data/filtered_tweets_engie.csv"
data = load_data(file_path)

# 🔹 Étape 2 : Nettoyage des données
data = clean_data(data)

# 🔹 Étape 3 : Nettoyage du texte et analyse de sentiment
data['full_text'] = data['full_text'].apply(clean_text)
data['sentiment'] = data['full_text'].apply(get_sentiment)

# 🔹 Étape 4 : Extraction des KPI
data = prepare_date_features(data)
kpi_results = extract_kpi(data)

# 🔹 Étape 5 : Sauvegarde du fichier final
output_path = "CHALL-48H-IA/output/filtered_tweets_engie_final.csv"
save_data(data, output_path)

# 🔹 Étape 6 : Affichage des KPI
print(f"✅ Données nettoyées et enregistrées dans : `{output_path}`")
print(f"📊 Nombre total de tweets : {kpi_results['total_tweets']}")
print(f"📅 Tweets par jour :\n{kpi_results['tweets_per_day']}")
print(f"📅 Tweets par semaine :\n{kpi_results['tweets_per_week']}")
print(f"📅 Tweets par mois :\n{kpi_results['tweets_per_month']}")
print(f"🕒 Répartition par heure :\n{kpi_results['tweets_per_hour']}")
print(f"📅 Répartition par jour de la semaine :\n{kpi_results['tweets_per_day_of_week']}")
print(f"⚠️ Nombre de tweets critiques : {kpi_results['critical_tweets']}")
print(f"😰 Score d'inconfort : {kpi_results['discomfort_score']}%")
