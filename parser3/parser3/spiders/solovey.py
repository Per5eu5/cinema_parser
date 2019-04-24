# -*- coding: utf-8 -*-
import scrapy
from ..items import Parser3Item
from ..items import Detail
import re


class SoloveySpider(scrapy.Spider):
    name = 'solovey'

    start_urls = ['https://kinocenter.ru/repertoire/']

    def parse(self, response):
        dates_in_schedule = response.xpath('//select[@id="date"]')
        date_in_schedule = dates_in_schedule.xpath('option[@value]/text()').extract()

        for i, date in enumerate(date_in_schedule):
            if i == 0:
                yield scrapy.Request('https://kinocenter.ru/repertoire/', callback=self.parse_main_page)
            elif i == 1:
                yield scrapy.Request('https://kinocenter.ru/repertoire/tomorrow.php', callback=self.parse_main_page)
            else:
                yield scrapy.Request('https://kinocenter.ru/repertoire/date.php?date=' + date,
                                    callback=self.parse_main_page)

    def parse_main_page(self, response):
        items = Parser3Item()

        current_date = response.xpath('//select[@id="date"]/option[@selected]/text()').extract()
        all_films = response.xpath('//div[@class="item"][@style]')

        for film in all_films:
            title = film.xpath('div[@class="description"]/a/text()').extract_first()
            age = film.xpath('div[@class="age"]/text()').extract()
            start_times = film.xpath('div[@class="shows_left"]/a/text()').extract()
            dimensions = film.xpath('div[@class="d"]/span/text()').extract()
            halls = film.xpath('div[@class="description"]/div[@class="links"]/div[@class="hall"]/text()').extract()
            poster = film.xpath('@style').extract_first()
            link = film.xpath('div[@class="description"]/a[@href]').extract_first()
            date = current_date

            items['title'] = title.strip()
            items['age'] = age
            items['start_times'] = start_times
            items['dimensions'] = dimensions
            items['halls'] = halls
            items['poster'] = "https://kinocenter.ru" + poster.replace("background-image: "
                                                                          "url('", "").replace("');", "")
            items['link'] = 'https://kinocenter.ru/repertoire/movie/?movie_id=' + re.findall('[0-9]+', link)[0] +\
                            '&repertore_start=' + date[0]
            # ноль потому что возвращается список
            yield scrapy.Request(items['link'], self.parse_detail_page, meta={'date': date[0]})

            items['date'] = date

            yield items

    def parse_detail_page(self, response):
        items = Detail()

        # #description = response.xpath('//div [@class="movie_description"]/div[@class="description"]/text()').extract()
        cost = response.xpath('//div[@class="cost"]/text()').extract()
        start_times_detail = response.xpath('//div[@class="time"]/text()').extract()
        #items["description"] = description
        items['date'] = response.meta['date']
        items['start_times_detail'] = start_times_detail
        items['cost'] = cost

        yield items



