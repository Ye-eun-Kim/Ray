import scrapy


class ProductSpider(scrapy.Spider):
    name = "product"

    def start_requests(self):
        urls = [
            'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010015&isLoginCnt=2&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010015_MID&trackingCd=Cat100000100010015_MID&t_page=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EA%B4%80&t_click=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EC%83%81%EC%84%B8_%EC%A4%91%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_2nd_category_type=%EC%A4%91_%ED%81%AC%EB%A6%BC',
            'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010016&isLoginCnt=3&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010016_MID&trackingCd=Cat100000100010016_MID&t_page=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EA%B4%80&t_click=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EC%83%81%EC%84%B8_%EC%A4%91%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_2nd_category_type=%EC%A4%91_%EB%A1%9C%EC%85%98',
            'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010013&isLoginCnt=4&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010013_MID&trackingCd=Cat100000100010013_MID&t_page=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EA%B4%80&t_click=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EC%83%81%EC%84%B8_%EC%A4%91%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_2nd_category_type=%EC%A4%91_%EC%8A%A4%ED%82%A8%2F%ED%86%A0%EB%84%88'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("_")[-1]
        filename = 'product-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
