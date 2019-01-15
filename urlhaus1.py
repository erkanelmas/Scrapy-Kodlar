import scrapy


class QuotesSpider(scrapy.Spider):
    name = "urlhaus"
    start_urls = [
        'https://urlhaus.abuse.ch/browse/page/910/',
    ]
    
    
    def parse(self, response):
        for tr in response.css('tr'):
            yield {
                'Date': tr.css('td::text').extract_first(),
                'URL': tr.css('a::text').extract_first(),
               # 'Reporter': tr.css('td a::text')[sayi+1].extract(),
               # 'Status': tr.css('span.badge.badge-danger::text')[0].extract(),
               # 'Tag': tr.css('span.badge::text')[0].extract(),
               
            }
            
            kontrol = response.css('td::text').extract_first()
        if kontrol is not None:
            next_page = response.css('li a.page-link::attr(href)')[1].extract()
            yield response.follow(next_page, callback=self.parse)
            