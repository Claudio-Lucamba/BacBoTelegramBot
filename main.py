import os
import time
import random
from telegram import Bot

# === CONFIGURAÇÃO INICIAL ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

# === DESIGN ===
HEADER = "💡 <b>BOT BACBO PROFISSIONAL</b> 💡"
DIV = "\n<b>------------------------------</b>\n"

# === SIMULAÇÃO DE HISTÓRICO ===
# Pode ser substituído por scraping real se acesso direto estiver disponível
def obter_historico_fake():
    opcoes = ["PLAYER", "BANKER", "TIE"]
    historico = [random.choice(opcoes) for _ in range(20)]
    return historico

# === LÓGICA DE ANÁLISE ===
def analisar_padroes(historico):
    player = historico.count("PLAYER")
    banker = historico.count("BANKER")
    tie = historico.count("TIE")

    total = len(historico)
    pct_player = player / total * 100
    pct_banker = banker / total * 100
    pct_tie = tie / total * 100

    if pct_player > 55:
        return "PLAYER", round(pct_player)
    elif pct_banker > 55:
        return "BANKER", round(pct_banker)
    elif pct_tie > 15:
        return "TIE", round(pct_tie)
    else:
        return random.choice([("PLAYER", 60), ("BANKER", 60)])

# === ENVIO PARA O TELEGRAM ===
def enviar_palpite():
    historico = obter_historico_fake()
    palpite, confianca = analisar_padroes(historico)

    mensagem = (
        f"{HEADER}{DIV}"
        f"📊 <b>Histórico:</b> {' | '.join(historico[-10:])}\n"
        f"📈 <b>Palpite:</b> <u>{palpite}</u>\n"
        f"⏳ <b>Confiança:</b> {confianca}%\n"
        f"🕒 <i>{time.strftime('%H:%M:%S')}</i>"
    )

    bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode="HTML")

# === LOOP PRINCIPAL ===
def main():
    while True:
        enviar_palpite()
        time.sleep(60)  # Espera 1 minuto

if __name__ == "__main__":
    main()
