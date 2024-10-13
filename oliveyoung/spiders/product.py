import scrapy
from scrapy.crawler import CrawlerProcess
# TODO: 스크립트 실행하려고 CrawlerProcess 쓰는 중인데 스크립트로 실행시키면 ModuleNotFoundError 발생. 패키지로 인식 안 함.
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
from oliveyoung.items import OliveyoungItem


class ProductSpider(scrapy.Spider):
    name = "oliveyoung"
    allowed_domains = ["www.oliveyoung.co.kr"]

    def start_requests(self):
        # 올리브영 에센스/세럼/앰플군
        urls = [
            'https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010014&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=48&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100010014_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EC%97%90%EC%84%BC%EC%8A%A4%2F%EC%84%B8%EB%9F%BC%2F%EC%95%B0%ED%94%8C&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd='
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for products in response.xpath('//ul[@class="cate_prd_list gtm_cate_list"]'):
            for product in products.xpath('.//div[@class="prd_info "]'):
                # item = OliveyoungItem()
                #
                # item['name'] = product.xpath('.//p[@class="tx_name"]/text()').get()
                # item['price'] = product.xpath('.//span[@class="tx_cur"]/span[@class="tx_num"]/text()').get()
                # item['brand'] = product.xpath('.//span[@class="tx_brand"]/text()').get()
                # item['url'] = product.xpath('./a/@href').get()
                #
                # yield item
                loader = ItemLoader(item=OliveyoungItem(), selector=product)
                loader.add_xpath('name', './/p[@class="tx_name"]/text()')
                loader.add_xpath('price', './/span[@class="tx_cur"]/span[@class="tx_num"]/text()')
                loader.add_xpath('brand', './/span[@class="tx_brand"]/text()')
                loader.add_xpath('url', './a/@href')
                yield loader.load_item()

        # 다음 페이지로 이동
        curr_page = response.xpath('//strong[@title="현재 페이지"]/text()').get()
        next_page_url = response.xpath('//strong[@title="현재 페이지"]/following-sibling::a/@data-page-no').get()

        # 다음 페이지 없으면 None
        if next_page_url:
            next_page_full_url = response.url.replace(f'pageIdx={curr_page}', f'pageIdx={next_page_url}')
            yield scrapy.Request(url=next_page_full_url, callback=self.parse)
        else:
            self.log("No more pages.")


if __name__ == "__main__":
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(ProductSpider)
    process.start()
