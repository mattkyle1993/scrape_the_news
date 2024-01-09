
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