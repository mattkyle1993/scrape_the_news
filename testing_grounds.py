from selenium import webdriver      
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
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

WEBDRIVER_PATH = "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"

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

# class TestArticleOrNot():
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
#                 print("The maximum datetime is more than 3 years from the current date.")T
#                 return False, max_datetime
#         else:
#             print("No valid datetime found in the strings.")
#             return False, max_datetime

#     def article_or_not(self,the_url="https://www.commondreams.org/"):
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
#             matches1 = []
#             matches2 = []
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
#             pattern1 = r'(\d{1,2} [A-Za-z]+ (?!and) \d{4}, \d{1,2}:\d{2} [ap]m|' \
#                   r'Today, \d{1,2}:\d{2} [ap]m|\d{1,2} [A-Za-z]+ (?!and) \d{4}, \d{1,2}:\d{2} [ap]m|' \
#                   r'>[A-Za-z]+\.\s\d{1,2}, \d{4}<|' \
#                   r'>\d{1,2} [A-Za-z]+ \d{4}, \d{1,2}:\d{2} [ap]m<|' \
#                   r'>Today, \d{1,2}:\d{2} [ap]m<|' \
#                   r'>\d{1,2} [A-Za-z]+ (?!and) \d{4}, \d{1,2}:\d{2} [ap]m|\d{2} [A-Za-z]+ (?!and) \d{4})'
#             pattern2 = r'\d{1,2} [A-Za-z]+ \d{4}'
#             try:
#                 matches1 = re.findall(pattern1, html_page_source)
#             except Exception as error:
#                 print("error2:",error)
#             skip = False
#             may_pass = True
#             if len(matches1) > 0:
#                 if may_pass == False:
#                     break
#                 print(matches1)
#                 for date in matches1:
#                     if "and" in date:
#                         may_pass = False
#                         # break
#                     if may_pass == True:
#                         answer, match = self.parse_datetime(datetime_strs=matches1,matches2=False)
#                         if answer == True:
#                             datetime_str = match
#                             # print(f"Datetime found (Pattern 1): {datetime_str}")
#                             skip = True
#                             return True
#                         if answer == False:
#                                 ult_ct+=1
#                     if may_pass == False:
#                         ult_ct+=1
#                         print("here1:",ult_ct)
#                         matches1 = []
#                         break
#             if skip == False:
#                 may_pass = True
#                 matches2 = re.findall(pattern2, html_page_source)
#                 if len(matches2) > 0:
#                     if may_pass == False:
#                         break
#                     print(matches2)
#                     for date in matches1:
#                         if "and" in date:
#                             may_pass = False
#                             # break
#                         if may_pass == True:
#                             answer, match = self.parse_datetime(datetime_strs=matches2,matches2=True)
#                             if answer == True:
#                                 datetime_str = match
#                                 # print(f"Datetime found (Pattern 2): {datetime_str}")
#                                 return True
#                             if answer == False:
#                                 ult_ct+=1
#                         if may_pass == False:
#                             ult_ct+=1
#                             print("here2:",ult_ct)
#                             matches2 = []
#                             break
#             ult_list = matches1 + matches2
#             if(len(ult_list)==0): 
#                 try_again = True           
#                 print("trying again with further-parsed-html")
#                 skip = False
#                 if ult_ct > 2:
#                     last_bit_of_url()
#                     return False
#                 else:
#                     ult_ct+=1
# answer = TestArticleOrNot().article_or_not()
# print(answer)

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


import urllib.request
from bs4 import BeautifulSoup

# url = "https://www.timesofisrael.com/israel-and-the-region/"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# }

# request = urllib.request.Request(url, headers=headers)
# response = urllib.request.urlopen(request)
# html_content = response.read()
# soup = BeautifulSoup(html_content, "html.parser")



# tags = [["div","nav"],["div","nav"]]
# class_names = ["load","pagination","next","older"]

# # Use CSS selector with the * wildcard to find elements containing "load" in class attribute
# elements = soup.select("div[class*=load]")

# for element in elements:
#     print("Text content:", element.text)
#     xpath = build_element_xpath(element)
#     print("XPath:", xpath)

# # /html/body/div[4]/div/section[2]/div[18]/a/text() # built
# # /html/body/div[4]/div/section[2]/div[18]/a # real
    
# driver = get_selenium_driver()
# driver.get(url)
# element = driver.find_element(By.XPATH,"/html/body/div[4]/div/section[2]/div[18]")
# print(element)

def unwanted_from_links(href,unwanted):
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

