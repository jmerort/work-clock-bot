"""
Work Clock bot launch client 

@jmerort
Sep 2025
"""

from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime

from data.credentials import bot_token

global TOKEN
TOKEN = bot_token # Stored in local .py file

global working, eating

working = False
eating = False

# Dictionary to store the four clock times
times = {
    'begin' : None,
    'lunch_begin' : None,
    'lunch_end' : None,
    'end' : None,
}

async def trabajo_ini(update, context):
    # Comprobar si el usuario ya fichó
    if times['trabajo_ini'] != None:
        await update.message.reply_text(f"Ya fichaste a las {times['trabajo_ini'].strftime('%H:%M')}.")
        return
    
    # Guardar la hora en memoria y sacarla por pantalla
    times['trabajo_ini'] = datetime.now()
    await update.message.reply_text(
        f"Inicio de trabajo: {times['trabajo_ini'].strftime('%H:%M')}"
    )


async def comida_ini(update, context):
    
    # save current time as start time
    times['comida_ini'] = datetime.now()
    await update.message.reply_text(
        f"Inicio de comida: {times['comida_ini'].strftime('%H:%M')}"
    )


async def comida_fin(update, context):
    chat_id = update.effective_chat.id
    # save current time as start time
    times['comida_fin'] = datetime.now()
    await update.message.reply_text(
        f"Fin de comida: {times['comida_fin'].strftime('%H:%M')}"
    )


async def trabajo_fin(update, context):
    if times['trabajo_ini'] == None:
        # no start time stored for this chat
        await update.message.reply_text("No se ha comenzado el trabajo.")
        return
    
    end_time = datetime.now()
    await update.message.reply_text(
        f"Fin del trabajo: {end_time.strftime('%H:%M')}\n",
    )

    for t in times.keys():
        times[t] = None

def diferencia_tiempos(hora_ini, hora_fin):
    """
    Devuelve la diferencia de tiempos entre dos horas, en horas y minutos
    """
    # convert to total minutes
    duration = hora_ini - hora_fin

    total_minutes = int(duration.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    return hours, minutes



def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Set working and eating flags to False
    working = False
    eating = False

    # command handlers
    app.add_handler(CommandHandler("begin", begin))
    app.add_handler(CommandHandler("lunch_begin", comida_ini))
    app.add_handler(CommandHandler("lunch_end", comida_fin))
    app.add_handler(CommandHandler("end", end))

    app.run_polling()

if __name__ == "__main__":
    main()