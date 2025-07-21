from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Funções (tools)
def adiciona(a: int, b: int) -> int:
    return a + b

def subtrai(a: int, b: int) -> int:
    return a - b

def multiplica(a: int, b: int) -> int:
    return a * b

def info_curiosa() -> str:
    return "Sabia que polvos têm três corações?"

def consulta_usuario(nome: str) -> str:
    base_usuarios = {
        "Alice": "Alice tem 22 anos, é uma engenheira de software, mora em São Paulo.",
        "Bob": "Bob tem 30 anos, é um designer gráfico, mora no Rio de Janeiro.",
        "Charlie": "Charlie tem 25 anos, é um analista de dados, mora em Belo Horizonte."
    }
    return base_usuarios.get(nome, "Usuário não encontrado.")

def consulta_pokemon(nome: str) -> str:
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
      return "Pokémon não encontrado."
    dados = response.json()
    tipos = [tipo['type']['name'] for tipo in dados['types']]
    altura = dados['height'] / 10  # Convertendo para metros
    peso = dados['weight'] / 10  # Convertendo para kg
    habilidades = [h['ability']['name'] for h in dados['abilities']]
    
    return f"{dados['name']} é um Pokémon do tipo {tipos[0]}, tem {altura}m de altura, {peso}kg e as habilidades: {', '.join(habilidades)}."

def compara_pokemons(nome1: str, nome2: str) -> str:
    pokemon1 = consulta_pokemon(nome1)
    pokemon2 = consulta_pokemon(nome2)
    
    if "Pokémon não encontrado" in pokemon1 or "Pokémon não encontrado" in pokemon2:
        return "Um ou ambos os Pokémon não foram encontrados."
    
    return f"Comparação entre {nome1} e {nome2}:\n{pokemon1}\n{pokemon2}"

tools = {
    "adiciona": adiciona,
    "subtrai": subtrai,
    "diminui": subtrai,
    "consulta_usuario": consulta_usuario,
    "multiplica": multiplica,
    "info_curiosa": info_curiosa,
    "consulta_pokemon": consulta_pokemon,
    "compara_pokemons": compara_pokemons
}

funcoes = [
    {
        "type": "function",
        "function": {
            "name": "adiciona",
            "description": "Soma dois números inteiros.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtrai",
            "description": "Subtrai dois números inteiros.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consulta_usuario",
            "description": "Consulta informações sobre um usuário pelo nome.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"}
                },
                "required": ["nome"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiplica",
            "description": "Multiplica dois números inteiros.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "info_curiosa",
            "description": "Retorna uma curiosidade aleatória.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consulta_pokemon",
            "description": "Consulta informações sobre um Pokémon pelo nome.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "description": "Nome do Pokémon"}
                },
                "required": ["nome"]
            }
        }
    },
    {
      "type": "function",
      "function": {
        "name": "compara_pokemons",
        "description": "Compara dois Pokémons e retorna uma análise das diferenças e semelhanças.",
        "parameters": {
          "type": "object",
          "properties": {
            "nome1": {"type": "string", "description": "Nome do primeiro Pokémon"},
            "nome2": {"type": "string", "description": "Nome do segundo Pokémon"}
          },
          "required": ["nome1", "nome2"]
        }
      }
    }
]

def agente_conversa(mensagem_usuario):
    mensagens = [
        {"role": "system", "content": "Você é um assistente inteligente que responde sempre em português do Brasil e pode usar ferramentas quando necessário."},
        {"role": "user", "content": mensagem_usuario}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=mensagens,
        tools=funcoes,  # type: ignore
        tool_choice="auto"
    )

    resposta = response.choices[0]

    print(f"DEBUG: Resposta inicial do modelo: {resposta.message}")

    if resposta.finish_reason == "tool_calls":
        chamada = resposta.message.tool_calls[0]  # type: ignore
        nome = chamada.function.name
        argumentos = json.loads(chamada.function.arguments)
        print(f"Chamando a função: {nome} com argumentos: {argumentos}")
        resultado = tools[nome](**argumentos)

        mensagens.append(resposta.message)
        mensagens.append({
            "role": "tool",
            "tool_call_id": chamada.id,
            "name": nome,
            "content": str(resultado)
        })

        resposta_final = client.chat.completions.create(
            model="gpt-4o",
            messages=mensagens
        )
        msg_final = resposta_final.choices[0].message
        return msg_final.content

    return resposta.message.content

if __name__ == "__main__":
    while True:
        entrada = input("Você: ")
        resposta = agente_conversa(entrada)
        print(f"Agente: {resposta}")
