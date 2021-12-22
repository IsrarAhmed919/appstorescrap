import scrapy
import json

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['apps.shopify.com']
    start_urls = ['https://apps.shopify.com/parcelpanel?surface_inter_position=3&surface_intra_position=23&surface_type=category']
    starting_url='https://apps.shopify.com/parcelpanel?surface_inter_position=3&surface_intra_position=23&surface_type=category'
    base_url="https://apps.shopify.com"

    

    check_flag=0

    def parse(self, response):
        if self.check_flag==0:
            see_all_reviews=response.xpath('//*[@id="reviews"]/div[2]/div[1]/div[1]/div[2]/a/@href').extract_first()
            reviews_url=response.urljoin(see_all_reviews)
            print("In Parse Function", reviews_url)
            yield scrapy.Request(reviews_url, callback=self.get_reviews)
        else:
            print("End")
    reviews_list=[]
    def get_reviews(self, response):
        revs=response.xpath('//*[@id="reviews"]/div[2]/div[2]/div[@class="review-listing "]')
        print(len(revs))
        x=0
        
        for i in range(2, len(revs)+2):
            r_dict={}
            name=revs[x].xpath('//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[1]/div[1]/h3//text()'.format(i)).get()
            r_dict["Store_Name"]=name
            ratings=revs[x].xpath('//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[1]/div[2]/div[1]/div[2]/div/div[2]/span/text()'.format(i)).get()
            r_dict["Ratings"]=ratings
            post_date=revs[x].xpath('//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[1]/div[2]/div[2]/div[2]//text()'.format(i)).get()
            r_dict["Post_Date"]=post_date
            review_content=revs[x].xpath('//*[@id="reviews"]/div[2]/div[2]/div[{}]/div[1]/div[3]/div/p/text()'.format(i)).get()
            r_dict["Review"]=review_content
            self.reviews_list.append(r_dict)
            print(name, ratings, post_date, review_content)
            x += 1
        next_pg=response.xpath('//*[@id="reviews"]/div[2]/div[2]/div[13]/*[@class="search-pagination__next-page-text"]/@href').get()
        print(next_pg)
        if next_pg:
            n_url=response.urljoin(next_pg)
            yield scrapy.Request(n_url, callback=self.get_reviews)
        else:
            f = open('reviews.json', 'w')
            #f.write(json.dumps(all_jobs)) # all in one line
            f.write(json.dumps(self.reviews_list, indent=2))
            f.close()
            print("End")
            self.check_flag=1
            yield scrapy.Request(self.starting_url, callback=self.parse)

         