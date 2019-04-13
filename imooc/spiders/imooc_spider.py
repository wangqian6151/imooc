# -*- coding: utf-8 -*-
import re
from datetime import datetime
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from imooc.items import CourseItem, CommentItem


class ImoocSpiderSpider(scrapy.Spider):
    name = 'imooc_spider'
    allowed_domains = ['www.imooc.com']
    start_urls = ['http://www.imooc.com/course/list?c=cb/']
    base_course_url = 'https://www.imooc.com/coursescore/'

    def parse(self, response):
        course_list = response.xpath('//*[@class="course-list"]/div[@class="moco-course-list"]/div/div')
        for c in course_list:
            course_item = CourseItem()
            course_item['name'] = c.xpath('./a/div[2]/h3/text()').extract_first()
            course_item['url'] = response.urljoin(c.xpath('./a/@href').extract_first())
            course_item['id'] = course_item['url'].split('/')[-1]
            course_item['level'] = c.xpath('.//div[@class="course-card-info"]/span[1]/text()').extract_first()
            course_item['learners_num'] = c.xpath('.//div[@class="course-card-info"]/span[2]/text()').extract_first()
            course_item['label'] = '/'.join(c.xpath('.//div[@class="course-label"]/label/text()').extract())
            course_item['img'] = 'http:' + c.xpath('.//img/@data-original').extract_first()
            course_item['description'] = c.xpath('./a//p[@class="course-card-desc"]/text()').extract_first()
            # yield course_item
            yield Request(self.base_course_url + course_item['id'], callback=self.parse_course, meta={'course_item': course_item})
        if response.xpath('.//div[@class="page"]/a[last()-1]/text()').extract_first() == '下一页':
            # next_url = response.urljoin(response.xpath('.//div[@class="page"]/a[last()-1]/@href').extract_first())
            le = LinkExtractor(restrict_xpaths='//*[@class="page"]/a[last()-1]')
            link = le.extract_links(response)
            if link:
                next_url = link[0].url
                print('next_course_url:{}'.format(next_url))
                self.logger.debug('next_course_url:{}'.format(next_url))
                yield Request(next_url, callback=self.parse)

    def parse_course(self, response):
        course_item = response.meta.get('course_item')
        print('parse_course course_item:{}'.format(course_item))
        self.logger.debug('parse_course course_item:{}'.format(course_item))
        course_item['duration'] = response.xpath('//div[contains(@class,"statics")]/div[3]/span[2]/text()').extract_first()
        course_item['overall_rating'] = response.xpath('//div[contains(@class,"statics")]/div[5]/span[2]/text()').extract_first()
        course_item['comment_num'] = response.xpath('//*[@class="person-num"]/span/text()').re_first(r'[1-9]\d*|0')
        course_item['utility_rating'] = response.xpath('//*[@class="score-detail-box"]/div[1]/span[1]/text()').extract_first()
        course_item['simplicity_rating'] = response.xpath('//*[@class="score-detail-box"]/div[2]/span[1]/text()').extract_first()
        course_item['logic_rating'] = response.xpath('//*[@class="score-detail-box"]/div[3]/span[1]/text()').extract_first()
        course_item['crawl_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield course_item

        comment_url = response.xpath('//*[@class="score-box"]/a[2]/@href').extract_first()
        if comment_url:
            comment_url = response.urljoin(comment_url)
            yield Request(comment_url, callback=self.parse_comment)

    def parse_comment(self, response):
        comment_list = response.xpath('//*[@class="evaluation-list"]/div')
        url = response.url
        for c in comment_list:
            comment_item = CommentItem()
            comment_item['course_id'] = re.findall(r"\d+\.?\d*", url)[0]
            comment_item['id'] = c.xpath('@id').extract_first()
            comment_item['username'] = c.xpath('.//*[@class="username"]/text()').extract_first()
            comment_item['score'] = c.xpath('.//*[@class="star-box"]/span/text()').re_first(r'[1-9]\d*|0')
            comment_item['content'] = c.xpath('.//p[@class="content"]/text()').extract_first()
            time = c.xpath('.//*[@class="time r"]/text()').extract_first().split('：')[1]
            comment_item['time'] = datetime.now().strftime("%Y-%m-%d") if '前' in time else time
            comment_item['crawl_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield comment_item
        if response.xpath('.//div[@class="page"]/a[last()-1]/text()').extract_first() == '下一页':
            # next_url = response.urljoin(response.xpath('.//div[@class="page"]/a[last()-1]/@href').extract_first())
            le = LinkExtractor(restrict_xpaths='//*[@class="page"]/a[last()-1]')
            link = le.extract_links(response)
            if link:
                next_url = link[0].url
                print('next_comment_url:{}'.format(next_url))
                self.logger.debug('next_comment_url:{}'.format(next_url))
                yield Request(next_url, callback=self.parse_comment)
