import scrapy

class MAOSpider(scrapy.Spider):
    name = 'mao_spider'
    start_urls = [r'http://www.mualphatheta.org/index.php?chapters/national-convention/past-tests']

    def parse(self, response):
        CSS_SELECTOR = 'li ul li a'
        for anchor in response.css(CSS_SELECTOR):
            yield {
            	'subject': anchor.css('::text').extract_first(),
                'type': anchor.css('a ::text').extract(),
                'url': anchor.css('a ::attr(href)').extract()
            }
