import os
import time
from datetime import datetime, timedelta

import requests
import telegram
from dateutil.relativedelta import relativedelta
from telegram import ChatAction, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
from telegram.ext.dispatcher import run_async

from utils import log, read_ids

file_name = os.path.basename(__file__)

chat_id = "1234"

wait_time = 15
counter_threshold = 50
answer_string = '{"duration":3,"duration_minutes":15,"available_days":[]}'

channel_id = "-1234"
token = "TOKEN"
url = "https://cqm.cleverq.de/public/sites/250/appointments/index.html?lang=de&service_id=1096"

bot = telegram.Bot(token=token)


def main():
    send_messages([chat_id, channel_id], text="Rest-Checker U60: Loop started")
    log(text="Rest-Checker: Loop started", file_name=file_name)
    counter = 101
    while True:
        today_date = datetime.today().strftime("%Y-%m-%d")
        new_date = (datetime.today() + relativedelta(years=1) + relativedelta(days=4)).strftime("%Y-%m-%d")

        rest_url = "https://cqm.cleverq.de/api/external/v2/sites/250/appointments/available_days?service_id=1096&from_day={}&to_day={}&subtask_items[]=%7B%22subtask_id%22:1455,%22number%22:1%7D".format(
            today_date, new_date
        )

        try:
            response = requests.get(rest_url)
            if response.text == answer_string:
                if counter % counter_threshold == 0:
                    send_messages([], text="nichts verfügbar!")
                    counter = 0
                else:
                    log("nichts verfügbar", file_name=file_name)
            else:
                log("Verfügbar!", file_name=file_name)
                send_messages([channel_id], text="Verfügbar! \n " + str(url))
        except requests.exceptions.ConnectionError:
            log("Connection refused")
        counter = counter + 1
        log(str(counter) + "/" + str(counter_threshold), file_name=file_name)
        log("wait " + str(wait_time) + "s", file_name=file_name)
        time.sleep(wait_time)


def send_messages(chat_ids: list, text):
    for chat_id in chat_ids:
        log(str(chat_id) + " : " + str(text), file_name=file_name)
        bot.sendMessage(chat_id=chat_id, text=text)


if __name__ == "__main__":
    main()
