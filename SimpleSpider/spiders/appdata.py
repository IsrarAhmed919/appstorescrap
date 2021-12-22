import scrapy
import json


class AppdataSpider(scrapy.Spider):
    name = 'appdata'
    allowed_domains = ['apps.shopify.com']
    start_urls = ['https://apps.shopify.com/parcelpanel?surface_inter_position=3&surface_intra_position=23&surface_type=category']
    base_url="https://apps.shopify.com"
    # def get_all_reviews(self, response, link):
    #     fetch(link)
    #     reviews=response.request.url
    #     return reviews
    app_data=[]

    def clean(self, lis):
        new_lis=[]
        for i in lis:
            cleaned=i.replace("\n", "")
            cleaned=cleaned.replace("'","")
            cleaned=cleaned.replace("  ", "")
            checkflag=cleaned.replace(" ","")
            if bool(checkflag)==True:
                new_lis.append(cleaned)

        return new_lis
    #Initializing a dictionary
    data_dict = {}
    def parse(self, response, data_dict=data_dict):
        
        #names
        names=response.xpath('//*[@id="Main"]/div/div[1]/div/div[1]/h1/text()').extract()
        # name=[]
        # for i in names:
        #     n=i.replace("\n", "")
        #     name.append(n)
        name=self.clean(names)
        data_dict['Name'] = name
        #tagline
        tagline=response.xpath('//*[@id="Main"]/div/div[1]/div/div[1]/p/text()').extract()
        tagline=self.clean(tagline)
        data_dict['Tag_Line'] = tagline
        #company_name
        company_name=response.xpath('//*[@id="Main"]/div/div[1]/div/div[1]/div[2]/a/text()').extract()
        company_name=self.clean(company_name)
        data_dict['Company'] = company_name
        #company_link
        company_link=response.xpath('//*[@id="Main"]/div/div[1]/div/div[1]/div[2]/a/@href').extract()
        company_link=self.clean(company_link)
        data_dict['Company_Link'] = company_link
        #no_of_reviews
        no_of_reviews=response.xpath('//*[@id="Main"]/div/div[1]/div/div[1]/div[3]/span/span/a/text()').extract()
        no_of_reviews=self.clean(no_of_reviews)
        data_dict['Total_Reviews'] = no_of_reviews
        #main_features
        main_features=response.xpath('//*[@id="Main"]/div/div[2]/div/div/div/h4/text()').extract()
        main_features=self.clean(main_features)
        data_dict['Features'] = main_features
        #Description
        full_description=response.xpath('//*[@id="DetailsSection--Accordion--AccordionItem0"]/div/div[1]/div/div[2]/div/div[1]/div//text()').extract()
        full_description=self.clean(full_description)
        data_dict["Description"]=full_description
        #pricing
        pricings=[]
        pricing=response.xpath('//*[@id="Main"]/div/section[2]/div/div[2]/div/div')
        print(pricing)
        x=1
        for i in pricing:
            pricing_dict={}
            pr_type=i.xpath('//*[@id="Main"]/div/section[2]/div/div[2]/div/div[{}]/div/p//text()'.format(x)).getall()
            pr_type=self.clean(pr_type)
            pricing_dict["Type"]=pr_type[0]
            pr_pay=i.xpath('//*[@id="Main"]/div/section[2]/div/div[2]/div/div[{}]/div/h3//text()'.format(x)).get()
            if not type(pr_pay)==list:
                pr_pay=[pr_pay]
            pr_pay=self.clean(pr_pay)
            pricing_dict["Ammount"]=pr_pay
            pr_fea=i.xpath('//*[@id="Main"]/div/section[2]/div/div[2]/div/div[{}]/ul/li/text()'.format(x)).getall()
            pr_fea=self.clean(pr_fea)
            pricing_dict["Facilities"]=pr_fea
            pricings.append(pricing_dict)
            #print(pr_type,pr_pay,pr_fea)
            x+=1
        #pricing=self.clean(pricing)
        data_dict["Pricing"]=pricings
        #overall_ratings
        overall_ratings=response.xpath('//*[@id="reviews"]/div[2]/div[1]/div[1]/div[1]/h3/span/div/div[2]/span/text()').extract()
        overall_ratings=self.clean(overall_ratings)
        data_dict["Overall_Ratings"]=overall_ratings
        see_all_reviews=response.xpath('//*[@id="reviews"]/div[2]/div[1]/div[1]/div[2]/a/@href').extract()
        reviews_url=response.urljoin(see_all_reviews[0])
        print("In Parse Function", reviews_url)
        yield scrapy.Request(reviews_url, callback=self.get_reviews)
                
        #print(" Name: ", name, "\n", "Tagline: ", tagline,"\n", "CompanyName: ",company_name,"\n", "Company_Link: ",company_link,"\n", "Total Reviews: ",no_of_reviews,"\n", "Main Features: ", main_features,"\n", "Description: ",full_description,"\n", "Pricing: ",pricings,"\n","Overall_Ratings: ", overall_ratings,"\n", "Reviews: ", reviews)

        

        # f = open('output.json', 'w')
        # #f.write(json.dumps(all_jobs)) # all in one line
        # f.write(json.dumps(data_dict, indent=2))
        # f.close()

    reviews_list=[]
    def get_reviews(self, response, data_dict=data_dict):
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
            data_dict["Reviews"]=self.reviews_list
            f = open('OneAppData.json', 'w')
            #f.write(json.dumps(all_jobs)) # all in one line
            f.write(json.dumps(data_dict, indent=2))
            f.close()
            print("Complete Data Has Been Stored")
        
            
            
