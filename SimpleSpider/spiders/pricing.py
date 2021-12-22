import scrapy

class PricingSpider(scrapy.Spider):
    name = 'pricing'
    allowed_domains = ['https://apps.shopify.com/dsers?surface_inter_position=1']
    start_urls = ['https://apps.shopify.com/dsers?surface_inter_position=1/']
    

    def parse(self, response):
        pricing=response.xpath('//*[@id="Main"]/div/section[2]/div/div[2]/div/div')
        print(pricing)
        x=1
        for i in pricing:
            pr_type=i.xpath('//*[@id="Main"]/div/section[2]/div/div[2]/div/div[{}]/div/p//text()'.format(x)).getall()
            pr_pay=i.xpath('//*[@id="Main"]/div/section[2]/div/div[2]/div/div[{}]/div/h3//text()'.format(x)).get()
            pr_fea=i.xpath('//*[@id="Main"]/div/section[2]/div/div[2]/div/div[{}]/ul/li/text()'.format(x)).getall()
            print(pr_type,pr_pay,pr_fea)
            x+=1

