import requests

URL = "http://127.0.0.1:8000/sentimento"

print("Digite um texto para analisar sentimento")
texto = input("> ")

resposta = requests.post(
    URL,
    json={"texto": texto}
)

if resposta.status_code == 200:
    dados = resposta.json()
    print("\nResultado da IA:")
    print("----------------")
    print("Texto:", dados["texto"])
    print("Sentimento:", dados["sentimento"])
    print("Confiança:", round(dados["confianca"], 2))
    print("Data/Hora:", dados["data_hora"])
else:
    print("Erro ao chamar o microserviço")
