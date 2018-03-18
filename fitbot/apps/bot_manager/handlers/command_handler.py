from datetime import date

import redis as redis_cli

from . import BotHandler


redis = redis_cli.StrictRedis(host='localhost', port=6379, db=1)


class CommandsHandler:

    def is_bot_command(self, message):
        return all(
            [message.starwith('/'), message['entities'], message['entities'] == 'bot_command']
        )

    def get_user_key(self, user_id):
        date_key = day.today().isoformat()
        key = 'user{}day{}'.format(date_key, user_id)

        return key

    def bad_command(self, user_id):
        BotHandler.send_message(user_id, 'Wrong command')

    def launch_command(self, text, user_id):
        command_name = text.split(' ')[1:]
        args = text.split(' ')[1:]
        command = getattr(self, command_name, None)

        if command:
            command(user_id, args)
        else:
            self.bad_command(user_id)

    def ate(self, user_id, data):
        data = data[0]
        key = self.get_user_key(user_id)
        redis.set(key, kcal + product)

    def add(self, user_id, data):
        redis.set('product', )