# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import Rule, CrawlSpider
from kassir.items import Event
from scrapy.contrib.linkextractors import LinkExtractor


class EventSpider(CrawlSpider):
    name = 'event_spider'
    allowed_domains = ['spb.kassir.ru']
    start_urls = ['https://spb.kassir.ru/kassir/search?categories=c&page=\d+']
    rules = [Rule(LinkExtractor(allow=['/kassir/search/index\?categories=c']), follow=True),
             Rule(LinkExtractor(allow=['/kassir/event/view/\d+']), 'parse_event')]

    def __init__(self, gui):
        self.gui = gui
        super(EventSpider, self).__init__()

    def parse_event(self, response):
        event = Event()
        event['name'] = response.xpath('//h1[@class="event-header__title"]/text()').extract()
        event['date'] = response.xpath('//div[@class="event-header__date"]/span[@class="date"]/text()').extract()
        event['url'] = response.url
        return event