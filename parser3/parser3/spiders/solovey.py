# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import Parser3Item
from ..items import Detail
import re
import datetime


class SoloveySpider(scrapy.Spider):
    name = 'solovey'

    # def start_requests(self):
    #     yield scrapy.Request('https://kinocenter.ru/repertoire/', self.parse_main_page)
    #     yield scrapy.Request('https://kinocenter.ru/repertoire/tomorrow.php', self.parse_main_page)

    start_urls = ['https://kinocenter.ru/repertoire/']
                  #'https://kinocenter.ru/repertoire/tomorrow.php']

    # rules = (
    #     Rule(LinkExtractor(allow=('kinocenter.ru/repertoire/',), deny=('movie', 'tomorrow', 'time', 'show', 'halls', 'genre', 'novelties',)), callback='parse_main_pages'),
    #     Rule(LinkExtractor(allow=('kinocenter.ru/repertoire/tomorrow.php',), deny=('movie', 'genre', 'show')), callback='parse_main_page'),
    #     Rule(LinkExtractor(allow=('movie')), callback='parse_detail_page'),
    # )

    def parse(self, response):
        dates_in_schedule = response.xpath('//select[@id="date"]')
        date_in_schedule = dates_in_schedule.xpath('option[@value]/text()').extract()
       # print(len(date_in_schedule))

        for i, date in enumerate(date_in_schedule):
            #print(date)

            if i == 0:
                yield scrapy.Request('https://kinocenter.ru/repertoire/', callback=self.parse_main_page)
            elif i == 1:
                yield scrapy.Request('https://kinocenter.ru/repertoire/tomorrow.php', callback=self.parse_main_page)
            elif i > 1:
                yield scrapy.Request('https://kinocenter.ru/repertoire/date.php?date=' + date,
                                    callback=self.parse_main_page)




    def parse_main_page(self, response):
        items = Parser3Item()
        current_date = response.xpath('//select[@id="date"]/option[@selected]/text()').extract()
        #print(current_date)

        all_films = response.xpath('//div[@class="item"][@style]')

        for film in all_films:
            title = film.xpath('div[@class="description"]/a/text()').extract()
            age = film.xpath('div[@class="age"]/text()').extract()
            start_times = film.xpath('div[@class="shows_left"]/a/text()').extract()
            dimensions = film.xpath('div[@class="d"]/span/text()').extract()
            halls = film.xpath('div[@class="description"]/div[@class="links"]/div[@class="hall"]/text()').extract()
            poster = film.xpath('@style').extract()
            link = film.xpath('div[@class="description"]/a[@href]').extract()
            date = current_date

            items['title'] = title[0].strip()  # нужно значение элемента, чтобы применить strip()
            items['age'] = age
            items['start_times'] = start_times
            items['dimensions'] = dimensions
            items['halls'] = halls
            items['poster'] = "https://kinocenter.ru" + poster[0].replace("background-image: "
                                                                          "url('", "").replace("');", "")
            items['link'] = 'https://kinocenter.ru/repertoire/movie/?movie_id=' + re.findall('[0-9]+', link[0])[0]
            # нули потому что возвращаются списки
            #yield scrapy.Request(items['link'], self.parse_detail_page)

            items['date'] = date

            yield items

    def parse_detail_page(self, response):
        print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
        # items = Detail()
        #
        # #description = response.xpath('//div [@class="movie_description"]/div[@class="description"]/text()').extract()
        # cost = response.xpath('//div[@class="cost"]/text()').extract()
        # start_times_detail = response.xpath('//div[@class="time"]/text()').extract()
        # #items["description"] = description
        # items['cost'] = cost
        # items['start_times_detail'] = start_times_detail
        #
        # yield items



