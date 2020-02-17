# -*- coding: utf-8 -*-
import scrapy
from weibo_spider.items import WeiboSpiderItem


class SSpiderSpider(scrapy.Spider):
    name = 's_spider'
    allowed_domains = ['s.weibo.com']
    start_urls = ['https://s.weibo.com/weibo?q=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&Refer=weibo_weibo']

    def parse(self, response):
        content_list = response.xpath("//div[@class='card-feed']")
        for item in content_list:
            weibo_item = WeiboSpiderItem()
            weibo_item['user_name'] = item.xpath(".//a[@class='name']/text()").get()
            weibo_item['weibo_content'] = ''.join(item.xpath(".//p[@node-type='feed_list_content_full']/text()").re('[\u4e00-\u9fa5]+'))
            weibo_item['reposts_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_forward']/text()").re('\d+'))
            weibo_item['comments_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_comment']/text()").re('\d+'))
            weibo_item['likes_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_like']/text()").re('\d+'))
            print(weibo_item)