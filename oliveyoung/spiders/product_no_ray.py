import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from oliveyoung.items import OliveyoungItem
from twisted.internet import reactor
from datetime import datetime

class ProductNoRaySpider(scrapy.Spider):
    name = "oliveyoung_no_ray"
    allowed_domains = ["www.oliveyoung.co.kr"]
    # FOR TEST: 페이지 수 제한 설정
    max_page = 2

    start_urls = [
        'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010014&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010014_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EC%97%90%EC%84%BC%EC%8A%A4%2F%EC%84%B8%EB%9F%BC%2F%EC%95%B0%ED%94%8C&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd=',
        # 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010015&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010015_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%ED%81%AC%EB%A6%BC&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd=',
        # 'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010013&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=2&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010013_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EC%8A%A4%ED%82%A8%2F%ED%86%A0%EB%84%88&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd='
    ]

    def parse(self, response):
        for products in response.xpath('//ul[@class="cate_prd_list gtm_cate_list"]'):
            for product in products.xpath('.//div[@class="prd_info "]'):
                item = OliveyoungItem()
                item['name'] = product.xpath('.//p[@class="tx_name"]/text()').get()
                item['price'] = product.xpath('.//span[@class="tx_cur"]/span[@class="tx_num"]/text()').get()
                item['brand'] = product.xpath('.//span[@class="tx_brand"]/text()').get()
                item['url'] = product.xpath('./a/@href').get()
                item['time'] = datetime.now().strftime('%m-%d %H:%M')
                yield item

        # 다음 페이지로 이동
        curr_page = response.xpath('//strong[@title="현재 페이지"]/text()').get()

        if curr_page and int(curr_page) >= self.max_page:  # FOR_TEST
            return

        next_page_url = response.xpath('//strong[@title="현재 페이지"]/following-sibling::a/@data-page-no').get()

        if next_page_url:  # 다음 페이지 없으면 None
            next_page_full_url = response.url.replace(f'pageIdx={curr_page}', f'pageIdx={next_page_url}')
            yield scrapy.Request(url=next_page_full_url, callback=self.parse)
        else:
            self.log("No more pages.")


if __name__ == "__main__":    
    start_time = datetime.now() # 시작 시간 기록
    print(f'Started at: {start_time}')

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(ProductNoRaySpider)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()

    end_time = datetime.now()  # 작업 완료 시간 기록
    print(f"작업 완료 시간: {end_time}")
    elapsed_time = end_time - start_time  # 경과 시간 계산 및 출력
    print(f"총 소요 시간: {elapsed_time}")
