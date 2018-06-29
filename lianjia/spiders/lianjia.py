from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from lxml import etree
from lianjia.items import ZuFangItem
from lianjia.redis_op import RedisOp
from lianjia.settings import REDIS_ZU_FANG_SET


redis_op = RedisOp()

class LianjiaSpider(Spider):
    name = 'lianjia'
    start_urls = [
        "https://bj.lianjia.com/zufang/",
        "https://cd.lianjia.com/zufang/",
        "https://cq.lianjia.com/zufang/",
        "https://cs.lianjia.com/zufang/",
        "https://dl.lianjia.com/zufang/",
        "https://dg.lianjia.com/zufang/",
        "https://fs.lianjia.com/zufang/",
        "https://gz.lianjia.com/zufang/",
        "https://hz.lianjia.com/zufang/",
        "https://hui.lianjia.com/zufang/",
        # "https://hk.lianjia.com/zufang/",
        "https://hf.lianjia.com/zufang/",
        "https://jn.lianjia.com/zufang/",
        "https://lf.lianjia.com/zufang/",
        "https://nj.lianjia.com/zufang/",
        "https://qd.lianjia.com/zufang/",
        "https://sh.lianjia.com/zufang/",
        "https://sz.lianjia.com/zufang/",
        "https://su.lianjia.com/zufang/",
        "https://sjz.lianjia.com/zufang/",
        "https://sy.lianjia.com/zufang/",
        "https://tj.lianjia.com/zufang/",
        "https://wh.lianjia.com/zufang/",
        "https://wx.lianjia.com/zufang/",
        "https://xm.lianjia.com/zufang/",
        "https://xa.lianjia.com/zufang/",
        "https://yt.lianjia.com/zufang/",
        "https://zs.lianjia.com/zufang/",
        "https://zh.lianjia.com/zufang/",
        "https://zz.lianjia.com/zufang/",
    ]

    city_names = {
        "https://bj.lianjia.com/zufang/": "北京市",
        "https://cd.lianjia.com/zufang/": "成都市",
        "https://cq.lianjia.com/zufang/": "重庆市",
        "https://cs.lianjia.com/zufang/": "长沙市",
        "https://dl.lianjia.com/zufang/": "大连市",
        "https://dg.lianjia.com/zufang/": "东莞市",
        "https://fs.lianjia.com/zufang/": "佛山市",
        "https://gz.lianjia.com/zufang/": "广州市",
        "https://hz.lianjia.com/zufang/": "杭州市",
        "https://hui.lianjia.com/zufang/": "惠州市",
        # "https://hk.lianjia.com/zufang/",
        "https://hf.lianjia.com/zufang/": "合肥市",
        "https://jn.lianjia.com/zufang/": "济南市",
        "https://lf.lianjia.com/zufang/": "廊坊市",
        "https://nj.lianjia.com/zufang/": "南京市",
        "https://qd.lianjia.com/zufang/": "青岛市",
        "https://sh.lianjia.com/zufang/": "上海市",
        "https://sz.lianjia.com/zufang/": "深圳市",
        "https://su.lianjia.com/zufang/": "苏州市",
        "https://sjz.lianjia.com/zufang/": "石家庄",
        "https://sy.lianjia.com/zufang/": "沈阳市",
        "https://tj.lianjia.com/zufang/": "天津市",
        "https://wh.lianjia.com/zufang/": "武汉市",
        "https://wx.lianjia.com/zufang/": "无锡市",
        "https://xm.lianjia.com/zufang/": "厦门市",
        "https://xa.lianjia.com/zufang/": "西安市",
        "https://yt.lianjia.com/zufang/": "烟台市",
        "https://zs.lianjia.com/zufang/": "中山市",
        "https://zh.lianjia.com/zufang/": "珠海市",
        "https://zz.lianjia.com/zufang/": "郑州市",
    }

    def parse(self, response):
        if response.url == 'https://bj.lianjia.com/zufang/':
            print('--------------------------------------')
            print('开始')
        sel = Selector(response=response)
        zufang_num = sel.xpath('//div[@class="list-head clear"]//h2//span/text()').extract_first()
        if zufang_num is None:
            zufang_num = '2000'
        zufang_num = int(int(zufang_num) / 20)
        if zufang_num > 100:
            zufang_num = 100
        for i in range(zufang_num):
            yield Request(response.url + 'pg%s/' % i, callback=self.parse_loop_page)
        
    def parse_loop_page(self, response):
        sel = Selector(response=response)
        all_zufang = sel.xpath('//div[@class="list-wrap"]//li//div[@class="info-panel"]//h2//a//@href').extract()
        for url in all_zufang:
            # print(url)
            if redis_op.sismember(name=REDIS_ZU_FANG_SET, value=url):
                # print("url %s 已访问,不再访问" % url)
                continue
            yield Request(url, callback=self.parse_zufang_info_page)
    
    def parse_zufang_info_page(self, response):
        if redis_op.sismember(name=REDIS_ZU_FANG_SET, value=response.url):
            # print("url %s 已访问,不再访问" % response.url)
            return

        sel = Selector(response=response)
        item = ZuFangItem()
        city = ''
        for city_name in self.city_names:
            if city_name in response.url:
                city = self.city_names[city_name]
        item['city'] = city
        item['name'] = sel.xpath('//h1[@class="main"]/text()').extract_first().strip()
        item['url'] = response.url.strip()
        price = sel.xpath('//span[@class="total"]/text()').extract_first()
        if price is None or not price.isdigit():
            return
        price = price.strip()
        item['price'] = int(price)
        item['area'] = sel.xpath('//div[@class="zf-room"]//p[@class="lf"][1]/text()').extract_first().strip()
        item['floor'] = sel.xpath('//div[@class="zf-room"]//p[@class="lf"][3]/text()').extract_first().strip()
        item['apartments'] = sel.xpath('//div[@class="zf-room"]//p[@class="lf"][2]/text()').extract_first().strip()
        item['towards'] = sel.xpath('//div[@class="zf-room"]//p[@class="lf"][4]/text()').extract_first().strip()
        item['subway'] = sel.xpath('//div[@class="zf-room"]//p[5]/text()').extract_first().strip()
        item['microdistrict'] = sel.xpath('//div[@class="zf-room"]//p[6]//a[1]/text()').extract_first().strip()
        location = ''
        for l in sel.xpath('//div[@class="zf-room"]//p[7]//a/text()').extract():
            location = ' ' + l
        item['location'] = location.strip()
        item['broker'] = sel.xpath('//div[@class="brokerName"]//a/text()').extract_first()
        item['broker_phone'] = sel.xpath('normalize-space(//div[@class="brokerInfo"]//div[@class="phone"])').extract_first().strip()
        redis_op.sadd(name=REDIS_ZU_FANG_SET, values=response.url)
        yield item