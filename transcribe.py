import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

def transcribe_from_microphone(model_path):
    print(f"Verificando a existência do modelo no caminho: {model_path}")
    if not os.path.exists(model_path):
        print(f"Modelo não encontrado no caminho: {model_path}")
        exit(1)

    print("Carregando o modelo...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    print("Inicializando PyAudio...")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4096)
    stream.start_stream()

    print("Fale algo...")

    results = []
    try:
        while True:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                print("Áudio reconhecido.")
                results.append(json.loads(recognizer.Result()))
                break
            else:
                partial_result = recognizer.PartialResult()
                print(partial_result)
                
    except Exception as e:
        print(f"Erro durante a transcrição: {e}")

    final_result = json.loads(recognizer.FinalResult())
    results.append(final_result)
    text = ' '.join([res.get('text', '') for res in results])
    print("Transcrição final: {}".format(text))

    stream.stop_stream()
    stream.close()
    p.terminate()

    return text

if __name__ == "__main__":
    model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model'))
    print(f"Usando o modelo no caminho: {model_path}")
    transcribe_from_microphone(model_path)
