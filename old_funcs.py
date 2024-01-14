
# def grab_menu_url_links():
#     url = "https://www.timesofisrael.com/"  
#     REGEX = RegexThatURLOhYeah()
#     clipped_url = REGEX.extract_domain_name(url)

#     headers = {
#                 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#                     'Accept-Encoding': 'none',
#                     'Accept-Language': 'en-US,en;q=0.8',
#                     'Connection': 'keep-alive'
#                 } 
#     req = urllib.request.Request(url=url, headers=headers)

#     with urllib.request.urlopen(req) as response:
#         html_content = response.read().decode('utf-8')
#     with open('new.html','w',encoding="utf-8") as w:
#         w.write(html_content)
#         w.close()


#     html_lines = []
#     with open('new.html', "r",encoding="utf-8") as f:
#         for line in f.readlines():
#             html_lines.append(line)
#         f.close()

#     ct = 0
#     for html_string in html_lines:
#         attributes = REGEX.extract_attributes_from_html(html_string)
#         # print(attributes)
#         results = REGEX.find_tag_with_main(html_string)
#         for result in results:
#             if (("menu" and "main" in result.lower())and("http" not in result.lower())):
#                 ct += 1
#                 if ct == 1:
#                     html_tag = result

#     extracted_attributes = REGEX.xtract_attributes_from_html(html_tag)

#     for element_name, attr_dict in extracted_attributes:

#         if len(attr_dict) == 1:
#             # print("One Quotation Group Attribute:")
#             for attr_name, attr_value in attr_dict.items():
#                 XPATH_NAME = attr_name
#                 XPATH_STR = attr_value
#         elif len(attr_dict) == 2:
#             # print("Two Quotation Group Attributes:")
#             for attr_name, attr_value in attr_dict.items():

#                 XPATH_NAME = attr_name
#                 XPATH_STR = attr_value
#         else:
#             print("Invalid Attribute Configuration")

#     tree = html.fromstring(html_content)

#     main_menu_elements = tree.xpath('//*[@{XPATH_NAME}="{XPATH_STR}"]'.format(XPATH_NAME=XPATH_NAME,XPATH_STR=XPATH_STR)) #tag_name=tag_name, //*[@id="HNAV"]

#     href_pattern = re.compile(r'href="(.*?)"', re.IGNORECASE)

