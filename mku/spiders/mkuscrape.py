import scrapy
from scrapy.http import FormRequest

mylist=[]
class QuotesSpider(scrapy.Spider):
        name = "quotes"
        def __init__(self, user='',pasw='', *args, **kwargs):
            super(QuotesSpider, self).__init__(*args, **kwargs)
            self.user = [user]
            self.pasw=[pasw]
            

        def start_requests(self):
            urls = [
                'https://studentportal.mku.ac.ke/umis/studentportal/course_registration.php',
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
                
        def parse(self, response):
    # DIT/2019/48039   35647276
            
            return FormRequest.from_response(response,
                            formdata={'regNo':self.user,
                                        'smisPass':self.pasw,'smisLogon':'maybe'},
                            callback=self.scrape_p)

        def scrape_p(self,response):
            self.name_box = response.xpath('//div/div/div/p/text()').extract()
            xtotal_fee = response.xpath('//tr/td/text()').extract()

            p=xtotal_fee[-3].strip()
            self.Total_sem_fees=int(p.replace(",",""))

            mylist.append(self.name_box[0])

            return scrapy.Request('https://studentportal.mku.ac.ke/umis/studentportal/statement_detailed.php', callback = self.parse_page1)

        def parse_page1(self, response): 

            # get closing balance

            xclosing_balance=response.xpath('//tr/td/b/text()').extract()
            if "," in xclosing_balance[-1]:
                cj=xclosing_balance[-1].strip()
                cjj=cj.replace(",","")
                self.closing_balance=round(float(cjj))
            else:
                x=float(xclosing_balance[-1].strip())
                self.closing_balance=round(x)
            # get paid amount and percentage
            
            self.paid_amount=self.Total_sem_fees-self.closing_balance
            self.paid_percent=(self.paid_amount/self.Total_sem_fees)*100
            
            #  append results to my list
            mylist.extend([self.Total_sem_fees,self.paid_amount,self.closing_balance,self.paid_percent])
            lis=['Student Info','Total sem fees','paid amount','closing balance','paidPercent']
            zipbObj = zip(lis, mylist)
            dictObj=dict(zipbObj)
            print(dictObj)
