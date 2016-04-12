# -*- coding: utf-8 -*-
import scrapy
import unicodedata
from marklogic.items import EventItem


class EventsSpider(scrapy.Spider):
    name = "MarkLogic Events"
    #allowed_domains = ["http://www.marklogic.com/events"]
    start_urls = (
        'http://www.marklogic.com/events/',
    )

    def parse(self, response):
        # Process first page of news articles
        for href in response.xpath('//h3/a/@href'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, self.parse_events)
            
    def parse_events(self, response):
        item = EventItem()
    
        item ['uri'] = response.url
        item ['spider'] = self.name
        item ['title'] = response.xpath('//h2/node()').extract()[0].strip()
        item ['date'] = response.xpath("//p[@class='event-date']/node()")[0].extract().strip()
        text = response.xpath('//div[@class="event-content entry"]/p[not(@*)]').extract()
        text = u''.join([t.strip() for t in text])
        item ['content'] = text
        item ['location'] = response.xpath('//p[@class="event-city"]/node()')[0].extract().strip()
        item ['regurl'] = response.xpath('//p[@class="event-links"]/a/@href')[0].extract().strip()
    
        yield item
        
    # Handles crazy unicode characters by translating them back into ACII
    def unicode_translate(self, text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')