from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import json
import os
from datetime import datetime

# Inicialização do FastAPI
app = FastAPI()

# Modelo de sentimento em português
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="pysentimiento/bertweet-pt-sentiment"
)

# Arquivo onde os dados serão salvos
ARQUIVO_DADOS = "dados.json"

# Modelo de entrada
class TextoEntrada(BaseModel):
    texto: str

# Endpoint principal
@app.post("/sentimento")
def analisar_sentimento(entrada: TextoEntrada):

    # Executa a IA
    resultado = sentiment_analyzer(entrada.texto)[0]

    # Traduz LABEL para algo humano
    label = resultado["label"]
    if label == "NEG":
        sentimento = "NEGATIVO"
    elif label == "NEU":
        sentimento = "NEUTRO"
    else:
        sentimento = "POSITIVO"

    # Registro que será salvo
    registro = {
        "texto": entrada.texto,
        "sentimento": sentimento,
        "confianca": resultado["score"],
        "data_hora": datetime.now().isoformat()
    }

    # Lê o arquivo JSON existente
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = []

    # Adiciona o novo registro
    dados.append(registro)

    # Salva de volta no arquivo
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    # Retorna a resposta
    return registro