def find_next_page_load_button(url):
    # url = "https://www.breitbart.com/politics/"
    headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Referer': '{main_url}'.format(main_url=url)
                    }

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html_content = response.read()
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.find_all(recursive=True)

    def find_tag_with_main(input_str):
            matches = re.findall(r'<[^>]+>', input_str)
            return matches

    load_pagination_words = ["load", "pagination", "more", "older", "page", "load-more", "load more", "older posts", "older-posts"]
    load_pagination_tags = ["<div", "<nav", "<a", "<button"]
    tuple_list = []
    elem_short_set = set()  # Use a set to store unique elem values



    for element in elements:
        for elem in find_tag_with_main(str(element)):
            if elem not in elem_short_set:
                for word in load_pagination_words:
                    if not(re.search(rf'\b{re.escape(word)}\b', elem)):
                        pass
                    else:
                        for tag in load_pagination_tags:
                            if tag not in elem:
                                pass
                            else:
                                if elem.count('-') < 7:
                                    tuple_ct = 0
                                    while tuple_ct < len(load_pagination_tags):
                                        if load_pagination_tags[tuple_ct] in elem:
                                            tuple_ct += 1
                                            # Iterate through the tuple_list to check if elem already exists in any tuple
                                            found = False
                                            for item in tuple_list:
                                                if elem == item[1]:
                                                    found = True
                                                    break
                                            if not found:
                                                tuple_list.append((word, elem))
                                        else:
                                            tuple_ct += 1
                                            
    tuple_list.sort(key=lambda x: min(load_pagination_words.index(word) if word in x[1] else float('inf') for word in load_pagination_words))
    # print("tuple_list:",tuple_list)
    if len(tuple_list) == 0:
        print("tuple list failed to create")
    final_element = "None"
    the_element = []
    if len(tuple_list) > 1:
        for tag in load_pagination_tags:
            for item in tuple_list:
                # print("item:",item)
                if tag in item[1]:
                    if tag == "<div":
                        the_element.append(item[1])
                    if tag == "<nav":
                        the_element.append(item[1])
                    if tag == "<a":
                        the_element.append(item[1])
                    if tag == "<button":
                        the_element.append(item[1])
    if len(the_element) == 0:
        if len(tuple_list) == 0:
            print("failed. zero elements.")
            final_element = None
        if len(tuple_list) == 1:
            print("only tuple list. is len() of 1")
            final_element = tuple_list[0][1]
            # print("final_element",(final_element,tuple_list))
    if len(the_element) == 1:
        print("element list is len() of 1")
        final_element = the_element[0]
        # print("final_element",(final_element,the_element))
    # print("the element list:",the_element)
    # print("final element", final_element)
    if len(the_element) > 1:

        div_s = []
        nav_s = []
        a_s = []
        button_s = []
        for tag in load_pagination_tags:
            for element in the_element:
                if tag in element:
                    if tag.startswith("<div"): 
                        div_s.append(element)
                    if tag.startswith("<nav"):
                        nav_s.append(element)
                    if tag.startswith("<a"):
                        a_s.append(element)
                    if tag.startswith("<button"):
                        button_s.append(element)
        if len(div_s) > 0:
            final_element = div_s[0]
        else:
            if len(nav_s) > 0:
                if "pagination" in final_element:
                    pass
                if "pagination" not in final_element:
                    final_element = nav_s[0]
            else:
                if len(button_s) > 0:
                    final_element = button_s[0]
                else:
                    if len(a_s) > 0:
                        final_element = a_s[0]
                    else:
                        final_element = None

    pattern = r'<(\w+)\s.*?class="([^"]+)"'

    matches = re.search(pattern, final_element)
    if matches:
        tag_name = matches.group(1)
        class_attribute = matches.group(2)
        # print(f'Tag Name: {tag_name}')
        # print(f'Class Attribute: {class_attribute}')
    else:
        print('No match found.')
    return (final_element,tag_name,class_attribute)

interact_button_elements = []
tag_and_class = []
urls = ["https://www.vox.com/politics"]
for URL in urls:
    final_element = find_next_page_load_button(url=URL)
    tag_and_class.append((final_element[1],final_element[2]))
    interact_button_elements.append((final_element[0],URL))
# print(interact_button_elements)
    
    driver = get_selenium_driver(minimize=False)
    driver.get("https://www.vox.com/politics")
    driver.implicitly_wait(2)
    # driver.find_element(By.XPATH,("//{tag_}[contains(@class,'{class_}')]".format(tag_=final_element[1],class_=final_element[2]))).click()
    # element = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//{tag_}[contains(@class,'{class_}')]".format(tag_=final_element[1],class_=final_element[2])))
    # )
    # element.click()
    ct = 0
    load_more_elem = "//{tag_}[contains(@class,'{class_}')]".format(tag_=final_element[1],class_=final_element[2])
    while ct <= 3:
        driver.execute_script("arguments[0].scrollIntoView();",driver.find_element(By.XPATH,load_more_elem))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, load_more_elem))).click()
        time.sleep(2)
        ct+= 1
        if ct == 3:
            web_page = driver.page_source

               