import random

from fitbot import celery_app
from celery.schedules import crontab

from fitbot.apps.bot_manager.handlers import BotHandler, CommandsHandler
from fitbot.apps.profiles.models import TelegramUser

redis = redis_cli.StrictRedis(host='localhost', port=6379, db=4)

@celery_app.task
def test():
    redis.set('axa',123)

@celery_app.task
def main():
    offset = redis.get('offset', 0)
    data = BotHandler.get_updates(offset)
    for request in data:
        update_id = request['update_id']
        message = request['message']
        user_id = message['from']['id']
        user_name = message['chat']['first_name']

        if update_id:
            redis.set('update_id', update_id)

        if user_id not in clients:
            redis.lpush('clients', 1)
            TelegramUser.objects.create(
                first_name=message['from']['first_name'],
                last_name=message['from']['last_name'],
                telegram_id=int(message['from']['id']),
                username=int(message['from']['username']),
            )
            setup_morning_greetings_task(app, user_id, user_name)

        if redis.get('update_id'):
            offset = int(redis.get('update_id')) + 1
            redis.set('update_id', offset)

        if is_bot_command(message):
            CommandsHandler.launch_command(message['text'], user_id)
        else:
            morning_greetings_task(user_id)
            print ('holla')

@celery_app.on_after_configure.connect
def setup_morning_greetings_task(sender, user_id, chat_name, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        morning_greetings_task.s(user_id, chat_name),
    )


@celery_app.task
def morning_greetings_task(user_id, chat_name):
    greet_bot.send_message(
        user_id, '{} {}'.format(random.choice(MORNING_GREETINGS), chat_name)
    )
