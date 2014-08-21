# -*- coding: utf-8 -*- #

from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request

from stats.items import *



class StatsSpider(CrawlSpider):
    name = 'quhua'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/']
    rules = (
        #处理省级列表
        Rule(LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/index\.html')), callback='Layer01_Parse'),
        )

    def Layer01_Parse(self, response):

        item = Layer01_Item()
        for i in LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/\d\d\.html')).extract_links(response):
            url = i.url
            text = i.text
            item['year'] = url[-12:-8]
            item['name'] = text
            item['code'] = url[-7:-5]
            yield item
            yield Request(url, callback=self.Layer02_Parse)


    def Layer02_Parse(self, response):
        text = response.xpath('/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table')\
               [0].extract()
        item = Layer02_Item()
        item['year'] = re.findall(r'dm/20\d\d', response.url)[0][3:]
        for code, name in re.findall(r'href="\d\d/(\d{4})\.html">([^\d]+?)</a>', text):
            item['name'] = name
            item['code'] = code
            yield item
        for i in LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/\d\d/\d{4}\.html')).extract_links(response):
            url = i.url
            text = i.text
            yield Request(url, callback=self.Layer03_Parse)

    def Layer03_Parse(self, response):
        text = response.xpath('/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table')\
               [0].extract()
        item = Layer03_Item()
        item['year'] = re.findall(r'dm/20\d\d', response.url)[0][3:]
        for code, name in re.findall(r'href="\d\d/(\d{6})\.html">([^\d]+?)</a>', text):
            item['name'] = name
            item['code'] = code
            yield item
        for i in LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/\d\d/\d\d/\d{6}\.html')).extract_links(response):
            url = i.url
            text = i.text
            yield Request(url, callback=self.Layer04_Parse)

    def Layer04_Parse(self, response):
        text = response.xpath('/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table')\
               [0].extract()
        item = Layer04_Item()
        item['year'] = re.findall(r'dm/20\d\d', response.url)[0][3:]
        for code, name in re.findall(r'href="\d\d/(\d{9}).html">([^\d]+?)</a>', text):
            item['name'] = name
            item['code'] = code
            yield item
        for i in LinkExtractor(allow=(r'tjyqhdmhcxhfdm/20\d\d/\d\d/\d\d/\d\d/\d{9}\.html')).extract_links(response):
            url = i.url
            text = i.text
            yield Request(url, callback=self.Layer05_Parse)

    def Layer05_Parse(self, response):
        text = response.xpath('/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table')\
               [0].extract()
        item = Layer05_Item()
        item['year'] = re.findall(r'dm/20\d\d', response.url)[0][3:]
        for code, code2, name in re.findall(r'<td>(\d{12})</td><td>(\d\d\d)</td><td>(.+?)</td>', text):
            item['name'] = name
            item['code'] = code
            item['code2'] = code2
            yield item
