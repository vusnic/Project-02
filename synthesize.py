from gtts import gTTS
import os

def synthesize_text(text, output_file_path):
    tts = gTTS(text=text, lang='pt')
    tts.save(output_file_path)
    print(f"Áudio gerado e salvo em: {output_file_path}")

if __name__ == "__main__":
    text = "Olá,eu sou Renamon!, como posso ajudar você hoje?"
    output_file_path = "output.mp3"
    synthesize_text(text, output_file_path)
