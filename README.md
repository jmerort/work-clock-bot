Work Clock Telegram bot for Python
___


This Telegram bot will serve as your personal work time assistant, tracking the time you spend at work, including possible breaks, and tell you at which time you're supposed to clock out. It will also track the under- and over-time you spend at work, making it easier for you to manage your work week and keep track of how much time you spend each day.


# Progress

## Version 0.1
- The Bot will let you enter 4 log times per day (begin, end, lunch_begin, lunch_end).
- When leaving work, the bot will tell you how much time you spend (h, min) at work that day.
- The Bot will respond properly to invalid commands (clocking out before having clocked in and so on).

Added functions:
    -begin: store the current begin time and set state to `Working=True`
    -start_lunch: store the lunch time begin and set `Eating=True` if `Working=True`, else throw error.
    -end_lunch: store the lunch time and set `Eating=False` end if `Working=True` and `Eating=True` else throw error. 
    -end: store the end work time and set `Working=False` and print the time spent at work today if `Working=True` and `Eating=False` else throw error.

## Version 0.2
- The Bot will include a `/check` command to check the time at which the user can leave work, based on a constant number of daily hours per day (same for every day).

Added functions:
    -check: See the time at which you can leave work and accomplish the minimum goal hours.

## Version 0.3
- The bot will allow multiple goal hours depending on the day of the week (edit in `data/credentials.py` file).

# To be added
- Option to add daily reminders to clock in and out at the chosen times.
- `/help` command to see available commands.
- Weekly track of time worked every day.

# How to install and use the bot
1) Clone this repo
2) In the data/credentials.py file, change the `bot_token` variable to match yours (if you don't have one yet, check this guide: [From BotFather to 'Hello World'](https://core.telegram.org/bots/tutorial)) and choose your goal working hours for each week day (Monday to Sunday) e.g. `[8, 8, 8, 8, 8, 0, 0]` for a 9 to 5.
3) Run `run_bot.py` and talk to your telegram bot using the following commands:
    - `/begin` : Clock in. Begin work day and start counting time.
    - `/lunch_begin` : Begin lunch break. Stop counting time until lunch is over.
    - `/lunch_end` : End lunch break and resume counting time.
    - `/end` : End work day and print how much time you spent working.
    - `/check` : Check at which time you can leave work, based on the number of hours needed (8 by default).