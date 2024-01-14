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
from datetime import datetime, timedelta
import re
import math
from piapy import PiaVpn
import random
import json
from dateutil import parser
from bs4 import BeautifulSoup
from article_urls_model.article_url_guess_model import ArticleURLGuesserModel

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

def build_element_xpath(element):
    """
    Recursively build the XPath for a BeautifulSoup element.
    """
    if element.parent is None:
        return '/' + element.name

    siblings = element.find_previous_siblings(element.name)
    if siblings:
        element_index = len(siblings) + 1
    else:
        element_index = 1

    return build_element_xpath(element.parent) + '/' + element.name + '[' + str(element_index) + ']'


class NavigateArticleLisTWebPage():
    def __init__(self,GRAB):
        self.navigate_style = "agnostic"
        self.navigate_list = ["pagination_style","load_more_style"] 
        self.GRAB = GRAB
        self.web_pages = []
        self.headers = self.GRAB.headers
        pass
    def navigate_articles_list_webpage(self,article_list_webpage,request_sleep_time=5):

        """
        scrolls page and clicks "load more". will modify this later so it can be agnostic to the website.
        want to also add functionality to search if it's a load more button, a next page button, or neither.
        """
        GRAB = self.GRAB
        if GRAB.navigate_style not in ["pagination_style","load_more_style"]: 
            GRAB(navigate_style = "agnostic")
        else:
            self.navigate_style = GRAB.navigate_style
            
        def load_more_style():

            nav_check = 0

            driver = get_selenium_driver(minimize=False)
            driver.get(article_list_webpage)
            driver.implicitly_wait(request_sleep_time)

            elements = driver.find_elements(By.CSS_SELECTOR,"a")
            nav_check+=1
            print("nav_check:",nav_check)
            driver.implicitly_wait(request_sleep_time)


            nav_check+=1
            print("nav_check:",nav_check)

            try:
                request = urllib.request.Request(article_list_webpage,headers=self.headers)  
                opener = urllib.request.build_opener()
            except Exception as error:
                print("load more style error here:",str(error))
            nav_check+=1
            print("nav_check:",nav_check)
            time.sleep(request_sleep_time)
            nav_check+=1
            print("nav_check:",nav_check)
            try:
                filtered_html = etree.HTML(opener.open(request).read())
                tree = etree.parse(filtered_html)
            except Exception as error:
                print("filtered html error:",str(error))
            nav_check+=1
            print("nav_check:",nav_check)

            try:
                ct = 0
                for elem in elements:
                    e_text = elem.text
                    nav_check+=1
                    print("nav_check:",nav_check)
                    if "load" in e_text.lower():
                        print("text of element, element object, and xpath str:",(e_text,elem,tree.getpath(elem)))
                        break
                load_more_elem = elem.get_attribute('xpath') 
                print("load more elem:",load_more_elem)
                while ct <= 3:
                    driver.execute_script("arguments[0].scrollIntoView();",driver.find_element(By.XPATH,load_more_elem))
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, load_more_elem))).click()
                    time.sleep(request_sleep_time)
                    ct+= 1
                    if ct == 3:
                        web_page = driver.page_source
                        self.web_pages.append(web_page)
                if self.navigate_style == "agnostic":
                    print("load_more_style is nav style")
                return True
            except Exception as error:
                print("load more style error:: ",str(error))
                return False
            
        def pagination_style():
            error_ = ""
            ct = 1
            wp_ct = 0
            while ct <= 3:
                try:
                    driver = get_selenium_driver(minimize=False)
                    article_list_webpage_1 = article_list_webpage + f"/page/{ct}/"
                    driver.get(article_list_webpage_1)
                    driver.implicitly_wait(request_sleep_time)
                    the__url = driver.current_url
                    if the__url in article_list_webpage_1:
                        pass
                    if the__url not in article_list_webpage_1:
                        error_ = "problem"
                except Exception as error:
                    print("error in navigate_articles_list_webpage.next_page_button function:",error)
                    error_ = str(error)
                    return False
                if error_ == "":
                    web_page = driver.page_source
                    self.web_pages.append(web_page)
                    ct+=1
                    wp_ct+= 1
                if True:
                    if ct == 3:
                        if wp_ct == 0:
                            print('failure')
                            return False
                        if wp_ct > 0:
                            if self.navigate_style == "agnostic":
                                print("pagination_style is nav style")
                                return True
                    else:
                        pass

        def figure_out_nav_style():
            unchosen = True
            rainge=6
            range_minus = rainge-1
            while unchosen == True:
                for z in range(rainge):
                    if(load_more_style()==True):
                        unchosen = False
                        self.navigate_style = "load_more_style"
                        GRAB(navigate_style = "load_more_style")
                        return True
                    if(pagination_style()==True):
                        unchosen = False
                        self.navigate_style = "pagination_style"
                        GRAB(navigate_style = "pagination_style")
                        return True
                    if z == range_minus:
                        unchosen = False
                        return False
                        
        if self.navigate_style == "agnostic":
            diagnosis = figure_out_nav_style()
            if diagnosis == False:
                print("failed to figure out navigation style")
                self.navigate_style = "no_style"
        if self.navigate_style == "load_more_style":
            _=load_more_style()
            if _ == False:
                print("load_more_style failed")
        if self.navigate_style == "pagination_style":
            _=pagination_style()
            if _ == False:
                print("pagination_style failed")
        if self.navigate_style == "no_style":
            #do absolutely nothing
            pass

