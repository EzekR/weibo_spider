# -*- coding: utf-8 -*-
import scrapy
import redis
import json
from weibo_spider.items import WeiboSpiderItem


class SSpiderSpider(scrapy.Spider):
    name = 's_spider'
    allowed_domains = ['s.weibo.com']
    start_urls = ['https://s.weibo.com/weibo?q=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&Refer=topic_weibo']
    redis_connection = redis.Redis(host='127.0.0.1', port=6379)
    
    # 网页微博登录后获取cookies并替换
    # cookies_str = ''
    # cookies = {'WEIBOCN_FROM': '1110106030', '_T_WM': '25607401384', 'SCF': 'Ajh8ojhSprfMrRVwugCif6ehSgsR_N-6H1x5wLCPYD_II8YBnVwV28rMswFD1qlIKfY3rP7BkFFbsAGOAiirPkc.', 'SSOLoginState': '1582001918', 'MLOGIN': '1', 'XSRF-TOKEN': '9309e2', 'M_WEIBOCN_PARAMS': 'uicode%3D20000174', 'SUHB': '0ElKF5YoiiJSAV', 'SUB': '_2A25zTx6uDeRhGeNI4lsV-SfNzD2IHXVQs6LmrDV6PUJbkdAKLUnbkW1NSBnUjTqUe6gpTrv06xmBLdCZtD3SIXPN'}

    # 从redis获取由cookiespool生成的cookie
    def get_cookies_from_redis(self):
        cookies = self.redis_connection.hvals('cookies:weibo')
        print(cookies)
        return cookies

    def start_requests(self):
        url= self.start_urls[0]
        cookies = self.get_cookies_from_redis()
        return [scrapy.FormRequest(url, cookies = json.loads(cookies[0]), callback = self.parse)]

    def parse(self, response):
        content_list = response.xpath("//div[@class='card']")
        print(content_list.text)
        for item in content_list:
            weibo_item = WeiboSpiderItem()
            weibo_item['user_name'] = item.xpath(".//a[@class='name']/text()").get()
            weibo_item['weibo_content'] = ''.join(item.xpath(".//p[@node-type='feed_list_content_full']/text()").re('[\u4e00-\u9fa5]+'))
            weibo_item['reposts_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_forward']/text()").re('\d+'))
            weibo_item['comments_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_comment']/text()").re('\d+'))
            weibo_item['likes_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_like']//em/text()").re('\d+'))
            print(weibo_item)
