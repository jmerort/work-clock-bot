"""
Bot de Telegram para ayudarme a fichar.

@jmerort
Sept 2025
"""


from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime

global TOKEN
TOKEN = "7730281798:AAE3hC4PJkAQYKMCxUfGS7dVOjgm5nn7Z9o"

# Diccionario para guardar los tiempos de cada fichaje
times = {
    'trabajo_ini' : None,
    'trabajo_fin' : None,
    'comida_ini' : None,
    'comida_fin' : None,
}

async def trabajo_ini(update, context):
    chat_id = update.effective_chat.id
    # save current time as start time
    times['trabajo_ini'] = datetime.now()
    await update.message.reply_text(
        f"Inicio de trabajo: {times['trabajo_ini'].strftime('%H:%M')}"
    )


async def comida_ini(update, context):
    chat_id = update.effective_chat.id
    # save current time as start time
    times['comida_ini'] = datetime.now()
    await update.message.reply_text(
        f"Inicio de trabajo: {times['comida_ini'].strftime('%H:%M')}"
    )


async def comida_fin(update, context):
    chat_id = update.effective_chat.id
    # save current time as start time
    times['comida_fin'] = datetime.now()
    await update.message.reply_text(
        f"Inicio de trabajo: {times['comida_fin'].strftime('%H:%M')}"
    )


async def trabajo_fin(update, context):
    if times['trabajo_ini'] == None:
        # no start time stored for this chat
        await update.message.reply_text("No se ha comenzado el trabajo.")
        return
    
    end_time = datetime.now()
    start_time = times['trabajo_ini'] # remove after use
    
    # convert to total minutes
    duration = end_time - start_time

    total_minutes = int(duration.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    await update.message.reply_text(
        f"Fin del trabajo: {end_time.strftime('%H:%M')}\n"
        f"Duración: {hours} h y {minutes} min."
    )

    for t in times.keys():
        times[t] = None



def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # command handlers
    app.add_handler(CommandHandler("trabajo_ini", trabajo_ini))
    app.add_handler(CommandHandler("comida_ini", comida_ini))
    app.add_handler(CommandHandler("comida_fin", comida_fin))
    app.add_handler(CommandHandler("trabajo_fin", trabajo_fin))

    app.run_polling()

if __name__ == "__main__":
    main()