from telegram import message
import ptbot
import os
import random
from pytimeparse import parse


def render_progressbar(total,
                       iteration,
                       prefix='',
                       suffix='',
                       length=30,
                       fill='█',
                       zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, author_id, message_id, message_time):
    bot.update_message(author_id,
                       message_id,
                       f"Осталось {secs_left} cекунд\n{render_progressbar(message_time, message_time - secs_left)}")


def main(chat_id, message_time):
    message_id = bot.send_message(chat_id,"Таймер запущен")
    bot.create_countdown(parse(message_time),
                         notify_progress,
                         author_id=chat_id,
                         message_id=message_id,
                         message_time=parse(message_time))
    bot.create_timer(parse(message_time), finish_of_countdown, author_id=chat_id)


def finish_of_countdown(author_id):
    bot.send_message(author_id, "Времы вышло")


if __name__ == '__main__':
    tg_token = os.environ['TELEGRAM_TOKEN']
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(main)
    bot.run_bot()
