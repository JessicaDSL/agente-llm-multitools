from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def adiciona(a: int, b: int) -> int:
  return a + b

def subtrai(a: int, b: int) -> int:
  return a - b

def consulta_usuario(nome: str) -> str:
  base_usuarios = {
    "Alice": "Alice tem 22 anos, é uma engenheira de software, mora em São Paulo.",
    "Bob": "Bob tem 30 anos, é um designer gráfico, mora no Rio de Janeiro.",
    "Charlie": "Charlie tem 25 anos, é um analista de dados, mora em Belo Horizonte."
  }
  return base_usuarios.get(nome, "Usuário não encontrado.")

tools = {
  "adiciona": adiciona,
  "subtrai": subtrai,
  "diminui": subtrai,
  "consulta_usuario": consulta_usuario
}

def agente_conversa(mensagem_usuario):
  mensagens = [
    {"role": "system", "content": "Você é um assistente inteligente que responde sempre em português do Brasil e pode usar ferramentas quando necessário."},
    {"role": "user", "content": mensagem_usuario}
  ]
  
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
    }
    ]
  print(f"Mensagens enviadas: {mensagens}")

  response = client.chat.completions.create(
    model="gpt-4o",
    messages=mensagens,
    tools=funcoes, # type: ignore
    tool_choice="auto",
  )
  
  resposta = response.choices[0]
  
  print(f"DEBUG: Resposta inicial do GPT: {resposta.message}")
  
  # print(f"Resposta: {resposta}")
  
  if resposta.finish_reason == "tool_calls":
    print("O modelo pediu para chamar uma ferramenta.")
    chamada = resposta.message.tool_calls[0] # type: ignore
    nome = chamada.function.name
    print(f"Nome da função que o modelo pediu: {nome}")
    argumentos = json.loads(chamada.function.arguments)
    print(f"Argumentos recebidos: {argumentos}")
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
    return resposta_final.choices[0].message.content
    print(f"Resposta final do modelo: {resposta_final_texto}")
  
  print("Modelo respondeu diretamente, sem usar ferramenta.")
  return resposta.message.content

if __name__ == "__main__":
  while True:
    entrada = input("Você: ")
    resposta = agente_conversa(entrada)
    print(f"Agente: {resposta}")
      
  