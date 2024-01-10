from selenium import webdriver      
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
import time
import psutil
import os
from lxml import etree
from lxml import html
import urllib.request
import http
import urllib
import datetime
import re
import math
from piapy import PiaVpn
import random
import json

WEBDRIVER_PATH = "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"

def change_vpn_location():
    """
    https://pypi.org/project/piapy/
    """
    locs = ['us-florida', 'us-atlanta', 'us-houston', 'us-washington-dc', 'us-east', 'us-chicago', 'us-new-york-city', 'us-texas', 'us-west','us-south-dakota']
    vpn = PiaVpn()
    current_region = vpn.region()
    locs = locs.remove(current_region)
    new_loc = random.choice(locs)
    print("changing to VPN IP location to:",new_loc)
    vpn.set_region(new_loc)
    changed = False
    while changed == False:
        print("sleeping now while change occurs")
        time.sleep(3)
        updated_region = vpn.region()
        if (updated_region != current_region):
            print("sleep complete. location changed.")
            changed = True
            locs = locs + [current_region]
            pass

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
        self.main_url = ""
        self.content_type =['politic','opinion','border']
        # outputs
        self.reject_urls = []
        self.articles_urls = []
        self.para_list = []
        # internals
        self.grab_articles = True
        self.if_state_idx = 0
        self.additional_unwanted = []
        self.headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Referer': '{main_url}'.format(main_url=self.main_url)
                    } 
        self.clipped_url = ""
        self.headline_grabapproach = ""

    def scroll_click_load_more(self,driver,xpath_input_dict):

        """
        scrolls page and clicks "load more". will modify this later so it can be agnostic to the website.
        want to also add functionality to search if it's a load more button, a next page button, or neither.
        """

        driver = get_selenium_driver(minimize=False)
        try:
            driver.get("NEWS.COM")
        except Exception as error:
            print("errorR:: ",error)

        ct = 0
        while ct <= 5:
            driver.execute_script("arguments[0].scrollIntoView();",driver.find_element(By.XPATH,".//descendant::div[@class='item load-more']/a"))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ".//descendant::div[@class='item load-more']/a"))).click()
            time.sleep(2)
            ct+= 1

    def grab_menu_url_links(self,the_url):

        """
        grab menu hrefs from header of html page, filter out unwanted urls
        """

        REGEX = RegexThatURLOhYeah()
        request = urllib.request.Request(the_url,headers=self.headers)  
        opener = urllib.request.build_opener()
        time.sleep(2)
        filtered_html = etree.HTML(opener.open(request).read())
        texts = filtered_html.xpath('//header')
        href_links=[]
        clipped_url = REGEX.extract_domain_name(the_url)
        for text in texts:
            href_link = text.xpath('.//a/@href')
            signsin = ["sign-in","sign-up"]
            for h in href_link:
                if((".com" in h)
                and("www" in h)
                and(h not in str for str in signsin)
                and(h != the_url)
                and(clipped_url == REGEX.extract_domain_name(h))
                and(h not in href_links)): 
                    href_links.append(h)
        return href_links

    def alternative_grab_paragraphs_headlines(self,url,selenium=False,urllib=True,request_sleep_time=2):
        p_dict = {}
        import urllib.request
        if selenium == True:
            urllib = False
            driver = get_selenium_driver()
            # print("checkpoint 1")
            driver.get(url)
            driver.implicitly_wait(request_sleep_time)
            # print("checkpoint 2")
            headline = driver.find_element(By.CSS_SELECTOR,"h1").text
            # print("headline:",headline)
            driver.implicitly_wait(request_sleep_time)
            elements = driver.find_elements(By.CSS_SELECTOR,"p")
            paras = []
            for elem in elements:
                para = elem.text
                # print("paragraph:",para)
                paras.append(para)
            p_dict = {"art_url":url,"paras":paras,"headline":headline.strip()}
        if urllib == True:
            try:
                print("inner url:",url)
                self.if_state_idx = 1
                request = urllib.request.Request(url,headers=self.headers) 
                time.sleep(request_sleep_time)
                opener = urllib.request.build_opener()
                time.sleep(request_sleep_time)
                filtered_html = etree.HTML(opener.open(request).read()) # 
                time.sleep(2)
                try:
                    headline_element = filtered_html.xpath("//h1") 
                except Exception as error:
                    print("error::",error)
                if headline_element:
                    # print("true",headline_element)
                    ct=0
                    for hedlin_el in headline_element:
                        if ct == 0:
                            headline = hedlin_el.text
                            # print("Headline:", headline_text.strip())
                            ct+=1
                        if ct == 1:
                            pass
                else:
                    print("Headline not found.")
                    headline = "headline_search_failed"
                parag_list = []
                text = filtered_html.xpath('//p')
                for t in text:
                    if t not in parag_list:
                        # print("paragraph:: ",t.text)
                        parag_list.append(t.text)
                    p_dict = {"art_url":url,"paras":parag_list,"headline":headline.strip()}
            except Exception as error:
                if "[WinError 10060]" in str(error):
                    change_vpn_location()
                print("reject on:",(url,error))
        return p_dict




    def feed_mainpage_info(self,main_url,additional_unwanted,reject_rate=0.35):    

        """     
        main_url: takes main newsite url (ex: "https://www.cnn.com"), finds header, grabs different news sections, then grabs articles within those news sections, and then grabs the content within those articles.
        additional_unwanted: takes unwanted str values that you don't want in the article URLs list
        reject_rate: how many articles are rejected before the while loop for grabbing articles 'gives up'
        """
        REGEX = RegexThatURLOhYeah()
        GRAB = GrabArticlesAndArticleContent()
        self.main_url = main_url
        self.clipped_url = REGEX.extract_domain_name(self.main_url)

        url_list = []
        articles = []
        url_list = GRAB.grab_menu_url_links(the_url=self.main_url)
        ult_url_list = url_list
        url_list = url_list[0:3]
        print("url list:",url_list)
        inner_href_links = []
        the_count = 0
        reject_count = 0
        threshold = len(url_list)*reject_rate
        reject_threshold = math.ceil(threshold)
        print("reject rate threshold:",reject_threshold)
        while(reject_count <= reject_threshold):
            # while len(inner_href_links) <= 10: 
                for the_url in url_list:
                    try:
                        clipped_url = REGEX.extract_domain_name(the_url)
                        request = urllib.request.Request(the_url,headers=self.headers)  
                        opener = urllib.request.build_opener()
                        time.sleep(3)
                        filtered_html = etree.HTML(opener.open(request).read())
                        texts = filtered_html.xpath('//body') # search body of page for article links
                        for text in texts:
                            href_link = text.xpath('.//a/@href')
                            unwanted = ["sign-in","sign-up","/contact/","/terms/","/privacy/","liveblog","/writers/"]
                            unwanted = unwanted + additional_unwanted
                            for h in href_link:
                                # catching href links with https:// in them
                                if(("https://" in h)   
                                and(h.count("/") >=3)
                                and((REGEX.unwanted_from_links(href=h,unwanted=unwanted)==True))
                                and(h != the_url)
                                and(clipped_url == REGEX.extract_domain_name(h))
                                and(h not in inner_href_links)
                                and(h not in ult_url_list)
                                and(h not in url_list)): 
                                    for content in self.content_type:
                                        if content in h:
                                            if h not in inner_href_links:
                                                print("complete:",h)
                                                inner_href_links.append(h)
                                # catching 'incomplete' links without https:// in them
                                elif("https://" not in h):
                                    if self.main_url[-1] == '/':
                                        full_url = self.main_url[:-1]+h
                                    if self.main_url[-1] != '/':
                                        full_url = self.main_url + h
                                    if((h.count("/") >=3)
                                    and((REGEX.unwanted_from_links(href=h,unwanted=unwanted)==True))
                                    and(h != the_url)
                                    and(h not in inner_href_links)
                                    and(h not in ult_url_list)
                                    and(full_url not in inner_href_links)
                                    and(h not in url_list)): 
                                        for content in self.content_type:
                                            if content in h:
                                                if h not in inner_href_links:
                                                    inner_href_links.append(full_url)
                                                    print("incomplete:",full_url)
                        the_count+=1
                    except Exception as error:
                        if "Error 429" in error:
                            print("error 429: too many requests")
                        reject_dict = {"url":the_url,"error":error}
                        reject_count += 1
                        self.reject_urls.append(reject_dict)
                        # print("reject count:",reject_count)
                        if reject_count > reject_threshold:
                            print("Reject count ({reject_count}) greater than reject threshold ({reject_threshold})".format(reject_count=reject_count,reject_threshold=reject_threshold))
                            break
                if True:
                    reject_count = 99999
        if True:
            while len(inner_href_links) < reject_threshold:
                print("fewer article links ({inner_href_links}) than the reject threshold of {reject_threshold}. stopping.".format(inner_href_links=len(inner_href_links),reject_threshold=reject_threshold))
                return None
            while len(inner_href_links) == 0:
                print("zero articles grabbed. stopping.")
                return None
        self.articles_urls = inner_href_links
        print("len of self.articles_urls:",len(self.articles_urls))    
        parag_art = [] # grab paragraphs and headlines
        inner_done = []
        for inner in inner_href_links[0:6]:
            
            if True:
                    true = "true"
                    if true == true:
                        if inner not in inner_done:
                            p_dict = GRAB.alternative_grab_paragraphs_headlines(url=inner,selenium=True)# if urllib fails, try selenium
                            # if p_dict:
                            if p_dict not in parag_art:
                                parag_art.append(p_dict)
                            selenium_failed = False
                            print("selenium success.")
                            inner_done.append(inner)
                    else:
                        print("selenium failed. Moving on.")
                        selenium_failed = True
            if selenium_failed == True:
                    true = "true"
                    if true == true:
                        if inner not in inner_done:
                            p_dict = GRAB.alternative_grab_paragraphs_headlines(url=inner,urllib=False) # try urllib first 
                            # if p_dict: 
                            if p_dict not in parag_art:
                                parag_art.append(p_dict)
                            print("urllib success.")
                            inner_done.append(inner)
                    else:
                        print("urllib and selenium both failed. Moving on.")
                        ran_num = random.randint(1000,9999)
                        p_dict = {"art_url":"failed_to_scrape.com","paras":["I","have","failed","you","...","{ran_num}".format(ran_num=ran_num)],"headline":"Local Man Claims This Article Failed to be Scraped Today"}
            parag_art.append(p_dict)
        self.para_list = parag_art
