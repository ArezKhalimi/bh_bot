import random

from celery import Celery
from celery.schedules import crontab

from bohdata_bot_handler import BotHandler
from constants import MORNING_GREETINGS
from conf import TOKEN


greet_bot = BotHandler(TOKEN)
app = Celery('tasks', broker='redis://localhost:6379/0')


@app.on_after_configure.connect
def setup_morning_greetings_task(sender, user_id, chat_name, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        morning_greetings_task.s(user_id, chat_name),
    )


@app.task
def morning_greetings_task(user_id, chat_name):
    greet_bot.send_message(
        user_id, '{} {}'.format(random.choice(MORNING_GREETINGS), chat_name)
    )
