import scrapy
import re

class SchoolinfoSpider(scrapy.Spider):
    name = 'schoolinfo'
    allowed_domains = ['www.minkou.jp']
    pages_number = 23
    start_urls = []
    for i in range(1,pages_number+1):
        start_urls.append('https://www.minkou.jp/hischool/search/page='+str(i)+'/pref=tokyo/')

    def parse(self, response):
        for href in response.css('#container > #contents > #main > #under > div.mod-listSearch > ul > li > a::attr(href)'):
            schoolId = href.get().replace("/hischool/school/","").replace("interview/","")
            url = 'https://www.minkou.jp/hischool/school/university/' + re.sub('/\d{2,}',"/",schoolId)
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        university = []
        for row in response.css('#main > div.sch-detail-main-box > div.sch-detail-goukakujisseki > table > tr'):
            univ = row.css('td.goukakujisseki-school > a::text').get()
            if univ:
                pass2021 = "0" if row.css('td:nth-child(4)::text').get().replace(" ","").replace("人","").strip() in ["-",""] else row.css('td:nth-child(4)::text').get().replace(" ","").replace("人","").strip()
                pass2020 = "0" if row.css('td:nth-child(5)::text').get().replace(" ","").replace("人","") in ["-",""] else row.css('td:nth-child(5)::text').get().replace(" ","").replace("人","")
                pass2019 = "0" if row.css('td:nth-child(6)::text').get().replace(" ","").replace("人","") in ["-",""] else row.css('td:nth-child(6)::text').get().replace(" ","").replace("人","")
                university.append([univ,pass2019,pass2020,pass2021])
        yield {
            'highschool':response.css('#container > #contents > #main > div.mod-school > div.mod-school-inner > div.mod-school-r > div.mod-school-top > div.mod-school-name::text').get(),
            'schoolcaption':response.css('#container > #contents > #main > div.mod-school > div.mod-school-inner > div.mod-school-r > div.mod-school-top > div.mod-school-caption::text').get().replace("(","").replace(")",""),
            'hensa':response.css('#container > #contents > #main > div.mod-school > div.mod-school-inner > div.mod-school-r > div.mod-school-bottom > div.mod-school-info > p > span::text').get(),
            'achievement':university,
        }