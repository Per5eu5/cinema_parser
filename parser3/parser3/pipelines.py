# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2


class Parser3Pipeline(object):

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = '1'
        database = 'cinemas'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into solovey(title,date,start_time,dimension,hall,poster,age,cost,url)"
                         " values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                         (item['title'], item['date'], item['start_time'], item['dimension'], item['hall'], item['poster'],
                         item['age'], item['cost'], item['url']))

        self.connection.commit()
        return item


# class Parser3Pipeline(object):
#     def process_item(self, item, spider):
#         return item
