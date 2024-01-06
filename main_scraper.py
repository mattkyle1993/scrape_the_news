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
        self.driver = ""
        self.xpath = ""
        self.layer = ""
        self.class_name = ""
        self.descendant_tag = ""
        self.class_txt = ""
        self.main_url = ""
        self.if_article_condition = ""
        self.reject_urls = []
        self.articles = []
        self.return_list = []
        self.articles_urls = []
        self.para_list = []

    def feed_info(self,driver,xpath,main_url,if_states,xpath_input_dict={}): #layer,class_name,descendant_tag,class_txt

        """     xpath_input_dict = {
                    descendant_tag:["article_tag","para_tag"],
                    class_name:["article_class","para_class"],
                    class_txt:["article_txt","para_txt"],
                    layer:["article_layer","para_layer"]
                }
        """
        self.driver = driver
        self.xpath = xpath
        self.layer = layer
        self.class_name = class_name
        self.descendant_tag = descendant_tag
        self.class_txt = class_txt
        self.main_url = main_url
        self.if_states = if_states
        self.grab_articles = True

    def find_elements_headlines(self):
        driver = self.driver
        xpath = self.xpath
        layer = self.layer
        class_name = self.class_name
        descendant_tag = self.descendant_tag
        class_txt = self.class_txt
        if_states = self.if_states
        main_url = self.main_url
        if self.grab_articles == False:
            self.para_list = []

        if if_state_idx == 0:
            url_list.append(self.main_url)
        else:
            url_list = self.articles_urls
        for the_url in url_list:
            if self.grab_articles == True:
                get_att = 'href'
                if_state_idx = 0
                the_url = main_url
                driver.get(the_url)
            else:
                get_att = 'p'
                if_state_idx = 1
                driver.get(the_url)
            xpath = ".//descendant::{descendant_tag}[@{class_name}='{class_txt}']/{layer}".format(descendant_tag=descendant_tag,class_name=class_name,class_txt=class_txt,layer=layer)
            elements = driver.find_elements(By.XPATH,xpath)
            for element in elements:
                item = element.get_attribute(get_att)
                info = []
                paras = []
                condition = if_states[if_state_idx]
                if condition:
                    if item not in info or item not in paras:
                        if get_att == 'p':
                            self.para_list.append(item.text)
                        if get_att == 'href':
                            self.articles_urls.append(info)
            if get_att == "p":
                p_dict = {"art_url":item,"paras":paras}
                self.para_list.append(p_dict)
            self.grab_articles = False
        if get_att == "p":
            return self.para_list
        if get_att == "href":
            return self.articles_urls
