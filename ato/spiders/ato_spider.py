import scrapy
from urllib.parse import quote
from scrapy.crawler import CrawlerProcess
import markdownify


class ATO(scrapy.Spider):
    name = "ato_spider"

    def start_requests(self):
        start = (self.page -1) * 10
        url = f"https://www.ato.gov.au/GSAProxy/search/?q={quote(self.query)}&site=ATOGOV_Ektron&partialfields=&requiredfields=&ms=ATO_Home&start={start}&client=ATOGOV_EKTRON&proxystylesheet=ATOGOV_FACETED&output=xml_no_dtd&getfields=*&dc_terms_identifier=DCTERMS_identifier&dc_terms_natnumber=ato_reference_natNumber&dc_terms_ato_gsa_code=ato_gsacode&gsa_searchable=&dc_terms_dc_date_filter=dc_date_filter&ato_home=ATO_Home&general_id=1006&exclude_general=146%2C210%2C1004%2C1005%2C1470%2C1829%2C1842%2C2026%2C2027%2C2040%2C2216&criteria_error_message=You%20need%20to%20enter%20a%20keyword%20for%20your%20search.&legal_nonindexed=ROBOTS%3AIndex%2520Only&legal_searchable=ROBOTS%3ANot%2520Searchable&market_segment_short=ATO_Home&market_segment=ATO_Home&market_label=ATO_Home&no_search_criteria=false&atogov_dns=https%3A%2F%2Fwww.ato.gov.au&legal_dns=http%3A%2F%2Flaw.ato.gov.au&search_tips_url=searchhelp&results_page_url=&advanced_page_url=AdvancedSearch.aspx&market_segment_list=146%2C210%2C1004%2C1005%2C1006%2C1470%2C1829%2C1842%2C2026%2C2027%2C2040%2C2216&atogov_collection=ATOGOV_Ektron&legaldb_collection=legaldb&numgm=10"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        articles = response.xpath("//li[@class='searchResult']//a/@href").getall()
        yield from response.follow_all(articles, callback=self.parse_article)

    def parse_article(self, response):
        content = markdownify.markdownify(response.xpath("//article").get())
        return {
            "ref": response.url,
            "content": content,
            "query": self.query
        }


# crawler = CrawlerProcess(settings={
#     "DEFAULT_REQUEST_HEADERS": {
#         'authority': 'www.ato.gov.au',
#         'accept': 'text/html, */*; q=0.01',
#         'accept-language': 'en-US,en;q=0.9,ur;q=0.8',
#         'referer': 'https://www.ato.gov.au/search/',
#         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
#         'x-requested-with': 'XMLHttpRequest',
#     },
#     "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
# })
# crawler.crawl(ATO)
# crawler.start()