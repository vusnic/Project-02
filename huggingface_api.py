import requests
import time

def get_huggingface_response(prompt):
    API_URL = "https://api-inference.huggingface.co/models/gpt2n"
    headers = {"Authorization": f"Bearer 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"}

    data = {
        "inputs": prompt,
        "parameters": {"max_length": 150},
    }

    max_retries = 5
    retries = 0

    while retries < max_retries:
        response = requests.post(API_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            return response_json[0]["generated_text"]
        elif response.status_code == 503:
            print("Serviço indisponível, tentando novamente em 10 segundos...")
            time.sleep(10)
            retries += 1
        else:
            response.raise_for_status()

    raise Exception(f"Falha após {max_retries} tentativas. Última resposta: {response.text}")

if __name__ == "__main__":
    prompt = "Olá, como posso ajudar você hoje?"
    response = get_huggingface_response(prompt)
    print(response)
