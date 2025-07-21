# 🤖 Agente LLM com Ferramentas Customizadas (via OpenAI API)

Este é um projeto de demonstração de um agente LLM (como o GPT-4o) que interage com o usuário via terminal e utiliza **ferramentas (tools/functions)** customizadas, como soma de números ou acesso a dados. Construído com Python e a API da OpenAI.

---

## 🚀 Funcionalidades

- Interação via terminal com o agente LLM
- Capacidade de chamar funções Python internas quando o modelo "decide"
- Estrutura pronta para expandir com novas ferramentas
- Uso da API da OpenAI com suporte à função de `tool_calls`

---

## 📦 Requisitos

- Python 3.8+
- Conta na [OpenAI](https://platform.openai.com/)
- Chave de API da OpenAI (`OPENAI_API_KEY`)

---

## 🛠️ Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/agente-llm-multitools.git
cd agente-llm-multitools
```

2. (Opcional) Crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # no macOS/Linux
.venv\Scripts\activate     # no Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

🔐 Configuração
Crie um arquivo .env na raiz do projeto com sua chave da OpenAI:

```bash
OPENAI_API_KEY=sua-chave-aqui
```

🧪 Como usar
Execute o agente via terminal:

```bash
python agent.py
```

Digite mensagens como:

```bash
Você: some 4 e 5
Agente: A soma de 4 e 5 é 9.
```

🧠 Estrutura Interna
agent.py: Código principal que define o agente LLM.
Funções Python são registradas como tools e o modelo pode chamá-las.
A resposta do modelo é interceptada quando ele tenta usar uma ferramenta (tool_calls), e o resultado é retornado ao usuário.

✨ Exemplo de Tool Implementada

```bash
def adiciona(a: int, b: int) -> int:
    """Soma dois números inteiros."""
    return a + b
```

📌 Licença
Este projeto é livre para uso e modificação, sem garantias.

🧙‍♀️ Feito por @jessicaDSL – seguindo aprendizado prático de como construir agentes LLM com ferramentas reais 💡
