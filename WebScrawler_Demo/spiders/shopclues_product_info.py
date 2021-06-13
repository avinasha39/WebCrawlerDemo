import scrapy
import re
from urllib.parse import urlparse
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor


class ShopcluesProductInfoSpider(scrapy.Spider):
    name = 'shopclues_product_info'
    count = 0
    maximum_page_to_process = 100
    url_set = {""}

    def __init__(self,  **kwargs):
        super(ShopcluesProductInfoSpider,self).__init__( **kwargs)
        url = kwargs.get('url') or kwargs.get('domain')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        self.url = url
        self.allowed_domains = [re.sub(r'^www\.', '', urlparse(url).hostname)]
        self.link_extractor = LinkExtractor()
        self.cookies_seen = set()

    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]
    
    custom_settings = {
       'FEED_URI' : 'Data/ShopClues_ProductInfo.csv'
    }
    def parse(self, response):
        
        domainName = self.GetDomainName(response)
        ShopcluesProductInfoSpider.url_set.add(response.url)
        
        exclude_keyword = self.GetKeyWordsToExclude()
        
        name_selectors1 = response.css('img::attr(title)').extract()
        product_url = response.xpath("//div[contains(@class,'column col3')]/a[2]/@href").getall()
        price_selectors = response.css('.p_price::text').extract()
        cat_selectors = response.xpath("//a[contains(@itemprop, 'item')]/span/text()").getall()
        

        if(len(name_selectors1)!=0 ):
            product_name =  name_selectors1 
            cat_str = '/'.join(cat_selectors)
            for item in zip(product_name,price_selectors,product_url):
                productinfo = {
                    'Product Name' : item[0],
                    'Price' : item[1].strip(),
                    'Category' :  cat_str,
                    'URL' : domainName + item[2]            
                }
                yield productinfo     

            next_page = response.xpath("//li[contains(@class, 'a-last')]/a/@href").extract_first()
            if next_page is not None:
                next_page = domainName+ next_page
                if next_page not in ShopcluesProductInfoSpider.url_set and ShopcluesProductInfoSpider.count < ShopcluesProductInfoSpider.maximum_page_to_process:
                    ShopcluesProductInfoSpider.count = ShopcluesProductInfoSpider.count + 1
                    yield scrapy.Request(url= next_page, callback= self.parse)
                            
        
        if(len(name_selectors1)==0):
            a_selectors = response.xpath("//a")
            for selector in a_selectors:
                link = selector.xpath("@href").extract_first()            
                if(link is not None):
                    if link.startswith("https://"):
                        continue
                    if any(ext in link for ext in exclude_keyword):
                        continue
                    abs_url = domainName + link[19:]
                    if abs_url in ShopcluesProductInfoSpider.url_set:
                        continue
                    ShopcluesProductInfoSpider.count = ShopcluesProductInfoSpider.count + 1                  
                    if ShopcluesProductInfoSpider.count < ShopcluesProductInfoSpider.maximum_page_to_process:
                        yield scrapy.Request(url= abs_url, callback= self.parse)
                    else:
                        break

    def GetKeyWordsToExclude(self):
        exclude_keyword = ["header","prime","select-language","signin","order-history","cart","help","amazon-coupons","gift-card","credit-card","deal",
        "nav-top","amazon.jobs","jobs","location","accelerator","advertising","amazonpay","abebooks","audible","dpreview","imdb","shopbop","nav_logo",
        "facebook","twitter","youtube","payments","shipping","tel:1800","giveindia.org","seller.flipkart","plus","login","about-us","press","stories",
        "privacypolicy","returnpolicy","sitemap","ewaste-compliance-tnc","buying-guide","pricing","blog","pinterest","linkedin","developer","javascript:void(0)",
        "storemanager","fulfillment-by","policies-and-rules","merchant-testimonial","seller-summit","merchant-community","aboutus","shopclues-history","bandoftrust",
        "brand-guidelines","tv-commercials","awards","workwithus","buyer-protection","return-policy","vip-club","mychat","cluesbucks","policy","surety","service-centers",
        "user-agreement","refer-and-earn","learn-to-sell","pricing"]
        
        return exclude_keyword
                    
    def GetDomainName(self, response):
        parsed_uri = urlparse(response.url)
        str = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return str

