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
def get_selenium_driver():
    """
    returns webdriver so selenium can be implemented more easily
    """
    webdriver_path = WEBDRIVER_PATH
    service = Service(executable_path=webdriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(service=service, options=options)    
    driver.minimize_window()
    return driver

class GrabArticlesAndArticleContent():
    def __init__(self):
        # inputs
        self.layers = []
        self.descendant_tags = []
        self.class_txts = []
        self.main_url = ""
        self.if_article_conditions = []
        # outputs
        self.reject_urls = []
        self.articles_urls = []
        self.para_list = []
        # internals
        self.grab_articles = True
        self.if_state_idx = 0


    def feed_info(self,xpath_input_dict):    

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

        self.layers = xpath_input_dict['layers']
        self.descendant_tags = xpath_input_dict['descendant_tags']
        self.class_txts = xpath_input_dict['class_txts']
        self.main_url = xpath_input_dict['main_url']
        self.if_states = xpath_input_dict['if_states']

        driver = get_selenium_driver()
        layers = self.layers
        descendant_tags = self.descendant_tags
        class_txts = self.class_txts
        if_states = self.if_states
        main_url = self.main_url
        url_list = []
        articles = []
        if self.grab_articles == False:
            url_list = self.articles_urls
        if self.grab_articles == True:
            url_list.append(self.main_url)
        print("url_list",url_list)
        url_list = url_list[0:15]
        parag_art = []
        for the_url in url_list:
            ctt = 0
            if self.grab_articles == True:
                while ctt < 8:
                    try:
                        if self.grab_articles == True:
                            ctt += 1
                            get_att = 'href'
                            the_url = main_url
                            driver.get(the_url)
                            print("start:",datetime.datetime.now().time())
                            print("checkpoint:",datetime.datetime.now().time())
                            # time.sleep(2)
                            xpath = ".//descendant::{descendant_tag}[@class='{class_txt}']/{layer}".format(
                                descendant_tag=descendant_tags[self.if_state_idx],
                                class_txt=class_txts[self.if_state_idx],
                                layer=layers[self.if_state_idx])
                            elements = driver.find_elements(By.XPATH,xpath)
                            print("length of elements:",len(elements))
                            print("checkpoint:",datetime.datetime.now().time())
                            # time.sleep(2)
                            len_ct = 0
                            # while ctt < 8:
                            for element in elements[0:15]:
                            # for element in elements:
                                len_ct += 1
                                # ctt += 1
                                print("elements left:",(len(elements)-len_ct))
                                if get_att == "href":
                                    print("checkpoint:",datetime.datetime.now().time())
                                    item = element.get_attribute(get_att)
                                    # time.sleep(2)
                                condition = if_states[self.if_state_idx]
                                print("checkpoint:",datetime.datetime.now().time())
                                if eval(condition): # execute string form of if statement
                                    print("checkpoint:",datetime.datetime.now().time())
                                    if item not in url_list:
                                        print(item)
                                        articles.append(item)
                    except Exception as error:
                        print("error:",error)
                        reject_dict = {"url":the_url,"error":error}
                        self.reject_urls.append(reject_dict)
                        ctt+=1
            if self.grab_articles == False:
                get_att = 'p'
                self.if_state_idx = 1
                headers = {
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                                'Accept-Encoding': 'none',
                                'Accept-Language': 'en-US,en;q=0.8',
                                'Connection': 'keep-alive'
                            } 
                request = urllib.request.Request(the_url,headers=headers)  
                opener = urllib.request.build_opener()
                time.sleep(10)
                filtered_html = etree.HTML(opener.open(request).read())
                text = filtered_html.xpath('//p')
                parag_list = []
                for t in text:
                    if t not in parag_list:
                        print("paragraph:: ",t.text)
                        parag_list.append(t.text)
            if get_att == "p":
                p_dict = {"art_url":the_url,"paras":parag_list}
                parag_art.append(p_dict)
            if get_att == "href":
                print("checkpoint:",datetime.datetime.now().time())
                print("len of articles list:",len(articles))
                self.articles_urls = articles
                print("len of self.articles_urls:",len(self.articles_urls))
            self.grab_articles = False
            self.para_list = parag_art
            print("checkpoint:",datetime.datetime.now().time())
            print("end:",datetime.datetime.now().time())

from scrape_info import XPATH_INPUT_DICT
grab = GrabArticlesAndArticleContent()
grab.feed_info(xpath_input_dict=XPATH_INPUT_DICT)
grab.feed_info(xpath_input_dict=XPATH_INPUT_DICT)

list_of_dicts = grab.para_list

merged_dict = {}
for d in list_of_dicts:
    url = d["art_url"]
    paragraphs = d["paras"]
    if url in merged_dict:
        merged_dict[url].extend(paragraphs)
    else:
        merged_dict[url] = paragraphs


ct_ = 0
while ct_ < 10:
    for url, paragraphs in merged_dict.items():
        ct_ += 1
        print(f"URL: {url}, Merged Paragraphs: {paragraphs}")