# class ArticleOrNot():

#     def __init__(self,years_within=.25):
#         self.suggested_for_the_boot = []
#         self.years_within = years_within
#         pass

#     def parse_datetime(self,datetime_strs,matches2=False):
#         max_datetime = None
#         for datetime_str in datetime_strs:
#             try:
#                 parsed_datetime = parser.parse(datetime_str)
#                 if max_datetime is None or parsed_datetime > max_datetime:
#                     max_datetime = parsed_datetime
#             except ValueError:
#                 pass  # Invalid datetime format, continue to the next string
#         if max_datetime:
#             current_date = datetime.now()
#             three_years = timedelta(days=365*self.years_within)
#             time_difference = current_date - max_datetime
#             if time_difference <= three_years:
#                 return True, max_datetime
#             else:
#                 print("The maximum datetime is more than 3 years from the current date.")
#                 return False, max_datetime
#         else:
#             print("No valid datetime found in the strings.")
#             return False, max_datetime
        
#     def article_or_not(self,the_url="https://www.timesofisrael.com"):
#         """
#         Determine whether a given URL is an article or not. if it's determined not to be an article, it appends the url to the 'TestArticleOrNot.suggested_for_the_boot' list.
#         The 'TestArticleOrNot.suggested_for_the_boot' tuple list can be retreived and then used to pick out url chunks (e.g., "/authors/", "/careers/","/podcasts/"). 
#         Then, that list can be used to fine tune the scraper so it grabs less and less junk/irrelevant URLS. I.e., add the results to the unwanted list
#         """
#         def last_bit_of_url():
#             match = re.search(r'/([^/]+)/?$', the_url)
#             if match:
#                 last_part = match.group(1)
#                 self.suggested_for_the_boot.append((the_url,last_part,"article suggested for booting. last_bit_of_url diagnosis: success"))
#             else:
#                 last_part = "FUNC_FAILED"
#                 self.suggested_for_the_boot.append((the_url,last_part,"article suggested for booting. last_bit_of_url diagnosis: fail"))
#                 pass
#         # begin function    
#         ult_ct = 1
#         while ult_ct <=2:
#             driver = get_selenium_driver()
#             try:
#                 driver.get(the_url)
#             except Exception as error:
#                 print("error1:",error)
#             driver.implicitly_wait(2)
#             html_page_source = driver.page_source
#             try_again = False
#             if try_again == True:
#                 soup = BeautifulSoup(html_page_source, 'html.parser')
#                 html_page_source = str(soup.header) # get body of page
#             # print(html_page_source)
#             pattern1 = r'(?:>\w+(?:\.|\s)\d{1,2}, \d{4}<)|(\d{1,2} [A-Za-z]+ \d{4}, \d{1,2}:\d{2} (am|pm)|Today, \d{1,2}:\d{2} (am|pm)|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
#             pattern2 = r'\d{1,2} [A-Za-z]+ \d{4}'
#             try:
#                 matches1 = re.findall(pattern1, html_page_source)
#             except Exception as error:
#                 print("error2:",error)
#             skip = False
#             matches1 = []
#             matches2 = []
#             if matches1:
#                 # print(matches1)
#                 answer, match = self.parse_datetime(datetime_strs=matches1,matches2=False)
#                 if answer == True:
#                     datetime_str = match
#                     # print(f"Datetime found (Pattern 1): {datetime_str}")
#                     skip = True
#                     return True
#                 if answer == False:
#                         ult_ct+=1
#             if skip == False:
#                 matches2 = re.findall(pattern2, html_page_source)
#                 if matches2:
#                     # print(matches2)
#                     answer, match = self.parse_datetime(datetime_strs=matches2,matches2=True)
#                     if answer == True:
#                         datetime_str = match
#                         # print(f"Datetime found (Pattern 2): {datetime_str}")
#                         return True
#                     if answer == False:
#                         ult_ct+=1
#             ult_list = matches1 + matches2
#             if(len(ult_list)==0): 
#                 try_again = True           
#                 print("trying again with further-parsed-html")
#                 skip = False
#                 if ult_ct == 2:
#                     last_bit_of_url()
#                     return False
#                 else:
#                     ult_ct+=1

