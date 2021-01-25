#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parsing import Parsing
from requester import Requester
import re
from datetime import datetime
from urllib.request import urlretrieve
from datetime import date
from dateutil.relativedelta import relativedelta


class ScraperBOE:

    def __init__(self, num):
        self.posts = []
        self.url_base= "https://www.boe.es/boe/dias/"
        self.url_suffix = "/index.php?s=2B"
        self.num_days = num

    
    def build(self):

        print('\nScraping BOE...')
        posts = []
        for i in range(0, self.num_days):

            dateToScrap = datetime.now() + relativedelta(days=-i)
            urlBOE = self.url_base+dateToScrap.strftime("%Y/%m/%d")+self.url_suffix   #build url to scrap

            postsOneDay = self.__parse_resource(Requester.requestLink(urlBOE), urlBOE, dateToScrap)

            if (postsOneDay):
                posts.extend(postsOneDay)

        return posts


    def __parse_resource(self, resource, url, date):

        posts = []
        for postElement in resource.findAll("li", {"class": ["dispo"]}):

            try:

                titleText = postElement.find("p").getText()
                titleTextLower = titleText.lower()

                if(  "coruña" in titleTextLower or
                     "pontevedra" in titleTextLower or
                     "lugo" in titleTextLower or
                     "orense" in titleTextLower or
                     "santiago de compostela" in titleTextLower or
                     "galicia" in titleTextLower):

                    if (not Parsing.esPlazaPersonalBOE(titleText)):
                        continue

                    liConEnlaceHTML = postElement.find("li", {"class": ["puntoHTML"]})
                    linkDetalleBOE = 'https://www.boe.es' + liConEnlaceHTML.find("a")['href']

                    webBOE = Requester.requestLink(linkDetalleBOE)

                    ramas = Parsing.extraeRamas(' ', titleText)
                    detallePraza = Parsing.extraeDetallePrazas(webBOE, True, titleText)

                    posts.append(
                        {
                            'org': 'BOE',
                            'title': titleText,
                            'url': url,
                            'boe_url': linkDetalleBOE,
                            'date': date.strftime("%Y-%m-%d"),
                            'date_short': date.strftime("%d/%m/%y"),
                            'ramas' : ramas,
                            'fuente': 'boe',
                            'active': 'yes',
                            'title_pdf': detallePraza,
                        }
                    )

            except IndexError:
                print("No se puede captuar el contenido")

        return posts