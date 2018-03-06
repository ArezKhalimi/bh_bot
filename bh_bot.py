import datetime

import redis as redis_cli
from celery import Celery

from bohdata_bot_handler import BotHandler
from conf import TOKEN
from tasks import morning_greetings_task, setup_morning_greetings_task


greet_bot = BotHandler(TOKEN)
now = datetime.datetime.now()
redis = redis_cli.StrictRedis(host='localhost', port=6379, db=1)
app = Celery('tasks', broker='redis://localhost:6379/0')
app.conf.timezone = 'Europe/Kiev'


def main():
    print('Start')
    offset = redis.get('offset')

    while True:
        clients = redis.lrange('clients', 0, -1)
        data = greet_bot.get_updates(offset)
        for message in data:
            update_id = message['update_id']
            chat_id = message['message']['chat']['id']
            chat_name = message['message']['chat']['first_name']
            if update_id:
                redis.set('update_id', update_id)
            if chat_id not in clients:
                redis.lpush('clients', 1)
                setup_morning_greetings_task(app, chat_id, chat_name)

            if redis.get('update_id'):
                offset = int(redis.get('update_id')) + 1
                redis.set('update_id', offset)

            chat_text = message['message']['text']

            if 'hello' in chat_text.lower():
                morning_greetings_task(chat_id, chat_name)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
