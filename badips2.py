import scrapy, csv, re


class QuotesSpider(scrapy.Spider):
    name = "badips2"
    start_urls = [ 'https://www.badips.com/info/20794' ]
    
    
    def parse(self, response):
        for ip_url in response.css('a.badips::attr(href)'):
            list_a = response.urljoin(ip_url.extract())
            list2_a = list_a.strip("\n")
            if list2_a is not None:
                yield scrapy.Request(list2_a, callback=self.parse2, dont_filter = True)  
            
        kontrol = response.css('a.badips::text')[1].re(r'next page')
        if kontrol is not None:
            next_page = response.css('a.badips::attr(href)')[-1].extract()
            yield response.follow(next_page, callback=self.parse) 
            
    def parse2(self, response):
        with open('badips_file.csv', mode='a', newline='') as badips_file:
            temp_writer = csv.writer(badips_file)
            
            badips = response.css('h2').extract_first()
            IP = re.search(r'(whois of )([0-9]+.[0-9]+.[0-9]+.[0-9]+)', badips)
            
            Category = response.css('tr td p.badipstable a.badips::text').extract_first()
            
            Time = response.css('tr td p.badipstable::text').extract_first()
            
            temp_writer.writerow([IP.group(2), Category, Time])
        
            
      