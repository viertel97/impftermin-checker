import os
import time

import telegram
from selenium import webdriver

from utils import log

file_name = os.path.basename(__file__)
chat_id = "1234"
wait_time = 50
counter_threshold = 15

token = "TOKEN"
channel_id = "-1234"
url = "https://cqm.cleverq.de/public/sites/250/appointments/index.html?lang=de&service_id=1119"
text1 = "BioNTech Impftermin - Impfberechtigung als Kontaktperson nach § 3 Abs. 1 Nr. 3 a CoronaImpfV"

bot = telegram.Bot(token=token)

if os.name == "nt":
    wait_time = 10
    # counter_threshold = 10
    # update_counter_threshold = 20
    windows = True


def main():
    send_messages([chat_id], text="Checker: Bot started")
    log(text="Checker: Bot started", file_name=file_name)
    counter = 0
    while True:
        a_element = None
        b_element = None
        c_element = None
        driver = webdriver.Chrome()
        driver.delete_all_cookies()
        driver.get(url)
        time.sleep(5)

        a_xpath = "//*[contains(text(), '{}')]".format(text1)
        try:
            a_element = driver.find_elements_by_xpath(a_xpath)[0]
        except:
            send_messages([channel_id], text="Fehlermeldung. Eventuell Termine verfügbar! \n " + str(url))
            driver.delete_all_cookies()
            driver.close()
            log("wait " + str(wait_time) + "s", file_name=file_name)
            counter = counter + 1
            log(str(counter) + "/" + str(counter_threshold), file_name=file_name)
            time.sleep(wait_time)
            break
        webdriver.ActionChains(driver).move_to_element(a_element).click(a_element).perform()
        # a_element.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        b_xpath = "//*[contains(text(), 'Weiter zur Terminauswahl')]"
        b_element = driver.find_elements_by_xpath(b_xpath)[0]
        # time.sleep(5)
        # webdriver.ActionChains(driver).move_to_element(b_element).click(b_element).perform()
        b_element.click()
        time.sleep(5)
        c_xpath = "//*[contains(text(), 'Für Ihre Auswahl sind leider aktuell alle Termine ausgebucht. Bitte versuchen Sie es zu einem späteren Zeitpunkt erneut.')]"
        try:
            c_element = driver.find_elements_by_xpath(c_xpath)
            if c_element:
                if counter % counter_threshold == 0:
                    log("nichts verfügbar!", file_name=file_name)
                    send_messages([], text="nichts verfügbar!")
                    counter = 0
                else:
                    log("nichts verfügbar", file_name=file_name)
            else:
                log("Verfügbar!", file_name=file_name)
                send_messages([channel_id], text="Verfügbar! \n " + str(url))
        except:
            send_messages([channel_id], text="Verfügbar! \n " + str(url))
        driver.delete_all_cookies()
        driver.close()
        log("wait " + str(wait_time) + "s", file_name=file_name)
        counter = counter + 1
        log(str(counter) + "/" + str(counter_threshold), file_name=file_name)
        time.sleep(wait_time)


def send_messages(chat_ids: list, text):
    for chat_id in chat_ids:
        log(str(chat_id) + " : " + str(text), file_name=file_name)
        bot.sendMessage(chat_id=chat_id, text=text)


if __name__ == "__main__":
    main()
