# -*- coding: utf-8 -*-

# Scrapy settings for kassir_events project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kassir'

SPIDER_MODULES = ['kassir.spiders']
NEWSPIDER_MODULE = 'kassir.spiders'
ITEM_PIPELINES = {'kassir.pipelines.ItemNotify': 200}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kassir_events (+http://www.yourdomain.com)'
