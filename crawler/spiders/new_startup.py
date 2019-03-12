import scrapy
import re
from googletrans import Translator
from crawler.items import NewItem

translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])

class ExampleSpider(scrapy.Spider):
    name = "newStartup"
    allowed_domains = ["startupranking.com"]
    start_urls = [
        'https://www.startupranking.com/startup/new',
    ]
    
    def parse(self, response):
        '''
        for company in response.css('tbody > tr'):
            item = NewItem()
            item['company'] = response.css("div.name > a::text").extract_first()
            item['description'] = response.css("td.tleft::text").extract_first()
            item['country'] = response.css("td > a::attr('href')").extract_first()
            
            yield item
        '''
        company = response.css("tbody > tr > td > div.name > a::text").extract()
        description = response.css("tbody > tr > td.description::text").extract()
        #translations = translator.translate(description, src='en', dest='ko')
        #print(translations.text)
        country = response.css("td > a::attr('href')").extract()
        
        for item in zip(company, description, country):
            scraped_info = {
                    'company' : item[0].strip(),
                    'description' : re.sub(' +',' ', item[1].replace('\n',' ').strip()),
                    'country' : item[2].strip()
            }
            yield scraped_info
