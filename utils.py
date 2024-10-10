import pyttsx3
from textblob import TextBlob

# Inicializar síntese de voz
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Analisar emoções
def analyze_emotion(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "positivo"
    elif sentiment < 0:
        return "negativo"
    else:
        return "neutro"