<<<<<<< Updated upstream
 
=======
    def create_searchable_content(self,):
        done = []
        parag_art = self.para_list
        merged_dict = {}
        dict_count = 0
        REGEX = RegexThatURLOhYeah()
        current_datetime = datetime.now()
        custom_format = "%Y_%m_%d_%H_%M_%S"
        formatted_datetime = current_datetime.strftime(custom_format)
        clipped_url = REGEX.extract_domain_name(self.main_url)
        current_datetime = datetime.now()
        if dict_count == 0:
            merged_dict[f"dict_id_{clipped_url}_00"] = {
                        "main_url": self.main_url,
                        "article_content_search": self.content_type,
                        "scrape_date_time":formatted_datetime
                    }
        for d in parag_art:
            if d not in done:
                dict_count += 1
                dict_ct = f"dict_id_{clipped_url}_0{dict_count}"
                url = d["art_url"]
                paragraphs = d["paras"]
                headline = d['headline']
                if dict_count > 0:
                    merged_dict[dict_ct] = {
                        "url": url,
                        "headline": headline,
                        "article_content": paragraphs
                    }
                done.append(d)

        with open('test_result_{clipped_url}_{now}.json'.format(now=formatted_datetime,clipped_url=clipped_url), 'w') as fp:
            json.dump(merged_dict, fp)

    def search_through_content(self,**keywordsearch):

        topics = keywordsearch["topics"]
        keywords = keywordsearch["keywords"]

>>>>>>> Stashed changes
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

from scrape_info import MAIN_URL #, XPATH_INPUT_DICT
from datetime import datetime
run_vpn_and_chromedriver() # make sure VPN is running
grab = GrabArticlesAndArticleContent()
grab.content_type = ['trump','border','migrants']
grab.feed_mainpage_info(main_url=MAIN_URL,additional_unwanted=["twitter.com","/topic/","/author/","/clips/"],)
searchable_content = grab.create_searchable_content()

