import requests
import json
import os
import time

# Defina sua chave da API diretamente aqui
OPENAI_API_KEY = "Coloca sua chave aqui"

# Função para carregar o cache de respostas
def load_cache():
    if os.path.exists("response_cache.json"):
        with open("response_cache.json", "r") as f:
            return json.load(f)
    return {}

# Função para salvar o cache de respostas
def save_cache(cache):
    with open("response_cache.json", "w") as f:
        json.dump(cache, f)

# Função para obter a resposta da API do ChatGPT com cache
def get_chatgpt_response(prompt):
    api_key = OPENAI_API_KEY
    if api_key is None:
        raise ValueError("A chave de API não está definida. Por favor, defina a chave da API.")
    
    cache = load_cache()
    if prompt in cache:
        print("Usando resposta em cache.")
        return cache[prompt]
    
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }

    max_retries = 5
    retries = 0
    wait_time = 30

    while retries < max_retries:
        print(f"Enviando solicitação ao ChatGPT com prompt: {prompt}")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            response_text = response_json['choices'][0]['message']['content'].strip()
            cache[prompt] = response_text
            save_cache(cache)
            print(f"Resposta recebida do ChatGPT: {response_json}")
            return response_text
        elif response.status_code == 429:
            print("Limite de taxa atingido, tentando novamente em 30 segundos...")
            time.sleep(wait_time)
            retries += 1
            wait_time *= 2  # Exponencialmente aumentar o tempo de espera
        else:
            print(f"Erro na API do ChatGPT: {response.status_code}, {response.text}")
            response.raise_for_status()

    raise Exception(f"Falha após {max_retries} tentativas. Última resposta: {response.text}")

if __name__ == "__main__":
    prompt = "Olá, como posso ajudar você hoje?"
    response = get_chatgpt_response(prompt)
    print(response)
