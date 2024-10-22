import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from scrapy.loader import ItemLoader # item loader 사용을 포기했다. 개별 요소를 array로 저장하는 문제를 해결하기 위해
# items.py에서 TakeFirst, Join 등을 활용해봤지만 전혀 효과가 없었다. 그래서 그냥 포기하는 게 빠르다는 의견에 동의함.
from oliveyoung.items import OliveyoungItem


class ProductSpider(scrapy.Spider):
    name = "oliveyoung"
    allowed_domains = ["www.oliveyoung.co.kr"]
    # # 페이지 수 제한 설정
    # max_page = 3
    # current_page = 1

    def start_requests(self):
        # 올리브영 에센스/세럼/앰플군
        urls = [
            'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010014&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010014_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EC%97%90%EC%84%BC%EC%8A%A4%2F%EC%84%B8%EB%9F%BC%2F%EC%95%B0%ED%94%8C&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd=',
            'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010015&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010015_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%ED%81%AC%EB%A6%BC&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd=',
            'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010013&isLoginCnt=2&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010013_MID&trackingCd=Cat100000100010013_MID&t_page=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EA%B4%80&t_click=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EC%83%81%EC%84%B8_%EC%A4%91%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&t_2nd_category_type=%EC%A4%91_%EC%8A%A4%ED%82%A8%2F%ED%86%A0%EB%84%88'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for products in response.xpath('//ul[@class="cate_prd_list gtm_cate_list"]'):
            for product in products.xpath('.//div[@class="prd_info "]'):
                item = OliveyoungItem()
                item['name'] = product.xpath('.//p[@class="tx_name"]/text()').get()
                item['price'] = product.xpath('.//span[@class="tx_cur"]/span[@class="tx_num"]/text()').get()
                item['brand'] = product.xpath('.//span[@class="tx_brand"]/text()').get()
                item['url'] = product.xpath('./a/@href').get()
                yield item

        # 다음 페이지로 이동
        curr_page = response.xpath('//strong[@title="현재 페이지"]/text()').get()
        if curr_page == 3:
            exit()
        next_page_url = response.xpath('//strong[@title="현재 페이지"]/following-sibling::a/@data-page-no').get()

        # 다음 페이지 없으면 None
        if next_page_url:
            next_page_full_url = response.url.replace(f'pageIdx={curr_page}', f'pageIdx={next_page_url}')
            yield scrapy.Request(url=next_page_full_url, callback=self.parse)
        else:
            self.log("No more pages.")


    # def practice(self, response):
    #     for products in response.xpath('//ul[@class="cate_prd_list gtm_cate_list"]'):
    #         for product in products.xpath('.//div[@class="prd_info "]'):
    #             item = OliveyoungItem()
    #             item['name'] = product.xpath('.//p[@class="tx_name"]/text()').get()
    #             item['price'] = product.xpath('.//span[@class="tx_cur"]/span[@class="tx_num"]/text()').get()
    #             item['brand'] = product.xpath('.//span[@class="tx_brand"]/text()').get()
    #             item['url'] = product.xpath('./a/@href').get()
    #             yield item
    #     # 현재 페이지 수가 최대 페이지 수보다 작을 때만 다음 페이지로 이동
    #     if self.current_page < self.max_page:
    #         self.current_page += 1
    #         next_page_url = response.xpath('//strong[@title="현재 페이지"]/following-sibling::a/@data-page-no').get()
    #
    #         if next_page_url:
    #             next_page_full_url = response.url.replace(f'pageIdx={self.current_page - 1}',
    #                                                       f'pageIdx={self.current_page}')
    #             yield scrapy.Request(url=next_page_full_url, callback=self.parse)
    #         else:
    #             self.log("No more pages.")
    #     else:
    #         self.log("Reached max page limit. Stopping.")


if __name__ == "__main__":
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(ProductSpider)
    process.start()
