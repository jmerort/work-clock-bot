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

global working, eating, eaten, daily_goal

working = False
eating = False
eaten = False
daily_goal = 8 # Number of hours user is supposed to work per day

# Dictionary to store the four clock times
times = {
    'begin' : None,
    'lunch_begin' : None,
    'lunch_end' : None,
    'end' : None,
}

async def begin(update, context):
    """
    Begin work day.
    """
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
    global working, eating, eaten
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
        eaten = False


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
    """
    End work day, print time worked.
    """
    global working, eating, eaten
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
        times['end'] = datetime.now()
        await update.message.reply_text(
            f"Work end: {times['end'].strftime('%H:%M')}\n",
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
        
        # Reset all flags
        working = False
        eating = False
        eaten = False
        return
    

async def check(update, context):
    """
    Print the time at which you're supposed to leave to fulfill the work hours
    """
    global daily_goal
    
    if not working: # BUG the program doesn't ever get here for some reason
        await update.message.reply_text(f"You are not currently working.")
        return
    
    current_time = datetime.now()
    if eaten:
        # tiempo = (hora salida - hora inicio) - (comida_fin - comida_inicio)
        total_s = diferencia_tiempos(times['begin'], current_time)
        lunch_s = diferencia_tiempos(times['lunch_begin'], times['lunch_end'])
        work_s = total_s - lunch_s

        seconds_left = daily_goal * 3600 - work_s
        if seconds_left > 0:
            leave_time = sum_seconds(current_time, seconds_left)
            await update.message.reply_text(f"You can leave at {leave_time.hour}:{leave_time.minute}.")
        else:
            await update.message.reply_text(f"You can leave already.")
        return
    elif eating: # If eating
        work_s = diferencia_tiempos(times['begin'],times['lunch_begin'])

        seconds_left = daily_goal * 3600 - work_s
        if seconds_left > 0:
            leave_time = sum_seconds(current_time, seconds_left)
            await update.message.reply_text(f"You can leave at {leave_time.hour}:{leave_time.minute}.")
        else:
            await update.message.reply_text(f"You can leave already.")
        return
    else: # If not yet eaten
        work_s = diferencia_tiempos(times['begin'], current_time)

        seconds_left = daily_goal * 3600 - work_s
        if seconds_left > 0:
            leave_time = sum_seconds(current_time, seconds_left)
            await update.message.reply_text(f"You can leave at {leave_time.hour}:{leave_time.minute}.")
        else:
            await update.message.reply_text(f"You can leave already.")
        return
        



def sum_seconds(time, added_seconds):
    """
    Takes a datetime object and returns another datetime object after n seconds have passed.
    Assumes the seconds are less than 24 hours. 
    """
    current_s = time.hour * 3600 + time.minute * 60 + time.second
    final_s = current_s + added_seconds

    h = final_s // 3600
    m = (final_s - h * 3600) // 60
    s = (final_s - h * 3600 - m * 60)

    final_time = datetime(
        year=1,
        month=1,
        day=1,
        hour=h,
        minute=m,
        second=s
        )
    
    return final_time

        



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
    app.add_handler(CommandHandler("check", check))


    app.run_polling()

if __name__ == "__main__":
    main()