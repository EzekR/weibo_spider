# -*- coding: utf-8 -*-
import scrapy
import redis
import json
from weibo_spider.items import WeiboSpiderItem
from weibo_spider.spiders.get_cookies import GetCookie
from pathlib import Path
import os

class SSpiderSpider(scrapy.Spider):
    name = 's_spider'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['https://s.weibo.com/weibo/%25E7%2597%2585%25E6%25AF%2592?topnav=1&wvr=6&b=1']
    redis_connection = redis.Redis(host='127.0.0.1', port=6379)
    
    # 网页微博登录后获取cookies并替换
    # cookies_str = ''
    cookies = 'SINAGLOBAL=8487031505947.978.1579270889878; UOR=www.iqiyi.com,widget.weibo.com,login.sina.com.cn; wb_view_log=1680*10502; un=971640625@qq.com; wvr=6; wb_view_log_2192411200=1680*10502; Ugrow-G0=1ac418838b431e81ff2d99457147068c; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhOLz1SCzqpW9E0Rd3UdZVs5JpX5KMhUgL.Fozp1KzXeK2Eeh52dJLoI0YLxKqL1KnLB-qLxK.L1KzLBKqLxKML1hzLBo.LxKBLBonL12BLxKqL1KnLB-qLxKMLBK2LB-eLxKML1hzLBo.t; ALF=1613919412; SSOLoginState=1582383413; SCF=AvTgBgYggK293VebdtLE8S3ESHQHmVX3AffiV1G0abAVfPCegWzRByxeHxKgpEHV-whEEs97rKTRlaaR9sZ7sIU.; SUB=_2A25zVTFmDeRhGeRP4lAV8S_OyzyIHXVQIyWurDV8PUNbmtAfLWHWkW9NU-_4Cmc8I_NEdOAX0m0ugOtzuY8Csu9j; SUHB=0TPUOA8Z4iqU36; YF-V5-G0=3751b8b40efecee990eab49e8d3b3354; _s_tentry=login.sina.com.cn; Apache=5245110694653.634.1582383416591; ULV=1582383416619:6:4:4:5245110694653.634.1582383416591:1582255869779; YF-Page-G0=44cd1a20bfa82176cbec01176361dd13|1582383416|1582383416; webim_unReadCount=%7B%22time%22%3A1582383419128%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'

    def parse_cookie(self):
        cookie_map = {}
        for item in self.cookies.split('; '):
            cookie_map[item.split('=')[0]] = item.split('=')[1]
        return cookie_map
        
    # 从redis获取由cookiespool生成的cookie
    def get_cookies_from_redis(self):
        cookies = self.redis_connection.hvals('cookies:weibo')
        print(cookies)
        return cookies

    def get_cookies_now(self):
        cookies = GetCookie().simulator()
        print(cookies)
        return cookies

    def start_requests(self):
        url= self.start_urls[0]
        cookies = self.parse_cookie()
        # cookies = self.get_cookies_now()
        return [scrapy.FormRequest(url, callback = self.parse, cookies=cookies)]

    def parse(self, response):
        print(response.text)
        content_list = response.xpath("//div[@class='card']")
        for item in content_list:
            weibo_item = WeiboSpiderItem()
            weibo_item['user_name'] = item.xpath(".//a[@class='name']/text()").get()
            weibo_item['weibo_content'] = ''.join(item.xpath(".//p[@node-type='feed_list_content_full']/text()").re('[\u4e00-\u9fa5]+'))
            weibo_item['reposts_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_forward']/text()").re('\d+'))
            weibo_item['comments_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_comment']/text()").re('\d+'))
            weibo_item['likes_count'] = ''.join(item.xpath(".//a[@action-type='feed_list_like']//em/text()").re('\d+'))
            print(weibo_item)
