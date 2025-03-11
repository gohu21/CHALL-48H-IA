from textblob import TextBlob

def get_sentiment(text):
#Analyse le sentiment d'un texte avec TextBlob.
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positif'
    elif analysis.sentiment.polarity < 0:
        return 'Négatif'
    else:
        return 'Neutre'
