from selenium import webdriver      
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import psutil
import os
from lxml import etree
from lxml import html
import urllib.request, http.cookiejar
import http
import urllib
import datetime
import re

WEBDRIVER_PATH = "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"

def run_vpn_and_chromedriver(chromedriver=False):
    
    program_directory = [
        "C:\\Program Files\Private Internet Access\pia-client.exe",
        "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"]
    program_name = ["VPN","CHROMEDRIVER"]
    if chromedriver == True:
        program_list = ["pia-client.exe","chromedriver.exe"]
    if chromedriver == False:
        program_list = ["pia-client.exe"]
    
    ct = -1
    for program in program_list:
        ct += 1
        wait_seconds = 10
        process_list = [p.name() for p in psutil.process_iter()]
        print("checking if VPN is running:")
        print("---------------------------"*5)
        if program not in process_list:
            print(f"...{program_name[ct]} not running...")
            print(f"...starting {program}...")
            os.startfile(program_directory[ct])
            print(f"...waiting for program {program_name[ct]} to start before scraping...")
            time.sleep(wait_seconds)
            process_list = [p.name() for p in psutil.process_iter()]
            if program in process_list:
                if "pia" in program:
                    print("...vpn has started. now activating private IP address...")
                    print(f"...waiting for {wait_seconds} seconds vpn to activate private IP addess...")
                    time.sleep(wait_seconds)
                    print("...wait complete!")
            if "pia" in program:
                print("error")
            else:
                pass
        else:
            print(f"...{program_name[ct]} running!")
