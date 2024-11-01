import ray
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from oliveyoung.items import OliveyoungItem
from datetime import datetime


@ray.remote
def run_spider(start_url):
    from twisted.internet import reactor
    settings = get_project_settings()
    settings.set('SPIDER_MODULES', ["oliveyoung.spiders.product_no_ray.py"], priority='cmdline')
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(ProductRaySpider, start_url=start_url)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()

class ProductRaySpider(scrapy.Spider):
    name = "oliveyoung_ray"
    allowed_domains = ["www.oliveyoung.co.kr"]

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []
        # FOR TEST: 페이지 수 제한 설정
        self.max_page = 3

    def parse(self, response):
        for products in response.xpath('//ul[@class="cate_prd_list gtm_cate_list"]'):
            for product in products.xpath('.//div[@class="prd_info "]'):
                item = OliveyoungItem()
                item['brand'] = product.xpath('.//span[@class="tx_brand"]/text()').get().strip()
                item['name'] = product.xpath('.//p[@class="tx_name"]/text()').get().strip()
                item['price'] = product.xpath('.//span[@class="tx_cur"]/span[@class="tx_num"]/text()').get().strip()
                item['url'] = product.xpath('./a/@href').get()
                item['time'] = datetime.now().strftime('%m-%d %H:%M')
                yield item

        # 다음 페이지로 이동
        curr_page = response.xpath('//strong[@title="현재 페이지"]/text()').get()

        if curr_page and int(curr_page) >= self.max_page: # FOR_TEST
            return

        next_page_url = response.xpath('//strong[@title="현재 페이지"]/following-sibling::a/@data-page-no').get()

        if next_page_url: # 다음 페이지 없으면 None
            next_page_full_url = response.url.replace(f'pageIdx={curr_page}', f'pageIdx={next_page_url}')
            yield scrapy.Request(url=next_page_full_url, callback=self.parse)
        else:
            self.log("No more pages.")


if __name__ == "__main__":
    print(0)
    ray.init()
    print(1)

    start_time = datetime.now() # 시작 시간 기록
    print(f'Started at: {start_time}')

    # 에센스/세럼/앰플, 크림, 스킨/토너 순
    start_urls = [
        'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010014&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010014_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EC%97%90%EC%84%BC%EC%8A%A4%2F%EC%84%B8%EB%9F%BC%2F%EC%95%B0%ED%94%8C&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd=',
        'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010015&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010015_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%ED%81%AC%EB%A6%BC&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd=',
        'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010013&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=2&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010013_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EC%8A%A4%ED%82%A8%2F%ED%86%A0%EB%84%88&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd='
    ]

    # Ray에서 remote 함수를 호출하면 ObjectRef라는 미래 객체(future)가 반환된다. 이는 실제 결과가 아니라 결과를 참조할 수 있는 핸들이다.
    # remote를 호출하면 해당 작업은 원격 프로세스나 노드에서 실행되며, 비동기적으로 실행된다.
    futures = [run_spider.remote(url) for url in start_urls]
    # ray.get()은 모든 작업이 완료될 때까지 기다린 후 결과를 반환한다. 결과 자체보다는 작업 완료를 기다리는 느낌에 가깝다.
    ray.get(futures)

    end_time = datetime.now() # 작업 완료 시간 기록
    print(f"작업 완료 시간: {end_time}")
    elapsed_time = end_time - start_time # 경과 시간 계산 및 출력
    print(f"총 소요 시간: {elapsed_time}")

    ray.shutdown()
