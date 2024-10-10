import tkinter as tk
from tkinter import ttk
from threading import Thread
from transcribe import transcribe_from_microphone
from chatgpt_api import get_chatgpt_response
from synthesize import synthesize_text
from pygame import mixer
import os
import time
import random

class AudioVisualizer(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.width = kwargs.get('width', 600)
        self.height = kwargs.get('height', 100)
        self.create_line(0, self.height//2, self.width, self.height//2, fill="green", tags="line")
        self.running = False

    def start(self):
        self.running = True
        self.animate()

    def stop(self):
        self.running = False

    def animate(self):
        if self.running:
            self.delete("line")
            self.create_line(0, self.height//2, self.width, self.height//2, fill="green", tags="line")
            for i in range(0, self.width, 10):
                height = random.randint(0, self.height)
                self.create_line(i, self.height//2, i, self.height//2 - height//2, fill="green", tags="line")
            self.after(100, self.animate)

class VoiceAssistantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assistente de Voz")
        self.geometry("600x500")
        
        # Título
        self.label_title = tk.Label(self, text="Assistente de Voz", font=("Helvetica", 18, "bold"))
        self.label_title.pack(pady=20)

        # Status
        self.label_status = tk.Label(self, text="Status: Inativo", font=("Helvetica", 14))
        self.label_status.pack(pady=10)

        # Visualizador de Áudio
        self.visualizer = AudioVisualizer(self, width=600, height=100)
        self.visualizer.pack(pady=10)

        # Transcrição
        self.label_transcript_title = tk.Label(self, text="Transcrição:", font=("Helvetica", 14, "bold"))
        self.label_transcript_title.pack(pady=10)
        self.text_transcript = tk.Text(self, height=5, width=50, font=("Helvetica", 12))
        self.text_transcript.pack(pady=5)

        # Resposta
        self.label_response_title = tk.Label(self, text="Resposta:", font=("Helvetica", 14, "bold"))
        self.label_response_title.pack(pady=10)
        self.text_response = tk.Text(self, height=5, width=50, font=("Helvetica", 12))
        self.text_response.pack(pady=5)

        # Botão Iniciar
        self.btn_start = tk.Button(self, text="Iniciar", command=self.start_listening, font=("Helvetica", 12))
        self.btn_start.pack(pady=10)
        
        # Botão Sair
        self.btn_exit = tk.Button(self, text="Sair", command=self.quit, font=("Helvetica", 12))
        self.btn_exit.pack(pady=10)
        
        self.model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'model'))
        self.output_files_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output_files'))
        if not os.path.exists(self.output_files_path):
            os.makedirs(self.output_files_path)
        print(f"Path do modelo no __init__: {self.model_path}")
        print(f"Path do output_files no __init__: {self.output_files_path}")

    def start_listening(self):
        self.label_status.config(text="Status: Escutando...")
        self.update()
        
        self.visualizer.start()  # Inicia a visualização de áudio

        thread = Thread(target=self.process_audio)
        thread.start()

    def process_audio(self):
        try:
            print(f"Path do modelo no process_audio: {self.model_path}")
            transcript = transcribe_from_microphone(self.model_path)
            self.text_transcript.delete(1.0, tk.END)
            self.text_transcript.insert(tk.END, transcript)
            self.label_status.config(text="Status: Processando...")
            self.update()

            response_text = get_chatgpt_response(transcript)
            self.text_response.delete(1.0, tk.END)
            self.text_response.insert(tk.END, response_text)
            self.label_status.config(text="Status: Gerando Áudio...")
            self.update()

            output_audio_file_path = os.path.join(self.output_files_path, 'output.mp3')
            synthesize_text(response_text, output_audio_file_path)
            
            self.visualizer.stop()  # Para a visualização de áudio

            self.play_audio(output_audio_file_path)
        except Exception as e:
            self.label_status.config(text=f"Erro: {str(e)}")
            print(f"Erro: {str(e)}")

    def play_audio(self, file_path):
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()
        self.visualizer.start()  # Inicia a visualização de áudio para a resposta
        while mixer.music.get_busy():
            time.sleep(1)
        self.visualizer.stop()  # Para a visualização de áudio
        self.label_status.config(text="Status: Inativo")

if __name__ == "__main__":
    app = VoiceAssistantApp()
    app.mainloop()
