#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import NavigableString, Tag

from parsing import Parsing
from requester import Requester
import re
from datetime import datetime
from datetime import datetime
from urllib.request import urlretrieve
from datetime import date
from dateutil.relativedelta import relativedelta


class ScraperBOPCorunha:
    """
        Clase para obtener el listado de vacantes
    """
    def __init__(self, num):
        self.posts = []
        self.url_base= "https://bop.dicoruna.es/bopportal/cambioBoletin.do?fechaInput="
        self.num_days = num
    
    def build(self):

        print('\nScraping BOP Corunha...')
        posts = []

        for i in range(0, self.num_days):

            dateToScrap = datetime.now() + relativedelta(days=-i)
            url = self.url_base+dateToScrap.strftime("%d/%m/%Y")  #build url to scrap. Example: https://bop.dicoruna.es/bopportal/cambioBoletin.do?fechaInput=20/01/2021

            web = Requester.requestLink(url)

            postsOneDay = self.__parse_resource(web, url, dateToScrap)

            if (postsOneDay):
                posts.extend(postsOneDay)

        return posts


    def __parse_resource(self, resource, url, date):

        posts = []
        divElement=resource.find("div", {"id": ["boletin"]})
        if(divElement is None):
            return

        divAnuncios = divElement.find_all("div", {"class": ["bloqueAnuncio"]})

        for divAnuncio in divAnuncios:

            try:
                organismoElement = divAnuncio.find("h3", {"class": ["tituloEdicto"]})
                if(organismoElement is None):
                    continue

                organismo = organismoElement.getText()
                linksAnuncios = divAnuncio.find_all("a")
                text = linksAnuncios[1].getText().strip().replace(u'\n', ' ')
                urlPdfBop  = linksAnuncios[0]['href']
                urlPdfBop = 'https://bop.dicoruna.es/bopportal/publicado/' + date.strftime("%Y/%m/%d") + "/" + urlPdfBop

                if (Parsing.esPlazaPersonal(text)):

                    ramas = Parsing.extraeRamas(organismo, text)
                    posts.append(
                        {
                            'org': 'BOP Coruña - ' + organismo,
                            'title': text,
                            'url': url,
                            'fuente': 'bop_corunha',
                            'ramas': ramas,
                            'active': 'yes',
                            'date': date.strftime("%Y-%m-%d"),
                            'date_short': date.strftime("%d/%m/%y"),
                            'bop_url': urlPdfBop,
                        }
                    )
            except Exception as e:
                continue

        return posts