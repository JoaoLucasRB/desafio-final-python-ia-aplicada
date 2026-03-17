import json
from openai import OpenAI

client_openai = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

def get_text_content():
    lines = []
    with open("resenhas.txt", "r") as file:
        for line in file:
            lines.append(line)
    return "".join(lines)

def get_reviews_list(text_content):
    response = client_openai.chat.completions.create(
        model="google/gemma-3n-e4b",
        messages=[
            {
                "role": "system",
                "content": """
                    Você é um especialista em análise de dados e conversão de dados para JSON.
                    Você receberá várias linhas de texto onde cada uma é uma resenha de um aplicativo em um marketplace online.
                    Eu quero que você analise essa resenha, traduza ela para PT-BR e me retorne uma lista de JSONs com as seguintes chaves:
                    - "usuario": o nome do usuário que fez a resenha
                    - "resenha_original": o texto original da resenha
                    - "resenha_pt": o texto da resenha traduzido para o português brasileiro
                    - "avaliacao": a avaliação da resenha, que pode ser "Positiva", "Negativa" ou "Neutra" (Apenas uma dessas opções)

                    Exemplo de entrada:
                    879485937$Pedro Pascal$This is a very good app, but the new update is a bit bad.
                    
                    Exemplo de saída:
                    [
                        {"usuario": "Pedro Pascal", 
                        "resenha_original": "This is a very good app, but the new update is a bit bad.", 
                        "resenha_pt": "Este é um aplicativo muito bom, mas a nova atualização está um pouco ruim.", "avaliacao": "Neutra"}
                    ]

                    Regra Importante:
                    Você deve retornar apenas a lista de JSON, sem nenhum texto além do JSON.
                """
            },
            {
                "role": "user", "content": f"""
                    Esses são os textos que quero que seja avaliado:
                    {get_text_content()}
                """
            }
        ],
        temperature=1.0
    )

    return json.loads(response.choices[0].message.content.replace("```json\n", "").replace("\n```", ""))

def treat_review_data(reviews_list):
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    reviews_list_str = []

    for review in reviews_list:
        match review["avaliacao"]:
            case "Positiva":
                positive_count += 1
            case "Negativa":
                negative_count += 1
            case "Neutra":
                neutral_count += 1
        reviews_list_str.append(str(review))
    
    return {
        "qtd_positivas": positive_count,
        "qtd_negativas": negative_count,
        "qtd_neutras": neutral_count,
        "textos_unidos": reviews_list_str
    }

review_data = treat_review_data(get_reviews_list(get_text_content()))

print(f"Positivas: {review_data["qtd_positivas"]}")
print(f"Negativas: {review_data["qtd_negativas"]}")
print(f"Neutras: {review_data["qtd_neutras"]}")
print(f"Todas as Avaliações: {review_data["textos_unidos"]}")