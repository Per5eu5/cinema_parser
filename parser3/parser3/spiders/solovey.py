# -*- coding: utf-8 -*-
import scrapy
from ..items import Detail
from urllib.parse import urljoin
import datetime


class SoloveySpider(scrapy.Spider):
    name = 'solovey'

    start_urls = ['https://kinocenter.ru/repertoire/']

    def parse(self, response):

        dates_in_schedule = response.xpath('//select[@id="showDate"]')
        date_in_schedule = dates_in_schedule.xpath('option[@value]/text()').extract()[1:]  # первое значение мусор

        yield response.follow('https://kinocenter.ru/repertoire/tomorrow.php', callback=self.parse_main_page)

        for i, date in enumerate(date_in_schedule):
            yield response.follow('https://kinocenter.ru/repertoire/date.php?date=' + date,
                                  callback=self.parse_main_page)

        yield response.follow('https://kinocenter.ru/repertoire/', callback=self.parse_main_page)

    def parse_main_page(self, response):
        all_films = response.xpath('//div[@class="item"][@style]')

        for film in all_films:
            if response.url == 'https://kinocenter.ru/repertoire/':
                today = datetime.datetime.today()
                link = film.xpath('div[@class="description"]/a/@href'
                                  ).extract_first() + '&repertore_start=' + today.strftime('%d.%m.%Y')
                yield response.follow(link, self.parse_detail_page)
            else:
                link = film.xpath('div[@class="description"]/a/@href').extract_first()
                yield response.follow(link, self.parse_detail_page)

    def parse_detail_page(self, response):
        items = Detail()

        items['title'] = response.xpath('//td[@class="title"]/text()').extract_first()
        items['age'] = response.xpath('//td[@class="age"]/span/text()').extract_first()
        items['date'] = response.xpath('//input[@id="repertore_start"]/@value').extract_first()
        items['poster'] = urljoin(response.url, response.xpath('//div[@class="poster"]/img/@src').extract_first())
        items['url'] = response.url

        # description = response.xpath('//div[@class="movie_description"]/div[@class="description"]/text()').extract()
        # items["description"] = description

        all_sessions = response.xpath('//a[@class="kh_boxoffice item"]')

        for session in all_sessions:
            items['cost'] = session.xpath('div[@class="cost"]/text()').extract_first()
            items['start_time'] = session.xpath('div[@class="time"]/text()').extract_first()
            items['hall'] = session.xpath('div[@class="hall"]/text()').extract_first()

            dimension = session.xpath('div[@class="d"]/text()').extract_first()

            if dimension is None:
                items['dimension'] = '2D'
            else:
                items['dimension'] = dimension

            yield items