#     href_links = []
#     ct = 1
#     for main_menu in main_menu_elements:
#         element_text = main_menu.text_content()
#         # print(element_text)
#         href_links = href_pattern.findall(element_text) 
#         for element in main_menu:
#             for e in element:
#                 href_link = e.xpath('.//a/@href')
#                 signsin = ["sign-in","sign-up"]
#                 for h in href_link:
#                     if((".com" in h)
#                         and("www" in h)
#                         and(h not in href_links)
#                         and(h not in str for str in signsin)
#                         and(clipped_url == REGEX.extract_domain_name(h))):
#                         # print("hrefs:",h)    
#                         if ct <= 3:
#                             href_links.append(h)
#                             ct+=1
#                             print(h)
#             pass
#     return href_links

    # def find_navmenu(self,input_str):
    #     """
    #     header
    #     nav
    #     main menu
    #     container(?)
    #     """
    #     match = re.search(r'<[^>]*(\bmain\b.*\bmenu\b|\bmenu\b.*\bmain\b)[^>]*>', input_str)
    #     if match:
    #         return match.group()
    #     return None
    # def find_tag_with_main(self,input_str):
    #     matches = re.findall(r'<[^>]+>', input_str)
    #     return matches
    # def find_html_tag_names(self,input_str): 
    #     pattern = r'<(\w+)'
    #     return re.findall(self,pattern, input_str)
    # def extract_values_within_quotes(self,tag):
    #     pattern = r'(["\'])(.*?)\1'
    #     matches = re.findall(pattern,tag)
    #     captured_values = [match[1] for match in matches]
    #     return captured_values
    # def extract_attributes_from_html(self,html_text):
    #     pattern = r'<(\w+)(.*?)>'
    #     matches = re.findall(pattern, html_text)
    #     attributes = []
    #     for match in matches:
    #         element_name, attributes_text = match
    #         attr_matches = re.findall(r'(\w+(?:-\w+)?)\s*=\s*["\'](.*?)["\']', attributes_text)
    #         attr_dict = {}
    #         for attr_match in attr_matches:
    #             attr_name, attr_value = attr_match
    #             attr_dict[attr_name] = attr_value
    #         attributes.append((element_name, attr_dict))
    #     return attributes

    # def navigate_articles_list_webpage(self,article_list_webpage,request_sleep_time=2):

    #     """
    #     scrolls page and clicks "load more". will modify this later so it can be agnostic to the website.
    #     want to also add functionality to search if it's a load more button, a next page button, or neither.
    #     """
    #     navigate_list = ["load_more_button","next_page_button"]
    #     for i in navigate_list:
    #         if i == "load_more_button":
    #             driver = get_selenium_driver(minimize=False)
    #             try:
    #                 driver.get(article_list_webpage)
    #                 driver.implicitly_wait(request_sleep_time)
    #             except Exception as error:
    #                 print("errorR:: ",error)
    #             elements = driver.find_elements(By.CSS_SELECTOR,"a")
    #             driver.implicitly_wait(request_sleep_time)
    #             # ct = 0
    #             # while ct <= 5:
    #             #     driver.execute_script("arguments[0].scrollIntoView();",driver.find_element(By.XPATH,".//descendant::div[@class='item load-more']/a"))
    #             #     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ".//descendant::div[@class='item load-more']/a"))).click()
    #             #     time.sleep(2)
    #             #     ct+= 1

                                # unwanted = ["sign-in","sign-up","/contact/","/terms/","/privacy/","liveblog","/writers/","/tag/","/podcasts/",'/entertainment/','/navigational-sitemap/',
                                #             'the-media/', '/economy/', '/europe/', '/border/', '/middle-east/', '/africa/','/asia/', '/latin-america/', '/world-news/','/politics/' ,
                                #             '/video/', '/tech/', '/sports/', '/on-the-hill-exclusive-video/','/newsletters/', '/people/', '/masthead/', '/accessibility-statement/', 
                                #             '/policy-information/', '/terms-of-use/', '/privacy-policy/', '/mediakit/', '/contact-us/', '/jobs/', '/careers/','/app/', '/send-a-tip/',
                                #             '/about/','/jewish-times/', '/israel-inside/', '/tech-israel/', '/real-estate-israel/', '/the-daily-edition/', '/tech-israel-signup/',
                                #             '/real-estate-israel-signup/','/the-weekend-edition/','/the-blogs-edition/','/local/','/advertise/','/jobs-at-the-times-of-israel/',
                                #             "twitter.com","/topic/","/author/","/clips/"] 
                                # unwanted = unwanted + self.additional_unwanted
                                # print("before:",unwanted)
                                # add_back = []
                                # menu_topics = self.mainmenu_news_topic
                                # skip_this_one = False
                                # for h in href_link:
                                    # # print("href link here:",h)
                                    # for want in menu_topics:
                                    #     if want in h:
                                    #         if f"/{want}/" in unwanted:
                                    #             while f"/{want}/" in unwanted:
                                    #                 unwanted.remove(f"/{want}/")
                                    #         if f"/{want}/" not in add_back:
                                    #             add_back.append(f"/{want}/")
                                    #         try:
                                    #             if (h.endswith(f"/{want}/")
                                    #                 and(h.endswith(MAIN_URL))):
                                    #                 skip_this_one = True 

                                    #         except:
                                    #             pass
                                    # if skip_this_one == False:
                                        # print("after skip_this_one==False:",h)
                                    # if(h == h.startswith("https://")):   
                                    #     if(GUESS.run_article_guesser_model(url_list=[h] == 1)):
                                    #         print("model predicted it's an article:",h)
                                    #             # build_up_more_url_data.append(h + ",1")
                                    # # and(h.count("/") >=3)
                                    # # # and(h.count("-") >=6) # here is where I would replace with is_article_or_not
                                    # # # and((REGEX.unwanted_from_links(href=h,unwanted=unwanted)==True))
                                    # # and(h != theurl)
                                    # # # amd(h != the_url)
                                    # # and(clipped_url == REGEX.extract_domain_name(h))
                                    #         if(clipped_url == REGEX.extract_domain_name(h)):
                                    #     # and(h.strip() != MAIN_URL.strip())
                                    #     # and(h not in inner_href_links)
                                    #     # and(h not in ult_url_list)
                                    #     # and(h not in url_list)):
                                    #     #             # print("h here:",h)
                                    #     #     # for content in self.article_headline_content_type:
                                    #             if h not in inner_href_links:
                                    #                 # print("complete:",h)
                                    # #                 print(h)
                                    # #                 inner_href_links.append(h)
                                    #     # catching 'incomplete' links without https:// in them
                                    #     if(h != h.startswith("https://")):
                                    #         if MAIN_URL[-1] == '/':
                                    #             h = MAIN_URL[:-1]+h
                                    #         if MAIN_URL[-1] != '/':
                                    #             h = MAIN_URL + h
                                    #     if(h == h.startswith("https://")):   
                                    #         if(GUESS.run_article_guesser_model(url_list=[h] == 1)):
                                    #             if(clipped_url == REGEX.extract_domain_name(h)):
                                    #                 if h not in inner_href_links:
                                    #                     inner_href_links.append(h)
                                                        # print("incomplete:",full_url)
                                            # if((h.count("/") >=3)
                                            # # and(h.count("-") >=6)
                                            # # and((REGEX.unwanted_from_links(href=h,unwanted=unwanted)==True))
                                            # # and(h.strip() != the_url.strip())
                                            # and(h.strip() != theurl.strip())
                                            # and(h not in inner_href_links)
                                            # and(h not in ult_url_list)
                                            # and(full_url not in inner_href_links)
                                            # and(h not in url_list)): 
                                            #     # for content in self.article_headline_content_type:
                                            #         # if content in h:
                                                # if full_url not in inner_href_links:
                                                #     inner_href_links.append(full_url)
                                                #     # print("incomplete:",full_url)
                                                #     print(full_url)
                                    # skip_this_one = False    
                                    # unwanted = unwanted + add_back