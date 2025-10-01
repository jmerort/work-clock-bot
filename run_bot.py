"""
Work Clock bot launch client 

@jmerort
Sep 2025
"""

from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime, timedelta

from data.credentials import bot_token

global TOKEN
TOKEN = bot_token # Stored in local .py file

global working, eating

working = False
eating = False
eaten = False

# Dictionary to store the four clock times
times = {
    'begin' : None,
    'lunch_begin' : None,
    'lunch_end' : None,
    'end' : None,
}

async def begin(update, context):
    global working
    # Check if user hasn't yet clocked out
    if working:
        await update.message.reply_text(f"You already clocked in at {times['begin'].strftime('%H:%M')}.")
        return
    else:
        # Save clock in time and update flag
        times['begin'] = datetime.now()
        await update.message.reply_text(
            f"Work begin: {times['begin'].strftime('%H:%M')}"
        )
        working = True


async def lunch_begin(update, context):
    global working, eating
    # save current time as start time
    if working == False:
        await update.message.reply_text(f"You haven't yet clocked in.")
        return
    else:
        times['lunch_begin'] = datetime.now()
        await update.message.reply_text(
            f"Lunch begin: {times['lunch_begin'].strftime('%H:%M')}"
        )
        eating = True


async def lunch_end(update, context):
    global working, eating, eaten
    if eating == False:
        await update.message.reply_text(f"You haven't started eating.")
        return
    else:
        chat_id = update.effective_chat.id
        # save current time as start time
        times['lunch_end'] = datetime.now()
        await update.message.reply_text(
            f"Lunch end: {times['lunch_end'].strftime('%H:%M')}"
        )
        eating = False
        eaten = True


async def end(update, context):
    global working, eating
    times['end'] = datetime.now()
    # Check if user hasn't clocked in
    if working == False:
        # Error, can't clock out
        await update.message.reply_text("You haven't yeat clocked in.")
        return
    # Check if user still eating
    elif eating == True:
        # Error, can't clock out
        await update.message.reply_text("You haven't finished lunch.")
        return
    else:
        end_time = datetime.now()
        await update.message.reply_text(
            f"Work end: {end_time.strftime('%H:%M')}\n",
        )
        # Print total hours and minutes worked
        if eaten:
            # tiempo = (hora salida - hora inicio) - (comida_fin - comida_inicio)
            total_s = diferencia_tiempos(times['begin'], times['end'])
            lunch_s = diferencia_tiempos(times['lunch_begin'], times['lunch_end'])
            work_s = total_s - lunch_s
            hours_worked = work_s//3600
            minutes_worked = (work_s - hours_worked*3600)//60
            await update.message.reply_text(f"Total time worked: {hours_worked} h {minutes_worked} m.")

        else:
            work_s = diferencia_tiempos(times['begin'],times['end'])
            hours_worked = work_s//3600
            minutes_worked = (work_s - hours_worked*3600)//60
            await update.message.reply_text(f"Total time worked: {hours_worked} h {minutes_worked} m.")
        working = False


def diferencia_tiempos(hora_ini, hora_fin):
    """
    Devuelve la diferencia de tiempos entre dos datetime, en segundos (asume que son del mismo día, es
    decir, que los días de diferencia son 0)
    """
    return int((hora_fin - hora_ini).total_seconds())


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Set working and eating flags to False
    working = False
    eating = False
    eaten = False

    # command handlers
    app.add_handler(CommandHandler("begin", begin))
    app.add_handler(CommandHandler("lunch_begin", lunch_begin))
    app.add_handler(CommandHandler("lunch_end", lunch_end))
    app.add_handler(CommandHandler("end", end))

    app.run_polling()

if __name__ == "__main__":
    main()