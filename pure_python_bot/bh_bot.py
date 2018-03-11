import datetime

import redis as redis_cli
from celery import Celery

from bohdata_bot_handler import BotHandler
from commands_handler import CommandsHandler
from conf import TOKEN
from tasks import setup_morning_greetings_task


greet_bot = BotHandler(TOKEN)
now = datetime.datetime.now()
redis = redis_cli.StrictRedis(host='localhost', port=6379, db=1)
app = Celery('tasks', broker='redis://localhost:6379/0')
app.conf.timezone = 'Europe/Kiev'


def is_bot_command(message):
    return all(
        [message.starwith('/'), message['entities'], message['entities'] == 'bot_command']
    )


def main():
    print('Start')
    offset = redis.get('offset')

    while True:
        clients = redis.lrange('clients', 0, -1)
        data = greet_bot.get_updates(offset)
        for request in data:
            update_id = request['update_id']
            message = request['message']
            user_id = message['from']['id']
            user_name = message['chat']['first_name']
            if update_id:
                redis.set('update_id', update_id)
            if user_id not in clients:
                redis.lpush('clients', 1)
                setup_morning_greetings_task(app, user_id, user_name)

            if redis.get('update_id'):
                offset = int(redis.get('update_id')) + 1
                redis.set('update_id', offset)

            if is_bot_command(message):
                CommandsHandler.launch_command(message['text'], user_id)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
