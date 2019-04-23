import scrapy

class demo(scrapy.Spider):
    name = 'demo'
    start_urls  = ['http://lab.scrapyd.cn']
    def parse(self, response):
        demoslider = response.css('div.quote')
        allText = []
        for v in demoslider:
            text = v.css('.text::text').extract_first()
            author = v.css('.author::text').extract_first()
            tags = v.css('.tags .tag::text').extract()
            tags = ','.join(tags)
            allText += text + '\n' + '作者：' + author + ' 标签：' + tags + '\n'

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        filename = 'allText.txt'
        f = open(filename, 'a+')
        f.write(allText)
        f.close()