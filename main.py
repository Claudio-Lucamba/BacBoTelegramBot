import os
import time
import requests
import random

# Pega as variáveis de ambiente do Render (ou usa padrão se testar localmente)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7958380213:AAFUw7jGywERwxvd-iOAV7MlFgD_aDV574Q")
CHAT_ID = os.getenv("CHAT_ID", "6105692781")

# Simulador simples de previsão de Bac Bo (você pode melhorar depois com lógica real)
def prever_resultado():
    jogador = random.randint(2, 12)
    banca = random.randint(2, 12)
    if jogador > banca:
        dica = "PLAYER"
    elif banca > jogador:
        dica = "BANKER"
    else:
        dica = "EMPATE"
    confianca = random.randint(85, 95)
    return jogador, banca, dica, confianca

# Envia mensagem para Telegram
def enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem}
    requests.post(url, data=payload)

# Mensagem de início
enviar_mensagem("🤖 Bot BacBo ativado com sucesso!")

# Loop contínuo
while True:
    jogador, banca, dica, confianca = prever_resultado()
    msg = f"🎲 Nova rodada:\nPLAYER: {jogador} | BANKER: {banca}\n✨ Sugestão: {dica}\n📈 Confiança: {confianca}%"
    enviar_mensagem(msg)
    time.sleep(20)
