#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scraperBOPCorunha import ScraperBOPCorunha
from scraperBOPPontevedra import ScraperBOPPontevedra
from scraperBOE import ScraperBOE
from telegram import Telegram
from storage import Storage
import datetime
import requests

basePath = "storage/"
num_days_to_scrap = 5

posts = []
posts.extend( ScraperBOE(num_days_to_scrap).build() )
posts.extend( ScraperBOPCorunha(num_days_to_scrap).build())
posts.extend( ScraperBOPPontevedra(num_days_to_scrap).build() )

sortedPosts = sorted(posts, key=lambda i: i['date'], reverse=True)

Telegram.sendAlert(sortedPosts)

now = datetime.datetime.now()

Storage.save(basePath +'post_jobs_{0}-{1}-{2}.json'.format(now.year,now.strftime('%m'),now.strftime('%d')), sortedPosts)
print('\nDone!')