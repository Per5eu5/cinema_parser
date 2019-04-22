# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import Parser3Item
from ..items import Detail
import re
import datetime


class SoloveySpider(CrawlSpider):
    name = 'solovey'


    start_urls = [#'https://kinocenter.ru/repertoire/',
                  'https://kinocenter.ru/repertoire/tomorrow.php']

    rules = (
        #Rule(LinkExtractor(allow=('https://kinocenter.ru/repertoire/',), deny=('movie', 'tomorrow', 'time', 'show', 'halls', 'genre', 'novelties',)), callback='parse_main_pages'),
        Rule(LinkExtractor(allow=('kinocenter.ru/repertoire/tomorrow.php',), deny=('movie', 'genre', 'show')), callback='parse_main_page'),

        # Rule(LinkExtractor(allow=('427889')), callback='parse_detail_page'),
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="film_blocks active"]'), callback='parse_main_page'),
        Rule(LinkExtractor(allow=('movie')), callback='parse_detail_page'),
        #Rule(LinkExtractor(restrict_xpaths='//div[@class="film_blocks active"]'), callback='parse_detail_page'),

    )

    def parse_main_page(self, response):
        print('parse')
        items = Parser3Item()

        all_films = response.xpath('//div[@class="item"][@style]')
        dates = response.xpath('//select[@id="date"]')
        print(dates)

        for film in all_films:
            title = film.xpath('div[@class="description"]/a/text()').extract()
            age = film.xpath('div[@class="age"]/text()').extract()
            start_times = film.xpath('div[@class="shows_left"]/a/text()').extract()
            dimensions = film.xpath('div[@class="d"]/span/text()').extract()
            halls = film.xpath('div[@class="description"]/div[@class="links"]/div[@class="hall"]/text()').extract()
            poster = film.xpath('@style').extract()
            link = film.xpath('div[@class="description"]/a[@href]').extract()
            date = dates.xpath('option[@selected]/text()').extract()

            items['title'] = title[0].strip()  # нужно значение элемента, чтобы применить strip()
            items['age'] = age
            items['start_times'] = start_times
            items['dimensions'] = dimensions
            items['halls'] = halls
            items['poster'] = "https://kinocenter.ru" + poster[0].replace("background-image: "
                                                                          "url('", "").replace("');", "")
            items['link'] = 'https://kinocenter.ru/repertoire/movie/?movie_id=' + re.findall('[0-9]+', link[0])[0]
            # нули потому что возвращаются списки
            items['date'] = date

            yield items

    def parse_detail_page(self, response):

        items = Detail()

        #description = response.xpath('//div [@class="movie_description"]/div[@class="description"]/text()').extract()
        cost = response.xpath('//div[@class="cost"]/text()').extract()
        start_times_detail = response.xpath('//div[@class="time"]/text()').extract()
        #items["description"] = description
        items['cost'] = cost
        items['start_times_detail'] = start_times_detail

        yield items



