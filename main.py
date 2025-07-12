import os
import time
import random
import threading
from telegram import __version__ as tg_ver
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes

# === Flask para manter Render ativo ===
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return f"✅ BacBo Bot v{tg_ver} está online com Python 3.13!"

# === Configuração ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # precisa ser int

HEADER = "💡 <b>BOT BACBO PROFISSIONAL</b> 💡"
DIV = "\n<b>------------------------------</b>\n"

# === Histórico fake ===
def obter_historico_fake():
    return [random.choice(["PLAYER", "BANKER", "TIE"]) for _ in range(20)]

# === Lógica do palpite ===
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

# === Envia palpite (versão async para Application) ===
async def enviar_palpite(context: ContextTypes.DEFAULT_TYPE):
    historico = obter_historico_fake()
    palpite, confianca = analisar_padroes(historico)

    mensagem = (
        f"{HEADER}{DIV}"
        f"📊 <b>Histórico:</b> {' | '.join(historico[-10:])}\n"
        f"🎯 <b>Palpite:</b> <u>{palpite}</u>\n"
        f"📈 <b>Confiança:</b> {confianca}%\n"
        f"🕒 <i>{time.strftime('%H:%M:%S')}</i>"
    )

    await context.bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode=ParseMode.HTML)

# === Inicialização do bot ===
async def start_bot():
    app_bot = Application.builder().token(TELEGRAM_TOKEN).build()
    job_queue = app_bot.job_queue
    job_queue.run_repeating(enviar_palpite, interval=240, first=5)
    await app_bot.run_polling()

# === Início ===
if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))).start()
    import asyncio
    asyncio.run(start_bot())
