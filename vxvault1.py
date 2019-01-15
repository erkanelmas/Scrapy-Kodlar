import scrapy, re, csv

class QuotesSpider(scrapy.Spider):
    name = "vxvault1"
    start_urls = [
        'http://vxvault.net/ViriList.php?s=0&m=40',
    ]
    
    def parse(self, response):
        for index in response.css('tr'):
            url_list = index.css('td a::attr(href)')
            url_list1 = url_list.extract_first()
            if url_list1 is not None:
                url_list2 = response.urljoin(url_list.extract_first())
                yield scrapy.Request(url_list2, callback=self.parse2, dont_filter = True)
    
        next_url = response.css('div#selector a::attr(href)')[2].extract()
        end_url = response.css('div#selector a::attr(href)')[3].extract()
        if next_url is not end_url:
            next_page = response.css('div#selector a::attr(href)')[2].extract()
            yield response.follow(next_page, callback=self.parse) 
    
    
    def parse2(self, response):
        with open('test.csv', mode='a', newline='') as test:
            temp_writer = csv.writer(test)
            
            line = response.css('div').extract_first()
            file = re.search(r'(File:</b>).(.*)(<br>)', line)
            size = re.search(r'(Size:</b>).(.*)(<br>)', line)
            md5 = re.search(r'(MD5:</b>).(.*)(<br>)', line)
            link = re.search(r'(Link:</b>).(.*)(<br>)', line)
            ip = re.search(r'(IP:</b>).(.*)(<br>)', line)
            added = re.search(r'(Added:</b>).(.*)(<br>)', line)
            
            if file and size and md5 and link and ip and added:
                temp_writer.writerow([ip.group(2), link.group(2), file.group(2), size.group(2), md5.group(2),  added.group(2)])
                