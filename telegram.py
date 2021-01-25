

import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date


class Telegram:

    @classmethod
    def sendAlert(cls, sortedPosts):

        urlAPITelegram = "https://api.telegram.org/botXXX&chat_id=@id&text="   #ChangeME

        dt_from_str = lambda dt: datetime.datetime.strptime(dt, '%Y-%m-%d').date()
        allTxtNovedades = ""

        for post in sortedPosts:

            if dt_from_str(post['date']) == date.today():

                if ( "TIC" not in post['ramas'] and "Investigación" not in post['ramas']):
                    continue

                novedades = post['org'] + "  " + str(dt_from_str(post['date'])) + "\n*" + post['title'] + "\n\n"
                allTxtNovedades = allTxtNovedades + novedades

        if not allTxtNovedades:
            allTxtNovedades = "No se encontraron vacantes relevantes"

        requests.get( urlAPITelegram + allTxtNovedades)
