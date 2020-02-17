# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 关键词/TAG
    keyword = scrapy.Field()

    # 用户类型(大V/蓝V/普通用户/会员)
    user_identity = scrapy.Field()

    # 用户名
    user_name = scrapy.Field()

    # 微博内容
    weibo_content = scrapy.Field()

    # 评论数
    comments_count = scrapy.Field()

    # 转发数
    reposts_count = scrapy.Field()

    # 点赞数
    likes_count = scrapy.Field()

    # 微博日期
    date = scrapy.Field()

    pass