def get_selenium_driver(minimize=True):
    """
    returns webdriver so selenium can be implemented more easily
    """
    webdriver_path = WEBDRIVER_PATH
    service = Service(executable_path=webdriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(service=service, options=options)    
    if minimize == True:
        driver.minimize_window()
    return driver

class GrabArticlesAndArticleContent():
    def __init__(self):
        # inputs
        # self.layers = []
        # self.descendant_tags = []
        # self.class_txts = []
        self.main_url = ""
        # self.if_article_conditions = []
        self.content_type =['politic','opinion','border']
        # outputs
        self.reject_urls = []
        self.articles_urls = []
        self.para_list = []
        # internals
        self.grab_articles = True
        self.if_state_idx = 0
        self.additional_unwanted = []


    def scroll_click_load_more(self,driver,xpath_input_dict):
        # driver = get_selenium_driver(minimize=False)
        # try:
        #     driver.get("NEWS.COM")
        # except Exception as error:
        #     print("errorR:: ",error)

        ct = 0
        while ct <= 5:
            driver.execute_script("arguments[0].scrollIntoView();",driver.find_element(By.XPATH,".//descendant::div[@class='item load-more']/a"))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ".//descendant::div[@class='item load-more']/a"))).click()
            time.sleep(2)
            ct+= 1

    def grab_menu_url_links(self,the_url):
        headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'
                    } 
        REGEX = RegexThatURLOhYeah()
        request = urllib.request.Request(the_url,headers=headers)  
        opener = urllib.request.build_opener()
        time.sleep(2)
        filtered_html = etree.HTML(opener.open(request).read())
        texts = filtered_html.xpath('//header')
        href_links=[]
        # ct=1
        for text in texts:
            href_link = text.xpath('.//a/@href')
            signsin = ["sign-in","sign-up"]
            for h in href_link:
                if((".com" in h)
                    and("www" in h)
                    and(h not in str for str in signsin)
                    # and(h == h.startswith(the_url))
                    and(h != the_url)
                    and(self.clipped_url == REGEX.extract_domain_name(h))
                    and(h in str for str in self.content_type)
                    and(h not in href_links)):
                    # if ct <= 3:
                            # print(h)
                            href_links.append(h)
        return href_links

    def feed_mainpage_info(self,xpath_input_dict):    

        """     
        takes the following dictionary as input:
        xpath_input_dict** = {
    
                                descendant_tags:["article_tag","para_tag"],

                                class_txts:["article_txt","para_txt"],

                                layers:["article_layer","para_layer"],

                                descendant_tags:["article_desc_tag","para_desc_tag"],

                                main_url:"mainurl.com",
                                
                                if_states:['(if and if and if)','(if and if and if)'] # takes string form of if statements. leave second list as '' if you have no conditions for the paragraphs.
                            
                            }
        """
        REGEX = RegexThatURLOhYeah()
        GRAB = GrabArticlesAndArticleContent()
        self.layers = xpath_input_dict['layers']
        self.descendant_tags = xpath_input_dict['descendant_tags']
        self.class_txts = xpath_input_dict['class_txts']
        self.main_url = xpath_input_dict['main_url']
        self.if_states = xpath_input_dict['if_states']
        self.clipped_url = REGEX.extract_domain_name(self.main_url)

        additional_unwanted = self.additional_unwanted
        url_list = []
        articles = []
        if self.grab_articles == False:
            url_list = self.articles_urls
        if self.grab_articles == True:
            url_list = GRAB.grab_menu_url_links(the_url=self.main_url)
        url_list = url_list[0:15]
        inner_href_links = []
        for the_url in url_list:
            if self.grab_articles == True:
                    try:
                        if self.grab_articles == True:
                            headers = {
                                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                                            'Accept-Encoding': 'none',
                                            'Accept-Language': 'en-US,en;q=0.8',
                                            'Connection': 'keep-alive'
                                        } 
                            
                            clipped_url = REGEX.extract_domain_name(the_url)
                            request = urllib.request.Request(the_url,headers=headers)  
                            opener = urllib.request.build_opener()
                            time.sleep(2)
                            filtered_html = etree.HTML(opener.open(request).read())
                            texts = filtered_html.xpath('//body')
                            
                            
                            inner_href_links = [] 
                            for text in texts:
                                href_link = text.xpath('.//a/@href')
                                unwanted = ["sign-in","sign-up","/contact/","/terms/","/privacy/","liveblog","/writers/"]
                                unwanted = unwanted + additional_unwanted
                                for h in href_link:
                                    if((".com" in h)
                                    and("www" in h)test
                                    # and(h not in str for str in unwanted)
                                    and(h.count("/") >=3)
                                    and((REGEX.unwanted_from_links(href=h,unwanted=unwanted)==True))
                                    and(h != the_url)
                                    and(clipped_url == REGEX.extract_domain_name(h))
                                    # and(h in str for str in content_type)
                                    and(h not in inner_href_links)
                                    and(h not in url_list)):
                                        print(h)
                                        inner_href_links.append(h)
                                    elif((".com" not in h)
                                    and("www" not in h)
                                    and(h.count("/") >=3)
                                    and((REGEX.unwanted_from_links(href=h,unwanted=unwanted)==True))
                                    and(h != the_url)
                                    # and(h in str for str in content_type)
                                    and(h not in inner_href_links)
                                    and(h not in url_list)):
                                        print(h)
                                        inner_href_links.append(h)

                    except Exception as error:
                        print("error:",error)
                        reject_dict = {"url":the_url,"error":error}
                        self.reject_urls.append(reject_dict)
        print("checkpoint:",datetime.datetime.now().time())
        print("len of articles list:",len(articles))
        self.articles_urls = inner_href_links
        print("len of self.articles_urls:",len(self.articles_urls))    
        parag_art = []
        for inner in inner_href_links:
            self.if_state_idx = 1
            headers = {
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                            'Accept-Encoding': 'none',
                            'Accept-Language': 'en-US,en;q=0.8',
                            'Connection': 'keep-alive'
                        } 
            request = urllib.request.Request(inner,headers=headers)  
            opener = urllib.request.build_opener()
            time.sleep(10)
            filtered_html = etree.HTML(opener.open(request).read())
            text = filtered_html.xpath('//p')
            parag_list = []
            for t in text:
                if t not in parag_list:
                    print("paragraph:: ",t.text)
                    # parag_list.append(t.text)
                p_dict = {"art_url":inner,"paras":parag_list}
                # parag_art.append(p_dict)

        self.para_list = parag_art
        print("checkpoint:",datetime.datetime.now().time())
        print("end:",datetime.datetime.now().time())

class RegexThatURLOhYeah():

    def extract_domain_name(self,url):
        pattern = r'www\.(.*?)\.com'
        match = re.search(pattern, url)
        if match:
            result = match.group(1)
            return result
        else:
            return None
    def unwanted_from_links(self,href,unwanted):

        true_list = []
        for substring in unwanted:
            match = re.search(re.escape(substring), href)
            if match:
                true_list.append('darn')
        
        return(eval("(len(true_list)==0)"))


from scrape_info import XPATH_INPUT_DICT
grab = GrabArticlesAndArticleContent()
grab.feed_mainpage_info(xpath_input_dict=XPATH_INPUT_DICT)
# grab.feed_mainpage_info(xpath_input_dict=XPATH_INPUT_DICT)

# list_of_dicts = grab.para_list

# merged_dict = {}
# for d in list_of_dicts:
#     url = d["art_url"]
#     paragraphs = d["paras"]
#     if url in merged_dict:
#         merged_dict[url].extend(paragraphs)
#     else:
#         merged_dict[url] = paragraphs


# ct_ = 0
# while ct_ < 10:
#     for url, paragraphs in merged_dict.items():
#         ct_ += 1
#         print(f"URL: {url}, Merged Paragraphs: {paragraphs}")