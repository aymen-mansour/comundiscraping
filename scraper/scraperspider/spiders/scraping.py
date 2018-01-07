# -*- coding: utf-8 -*-


import re
import scrapy



class Spidercomundi(scrapy.Spider):
    #name spider
    name = 'comundi'
    #host
    comundihost = 'http://www.comundi.fr'
    #allowed domains
    allowed_domains = ['comundi.fr']
    #starting url scraping
    start_urls = [comundihost]
    #output csv file
    custom_settings = {'FEED_URI' : 'output/parsed_comundi.csv'}
    
    #parse_init
    def parse(self, response):
        comundihost = self.start_urls[0]
        #remove namespaces
        response.selector.remove_namespaces()
        #extract  domaines_formations
        domainehref = response.xpath("//a[@class='btn btn-tag']/@href").extract()
        for item in zip(domainehref):
            urlformationhref = comundihost+item[0]
            yield scrapy.Request(url=urlformationhref, callback=self.step0)
    
    #extract  sous_domaines_formations
    def step0(self, response):
        comundihost = self.start_urls[0]
        #remove xml namespaces
        response.selector.remove_namespaces()
        #xpath extract sous_domaines_formations
        doc = response.xpath("//div[@class='panel panel-default']/a/@href").extract()
        for item in doc:
            sdomaineformation = comundihost+item
            yield scrapy.Request(url=sdomaineformation, callback=self.step1)

    #extract  pagination1_formation:name,htmlcontentsku,formationhref
    def step1(self, response):
        #Extract sku from htmlcontentsku
        def sxtractsku(item):
            itemstr = str(item)
            ma = re.search(r"Ref\s(?P<ref>.{1,4})", itemstr)
            sku = ma.group("ref")
            return sku
        comundihost = self.start_urls[0]
        name = response.xpath("//a[@class='category-list-item']//h2/text()").extract()
        htmlcontentsku = response.xpath("//a[@data-formation-detail]/abbr/text()")
        formationhref = response.xpath("//a[@class='category-list-item']/@href").extract()
        for item in zip(name, htmlcontentsku, formationhref):
            sku = sxtractsku(item[1])
            urlformationhref = comundihost+item[2]
            yield scrapy.Request(url=urlformationhref, callback=self.step2,
                                 meta={'name':item[0], 'sku':sku, 'url':urlformationhref})            
   
    #extract  pagination2_formation:objectives,parsed_duration,parsed_price
    def step2(self, response):
        url = response.meta['url']
        name = response.meta['name']
        sku = response.meta['sku']
        objectives = response.xpath("//div[@id='objectifs']//ul").extract()
        parsed_duration = response.xpath("//th[@scope='row']/text()").extract_first()
        parsed_price = response.xpath("//ins/text()").extract()  
        scraped_info = {'url':url, 'name':name, 'sku':sku,
                        'parsed_duration':parsed_duration,
                        'parsed_price':parsed_price, 'objectives':objectives}    
        yield scraped_info