class GrabArticlesAndArticleContent():
    def __init__(self,main_url,article_headline_content_type=[],mainmenu_news_topic=[],sleep_seconds=2,reject_rate=0.0,navigate_style="agnostic",additional_unwanted=[]):

        self.main_url = main_url
        self.article_headline_content_type = article_headline_content_type
        self.mainmenu_news_topic = mainmenu_news_topic
        self.reject_rate = reject_rate

        self.reject_urls = []
        self.articles_urls = []
        self.para_list = []
        self.merged_dict = {}
        self.all_paragraphs = []

        self.sleep_seconds = sleep_seconds
        self.search_content_json_file_name = ""
        self.grab_articles = True
        self.if_state_idx = 0
        self.additional_unwanted = additional_unwanted
        self.navigate_style = navigate_style
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

    def grab_menu_url_links(self,the_url):
        """
        grab menu hrefs from header of html page, filter out unwanted urls
        """
        REGEX = RegexFunctions()
        request = urllib.request.Request(the_url,headers=self.headers)  
        opener = urllib.request.build_opener()
        time.sleep(self.sleep_seconds)
        filtered_html = etree.HTML(opener.open(request).read())
        texts = filtered_html.xpath('//header')
        href_links=[]
        clipped_url = REGEX.extract_domain_name(the_url)
        for text in texts:
            href_link = text.xpath('.//a/@href')
            signsin = ["sign-in","sign-up"]
            for h in href_link:
                # print(h)
                if((".com" in h)
                and("www" in h)
                and(h not in str for str in signsin)
                and(h != the_url)
                and(clipped_url == REGEX.extract_domain_name(h))
                and(h not in href_links)): 
                    # print('reached')
                    # print(self.mainmenu_news_topic)
                    # if REGEX.unwanted_from_links(href=h,unwanted=self.mainmenu_news_topic) == False:
                    href_links.append(h)
                    # break
        return href_links

    def alternative_grab_paragraphs_headlines(self,url,selenium=False,urllib=True,):
        p_dict = {}
        import urllib.request
        if selenium == True:
            urllib = False
            driver = get_selenium_driver()
            driver.get(url)
            print("url from selenium:",url)
            driver.implicitly_wait(self.sleep_seconds)
            headline = driver.find_element(By.CSS_SELECTOR,"h1").text
            driver.implicitly_wait(self.sleep_seconds)
            elements = driver.find_elements(By.CSS_SELECTOR,"p")
            parag_list = []
            for elem in elements:
                para = elem.text
                parag_list.append(para)
            p_dict = {"art_url":url,"paras":parag_list,"headline":headline.strip()}
            self.all_paragraphs.append(parag_list)
        if urllib == True:
            try:
                print("inner url:",url)
                self.if_state_idx = 1
                request = urllib.request.Request(url,headers=self.headers) 
                time.sleep(self.sleep_seconds)
                opener = urllib.request.build_opener()
                time.sleep(self.sleep_seconds)
                filtered_html = etree.HTML(opener.open(request).read()) # 
                time.sleep(self.sleep_seconds)
                try:
                    headline_element = filtered_html.xpath("//h1") 
                except Exception as error:
                    print("error::",error)
                if headline_element:
                    ct=0
                    for hedlin_el in headline_element:
                        if ct == 0:
                            headline = hedlin_el.text
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
                        parag_list.append(t.text)
                    p_dict = {"art_url":url,"paras":parag_list,"headline":headline.strip()}
                    self.all_paragraphs.append(parag_list)
            except Exception as error:
                if "[WinError 10060]" in str(error):
                    change_vpn_location()
                print("reject on:",(url,error))
        return p_dict

    def create_searchable_content(self,):
        done = []
        parag_art = self.para_list
        merged_dict = {}
        dict_count = 0
        REGEX = RegexFunctions()
        current_datetime = datetime.now()
        custom_format = "%Y_%m_%d_%H_%M_%S"
        formatted_datetime = current_datetime.strftime(custom_format)
        clipped_url = REGEX.extract_domain_name(self.main_url)
        current_datetime = datetime.now()
        if dict_count == 0:
            merged_dict[f"dict_id_{clipped_url}_00"] = {
                        "main_url": self.main_url,
                        "article_content_search": self.article_headline_content_type,
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
        file_name = 'json_results_output/test_result_{clipped_url}_{now}.json'.format(now=formatted_datetime,clipped_url=clipped_url)
        with open(file_name, 'w') as fp:
            json.dump(merged_dict, fp)
        self.search_content_json_file_name = file_name
        self.merged_dict = merged_dict

    def search_through_content(self): # ,**keywordsearch
        REGEX = RegexFunctions()
        current_datetime = datetime.now()
        custom_format = "%Y_%m_%d_%H_%M_%S"
        formatted_datetime = current_datetime.strftime(custom_format)
        clipped_url = REGEX.extract_domain_name(MAIN_URL)
        keywords = self.article_headline_content_type
        json_file_name = self.search_content_json_file_name
        with open(f"{json_file_name}","r",encoding="utf-8") as file:
            loop_dict = json.load(file)
        topic_count = {}
        len_ = len(self.articles_urls) + 1
        for i in range(len_):
            if i == 0:
                pass
            else:
                try:
                    dict_id = f"dict_id_{clipped_url}_0{i}"
                    # print(self.merged_dict)
                    # loop_dict = self.merged_dict[dict_id]
                    paragraphs = loop_dict[dict_id]['article_content']
                    headline = loop_dict[dict_id]['headline']
                    url = loop_dict[dict_id]["url"]
                    print("search through content url here:",url)
                    topic_count[dict_id] = {
                            "main_url": MAIN_URL,
                            "article_url":url,
                            "headline":headline,
                            "article_content_search": keywords,
                                }
                    for keyword in keywords:
                        topic_count[dict_id][f"{keyword}_ct"]=0
                    for paragraph in paragraphs:
                        # print("paragraph:",paragraph)
                        paragraph = paragraph.lower()
                        for keyword in keywords:
                            top_ct = paragraph.count(keyword.lower())
                            # print(top_ct)
                            topic_count[dict_id][f"{keyword}_ct"]+=top_ct
                except Exception as error:
                    print("search_through_content error here:",error)
        with open('json_keyword_count/keyword_count_{clipped_url}_{now}.json'.format(now=formatted_datetime,clipped_url=clipped_url), 'w') as fp:
            json.dump(topic_count, fp)

    def count_all_words_in_article_content(self,):
        from collections import defaultdict
        word_counts = defaultdict(int)
        nested_content_list = self.all_paragraphs
        flat_list = []
        for nest in nested_content_list:
            if type(nest) == str:
                nest = nest.split()
                for nestt in nest:
                    flat_list.append(nestt)
            if type(nest) == list:
                for n in nest:
                    nn = n.split()
                    for nnn in nn:
                        flat_list.append(nnn)
        for content in flat_list:
            words = content.split()
            for word in words:
                word_counts[word]+=1

    def feed_mainpage_info(self,):    

        """     
        main_url: takes main newsite url (ex: "https://www.cnn.com"), finds header, grabs different news sections, then grabs articles within those news sections, and then grabs the content within those articles.
        additional_unwanted: takes unwanted str values that you don't want in the article URLs list
        reject_rate: how many articles are rejected before the while loop for grabbing articles 'gives up'
        """
        REGEX = RegexFunctions()
        GRAB = GrabArticlesAndArticleContent(main_url=self.main_url,article_headline_content_type=self.article_headline_content_type,mainmenu_news_topic=self.mainmenu_news_topic)
        self.clipped_url = REGEX.extract_domain_name(self.main_url)
        NAVIGATE = NavigateArticleLisTWebPage(GRAB=GRAB)

        url_list = []
        url_list = GRAB.grab_menu_url_links(the_url=self.main_url)
        ult_url_list = url_list
        print("the url list:",url_list)
        GUESS = ArticleURLGuesserModel()
        # url_list = url_list[0:3]
        # print("trimmed url list:",url_list)
        inner_href_links = []
        inner_href_set = set(inner_href_links)
        reject_count = 0
        threshold = len(url_list)*self.reject_rate
        reject_threshold = math.ceil(threshold)
        print("reject rate threshold:",reject_threshold)
        error_429 = 0
        skip = False
        temp_h_list = []
        while(reject_count <= reject_threshold):
                for theurl in url_list:
                    try:    
                        # print("theurl",theurl)
                        # NAVIGATE.navigate_articles_list_webpage(article_list_webpage=theurl)
                        # for the_url in NAVIGATE.web_pages:
                        clipped_url = REGEX.extract_domain_name(theurl)
                        request = urllib.request.Request(theurl,headers=self.headers)  
                        opener = urllib.request.build_opener()
                        time.sleep(self.sleep_seconds)
                        filtered_html = etree.HTML(opener.open(request).read())
                        # texts = filtered_html.xpath('//body') # search body of page for article links
                        # for text in texts:
                        divs = filtered_html.xpath('//div')
                        for d in divs:
                            a_elements = d.xpath(".//a")  # Find all <a> elements within the <div>
                            ct = 0
                            for a_element in a_elements:
                                h = a_element.get("href")  # Get the href attribute from the <a> element
                                # ct = 0
                                if h is not None:
                                    if h not in temp_h_list:
                                        temp_h_list.append(h)
                                        ct+=1
                                        if(h.startswith("https://")==False):
                                            if MAIN_URL[-1] == '/':
                                                h = MAIN_URL[:-1]+h
                                            if MAIN_URL[-1] != '/':
                                                h = MAIN_URL + h
                                            prediction = GUESS.run_article_guesser_model(h,save_article_guesses=False,print_results=True,print_only_neg_results=True)
                                            if prediction[0] == 1:
                                                inner_href_set.add(h)
                                                skip = True
                                            if prediction[0] == 0:
                                                skip = True
                                        if skip == False:
                                            if(h.startswith("https://")==True):  
                                                prediction = GUESS.run_article_guesser_model(h,save_article_guesses=False,print_results=True,print_only_neg_results=True)
                                                if prediction[0] == 1:
                                                    inner_href_set.add(h)
                                                    skip = False
                                                if prediction[0] == 0:
                                                    skip = False
                                        skip = False
                    except Exception as error:
                        if "Error 429" in str(error):
                            error_429+=1
                            # print("error 429: too many requests")
                            if error_429 <= 3:
                                print("Error 429: too many requests. Current error 429 ct:{error_429}. Sleeping for {sleep_seconds}".format(error_429=error_429,sleep_seconds=self.sleep_seconds*2))
                                time.sleep(self.sleep_seconds*2)
                            if error_429 > 3:
                                print("Error 429: too many requests. Current error 429 ct:{error_429}. Sleeping for {sleep_seconds}".format(error_429=error_429,sleep_seconds=self.sleep_seconds*3))
                                time.sleep(self.sleep_seconds*3)
                        reject_dict = {"url":theurl,"error":str(error)}
                        reject_count += 1
                        self.reject_urls.append(reject_dict)
                        # print("reject count:",reject_count)
                        if reject_threshold > 0:
                            if reject_count > reject_threshold:
                                print("Reject count ({reject_count}) greater than reject threshold ({reject_threshold})".format(reject_count=reject_count,reject_threshold=reject_threshold))
                                break  
                if True:
                    reject_count = 99999
        if True:
            if reject_threshold > 0:
                while len(inner_href_links) < reject_threshold:
                    print("fewer article links ({inner_href_links}) than the reject threshold of {reject_threshold}. stopping.".format(inner_href_links=len(inner_href_links),reject_threshold=reject_threshold))
                    return None
                while len(inner_href_links) == 0:
                    print("zero articles grabbed. stopping.")
                    return None
            else:
                while len(inner_href_links) == 0:
                    print("zero articles grabbed. stopping.")
                    return None
        inner_href_links = list(inner_href_set)
        self.articles_urls = inner_href_links
        print("len of self.articles_urls:",len(self.articles_urls))    

        file_name = "article_urls_model/model_guesses_output/model_guesses_output"
        parag_art = [] # grab paragraphs and headlines
        inner_done = []
        # print("inner links:",inner_href_links)
        for inner in inner_href_links:
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

class RegexFunctions():
    def extract_domain_name(self,url):
        pattern = r'www\.(.*?)\.com'
        match = re.search(pattern, url)
        if match:
            result = match.group(1)
            return result
        else:
            return None
    def unwanted_from_links(self,href,unwanted):
        """
        if any number of unwanted terms are found in the href link it will return False.
        If no unwanted tersm are found in the href link it will return True.
        """
        true_list = []
        for substring in unwanted:
            match = re.search(re.escape(substring), href)
            if match:
                true_list.append('darn')
        return(eval("(len(true_list)==0)"))

from scrape_info import MAIN_URLS,MAIN_MENU_TOPICS,MAIN_KEYWORDS #, 
from datetime import datetime
run_vpn_and_chromedriver() # make sure VPN is running

for MAIN_URL,MAIN_TOPIC,MAIN_KEYWORD in zip(MAIN_URLS,MAIN_MENU_TOPICS,MAIN_KEYWORDS):
    print((MAIN_URL,MAIN_TOPIC,MAIN_KEYWORD))
    grab = GrabArticlesAndArticleContent(main_url=MAIN_URL,mainmenu_news_topic=MAIN_TOPIC,article_headline_content_type=MAIN_KEYWORD)
    grab.feed_mainpage_info()
    grab.create_searchable_content()
    grab.search_through_content()

