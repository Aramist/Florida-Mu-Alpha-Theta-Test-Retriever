import scrapy

class MAOSpider(scrapy.Spider):
    name = 'mao_spider'
    start_urls = [r'http://www.mualphatheta.org/index.php?chapters/national-convention/past-tests']

    def parse(self, response):
        CSS_SELECTOR = 'ul li a'
        for anchor in response.css(CSS_SELECTOR):
            yield {
                'type': anchor.css('::text').extract_first(),
                'url': anchor.css('::attr(href)').extract_first()
            }
