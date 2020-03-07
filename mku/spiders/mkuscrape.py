import scrapy
import unicodedata
from scrapy.http import FormRequest

detaillist = ['DETAIL']
unitlist = []
timetablelist = []

myUnitsList = ["REG_UNITS"]
cleanTimtable=["TIMETABLE"]

roughresultlist=[]
cleanresultlist=["RESULTS"]

finalList=[]

timetable_url = 'https://studentportal.mku.ac.ke/umis/studentportal/teaching_timetable.php'
result_url='https://studentportal.mku.ac.ke/umis/studentportal/result_slip.php'


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, user='', pasw='', *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.user = [user]
        self.pasw = [pasw]

    def start_requests(self):
        urls = [
            'https://studentportal.mku.ac.ke/umis/studentportal/course_registration.php',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # DIT/2019/48039   35647276

        return FormRequest.from_response(response,
                                         formdata={'regNo': self.user,
                                                   'smisPass': self.pasw, 'smisLogon': 'maybe'},
                                         callback=self.scrape_p)

    def scrape_p(self, response):
        try:
            self.name_box = response.xpath('//div/div/div/p/text()').extract()
            xtotal_fee = response.xpath('//tr/td/text()').extract()
            all_td = response.xpath('//td/text()').extract()
            # print(all_td)

            for i in all_td:
                try:
                    x = i.replace(u'\xa0', u'')
                    y = x.strip()
                    if y:
                        unitlist.append(y)
                    else:
                        pass
                except:
                    unitlist.append(i)

            # print(unitlist)

            p = xtotal_fee[-3].strip()
            self.Total_sem_fees = int(p.replace(",", ""))


            x=self.name_box[0].replace(u'\xa0', u'')
            detaillist.append(x)

            return scrapy.Request('https://studentportal.mku.ac.ke/umis/studentportal/statement_detailed.php', callback=self.parse_page1)

        except:
            pass

    def parse_page1(self, response):

        # get closing balance

        xclosing_balance = response.xpath('//tr/td/b/text()').extract()
        if "," in xclosing_balance[-1]:
            cj = xclosing_balance[-1].strip()
            cjj = cj.replace(",", "")
            self.closing_balance = round(float(cjj))
        else:
            x = float(xclosing_balance[-1].strip())
            self.closing_balance = round(x)
        # get paid amount and percentage

        self.paid_amount = self.Total_sem_fees-self.closing_balance
        self.paid_percent = (self.paid_amount/self.Total_sem_fees)*100

        #  append results to my list
        detaillist.extend([self.Total_sem_fees, self.paid_amount,
                       self.closing_balance, self.paid_percent])
        # print(detaillist)

        return scrapy.Request(timetable_url, callback=self.parse_anotherpage)

    def parse_anotherpage(self, response):
        all_td_forTimetable = response.xpath('//td/text()').extract()
        # print(all_td)

        for i in all_td_forTimetable:
            try:
                x = i.replace(u'\xa0', u'')
                y = x.strip()
                if y:
                    timetablelist.append(y)
                else:
                    pass
            except:
                timetablelist.append(i)

        # print(timetablelist)

        for i in timetablelist:
            if i in unitlist:
                if len(i) > 7:
                    if "Unlocking" not in i:
                        if "Course" not in i:
                            myUnitsList.append(i)

        numlist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
            'Sunday')
        for i in timetablelist:
            
            if len(i) > 7:
                if i not in days:
                    if "Unlocking" not in i and 'Dr' not in i and 'Mr' not in i and 'Course' not in i and 'the'not in i and 'Lecturer' not in i and 'Exam' not in i:
                        if i[-1] not in numlist:

                            cleanTimtable.append(i)


        # print(myUnitsList)
        # print(cleanTimtable)

        return scrapy.Request(result_url, callback=self.parse_resultpage)

    def parse_resultpage(self, response):
        all_td_forResults = response.xpath('//td/text()').extract()
        
        for i in all_td_forResults:
            try:
                x = i.replace(u'\xa0', u'')
                y = x.strip()
                if y:
                    roughresultlist.append(y)
                else:
                    pass
            except:
                roughresultlist.append(i)

        # print(roughresultlist)

        for i in roughresultlist:
            if len(i) ==7:
                x=roughresultlist.index(i)
                out=i+' '+roughresultlist[x+1]+' '+roughresultlist[x+2]+' '+roughresultlist[x+3]
                cleanresultlist.append(out)

               
        # print(cleanresultlist)

        finalList.extend([detaillist,myUnitsList,cleanTimtable,cleanresultlist])

        print(finalList)

