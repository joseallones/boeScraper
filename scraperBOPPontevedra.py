#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parsing import Parsing
from requester import Requester
import re
from datetime import datetime
from urllib.request import urlretrieve
from datetime import date
from dateutil.relativedelta import relativedelta


class ScraperBOPPontevedra:

    def __init__(self, num):
        self.posts = []
        self.url_base= "https://boppo.depo.gal/detalle/-/boppo/"
        self.num_days = num

    def build(self):

        print('\nScraping BOP Pontevedra...')

        posts = []
        for i in range(0, self.num_days):

            dateToScrap = datetime.now() + relativedelta(days=-i)
            urlBOP = self.url_base+dateToScrap.strftime("%Y/%m/%d")

            try:
                webBOP = Requester.requestLink(urlBOP)
                postsOneDay = self.__parse_resource(webBOP, urlBOP, dateToScrap)

                if (postsOneDay):
                    posts.extend(postsOneDay)

            except Exception as e:
                print(e)
                print("BOP Pontevedra no responde")

        return posts


    def __parse_resource(self, resource, url, date):

        posts = []

        divElement=resource.find("div", {"id": ["contSumario"]})
        if(divElement is None):
            return

        item = resource.find("a", {"class": ["botDescPDF"]}).findNext()
        organismo = ""

        while (item is not None):

            claseElemento = ""
            if "class" in item.attrs:
                contentClass = item.attrs['class']
                if (contentClass and len(contentClass)>0):
                    claseElemento = item.attrs['class'][0]


            if (item.name == 'span' and claseElemento == 'pub'):
                organismo = item.getText()

            elif ((organismo) and item.name == 'a' and claseElemento == 'botDescPDF'):
                urlPdfBopDetalle = 'https://boppo.depo.gal' + item['href']

            elif ((organismo) and item.name == 'p' and claseElemento == 'sumario'):

                originalText = item.getText().strip().replace(u'\n', ' ')

                if (Parsing.esPlazaPersonal(originalText)):

                    ramas = Parsing.extraeRamas(organismo, originalText)
                    posts.append(
                        {
                            'org': 'BOP Pontevedra - ' + organismo,
                            'title': originalText.title(),
                            'url': url,
                            'fuente': 'bop_pontevedra',
                            'ramas': ramas,
                            'active': 'yes',
                            'date': date.strftime("%Y-%m-%d"),
                            'date_short': date.strftime("%d/%m/%y"),
                            'bop_url': urlPdfBopDetalle,
                        }
                    )

            item = item.findNext()

        return posts