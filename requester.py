#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class Requester:

    @classmethod
    def requestLink(cls, link):
        return cls.__get_content(cls, link)

    @classmethod
    def requestLinkPost(cls, link, payload):
        return cls.__get_content_postrequest(cls, link, payload)

    @classmethod
    def requestLinkNotChangeEncoding(cls, link):
        return cls.__get_content_not_change_encoding(cls, link)

    @classmethod
    def requestLinkPostCookies(cls, link, payload, cookies):
         return cls.__get_content_postrequest_cookies(cls, link, payload, cookies)

    def __get_content(self, url):
        res = requests.get(url, timeout=200)
        if(res.encoding.lower() != 'utf-8'): #https://stackoverflow.com/questions/44203397/python-requests-get-returns-improperly-decoded-text-instead-of-utf-8
            res.encoding = 'UTF-8'
        return self.__parseHTML(self, res)

    def __get_content_not_change_encoding(self, url):
        res = requests.get(url)
        return self.__parseHTML(self, res)

    def __get_content_postrequest(self, url, payload):
        res = requests.post(url, data=payload)
        return self.__parseHTML(self, res)

    def __get_content_postrequest_cookies(self, url, payload, cookies):
        res = requests.post(url, data=payload, cookies=cookies)
        return self.__parseHTML(self, res)

    def __parseHTML(self, res):

        try:
            res.raise_for_status()
        except Exception as exc:
            return BeautifulSoup("", "lxml")

        soup = BeautifulSoup(res.text, "lxml")
        return soup
