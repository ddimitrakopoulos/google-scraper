my_dir='/home/mitsos/Documents/code base/google my bussiness/'

import pandas as pd
import csv
import re
import os
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from time import sleep
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchWindowException
import tkinter as tk
from urllib.parse import urlparse

def set(list, i):
    if(len(list) == 0):
        return "Not Found"
    else:
        return list[i].text 
    
def set_with_html(list, i):
    if(len(list) == 0):
        return "Not Found"
    else:
        return list[i].get_attribute('innerHTML')
    
def set_name_r(list, i):
    if(len(list) == 0):
        return "No Name:"
    else:
        return list[i].get_attribute('innerHTML')

def get_first_line(string):
    lines = string.split('\n')
    if lines:
        return lines[0]
    else:
        return "Not Found" 
    
def categorize_social_media(url):
    # Dictionary mapping domain names to social media platform names
    social_media_domains = {
        'facebook.com': 'Facebook',
        'twitter.com': 'Twitter',
        'instagram.com': 'Instagram',
        'linkedin.com': 'LinkedIn',
        'youtube.com': 'YouTube',
        'tiktok.com': 'TikTok',
        # Add more social media domains as needed
    }
    
    # Parse the URL to extract the domain name
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Check if the domain belongs to any known social media platform
    for social_domain, platform in social_media_domains.items():
        if social_domain in domain:
            return platform
    
    # If the domain doesn't match any known social media platform, return None
    return None

def get_specific_column(csv_file, row_number, column_number):
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i == row_number:
                if column_number < len(row):
                    return row[column_number]
                else:
                    return 'Not Found'
        return 'Not Found'
    
def get_social(s):
    start_index = s.find('href="')
    if start_index == -1:
        return None  
    start_index += len('href="')  
    end_index = s.find('"', start_index) 
    if end_index == -1:
        return None  
    return s[start_index:end_index] 

def set_link(list, i):
    if(len(list)==0):
        return "Not Found"
    else:
        url_string = list[i].get_attribute("innerHTML")
        start_index = url_string.find("url=")
        substring_after_url = url_string[start_index + len("url="):]
        end_index = substring_after_url.find('"')
        extracted_url = substring_after_url[:end_index]
        if(extracted_url==""):
            extracted_url="Not Found"
        return extracted_url

def phone_transform(phone):
    pattern = r'\(([^)]*)\)[^\d]*(\d)(\d*)'
    match = re.search(pattern, phone)
    if match:
        part_inside_parentheses = match.group(1)
        digit_after_parentheses = match.group(2)
        rest_of_digits = match.group(3)
        return (part_inside_parentheses + digit_after_parentheses + rest_of_digits)[1:]
 
def scr_transform(phone):
    return phone[4:].replace(" ","")

def compare_phone(csv_file, scraped_info, i):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for _ in range(i - 1):
            next(reader)
        target_row = next(reader)
        phone1 = str(phone_transform(target_row[2])) 
        phone2 = str(phone_transform(target_row[3]))  
        phone3 = str(phone_transform(target_row[4]))  
    scraped_phone = str(scr_transform(scraped_info[i-1][2]))
    if(phone1 == scraped_phone or phone2 == scraped_phone or phone3 == scraped_phone):
        return True
    else:
        return False
    
def compare_phone2(csv_file, scraped_info, i, j):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for _ in range(i - 1):
            next(reader)
        target_row = next(reader)
        phone1 = str(phone_transform(target_row[2])) 
        phone2 = str(phone_transform(target_row[3]))  
        phone3 = str(phone_transform(target_row[4]))  
    scraped_phone = str(scr_transform(scraped_info[j][2]))
    if(phone1 == scraped_phone or phone2 == scraped_phone or phone3 == scraped_phone):
        return True
    else:
        return False

def address_transform(address):
    add = address.replace(" ","").replace("\n","")
    add = re.sub(r'[^a-zA-Z0-9]', '', add)
    return add

def address_transform2(address):
    add = re.sub(r'\s+', ' ', address)
    add = re.sub(r'(?<=[a-zA-Z0-9])\s+', ' ', add)
    return add

def similarity_score(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1
    max_len = max(m, n)
    similarity = 1 - dp[m][n] / max_len
    return similarity

def compare_address(csv_file,scraped_info,i):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for _ in range(i - 1):
            next(reader)
        target_row = next(reader)
        address = address_transform(target_row[5])
    scraped_address = address_transform(scraped_info[i-1][1])
    s = similarity_score(address,scraped_address)
    s2 = False
    if(s>0.2):
        s2 = True
    return [s, s2]

def compare_address2(csv_file,scraped_info,i, j):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for _ in range(i - 1):
            next(reader)
        target_row = next(reader)
        address = address_transform(target_row[5])
    scraped_address = address_transform(scraped_info[j][1])
    s = similarity_score(address,scraped_address)
    s2 = False
    if(s>0.27):
        s2 = True
    return [s, s2]

def compare_name(csv_file,scraped_info,i):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for _ in range(i - 1):
            next(reader)
        target_row = next(reader)
        name = target_row[0]
    scraped_name = scraped_info[i-1][0]
    s = similarity_score(name,scraped_name)
    s2 = False
    if(s>0.5):
        s2 = True
    return [s, s2]

def compare_name2(csv_file,scraped_info,i, j):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for _ in range(i - 1):
            next(reader)
        target_row = next(reader)
        name = target_row[0]
    scraped_name = scraped_info[j][0]
    s = similarity_score(name,scraped_name)
    s2 = False
    if(s>0.5):
        s2 = True
    return [s, s2]

def categorize(info):
    r = ""
    a = 0
    if(info[12]==True or (info[3]==True and info[15]==True)):
        r += "Account Exists: "
    else:
        r += "Different Account: "
    if(info[12]!=True):
        if(info[11]!="Not Found"): 
            r+="Different Phone "
    if(info[15]!=True):
        a += 1
        r += "Different Address "
    if(info[3]!=True):
        a += 1
        r += "Different Name "
    if(info[21]=="Not Found"):
        a += 1
        r += "No Hours Open "
    if(info[19]=="Not Found"):
        a += 1
        r += "No Website "
    if(info[11]=="Not Found"):
        a += 1
        r += "No Phone"
    if(r == "Account Exists: "):
        r += "All Done"
    if(a == 5):
        r = "No Account Found"
    return r

def update_label():
    label.config(text=f"Checked: {i} out of {x} entries")

def increment():
    global i
    global x
    i = i + 1
    update_label()

def characters_before_in(string):
    index = string.find('in')
    if index != -1:
        return string[:index]
    else:
        return string

options = webdriver.ChromeOptions() 
#options.add_experimental_option("detach", True)
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_extension(my_dir+'captcha.crx')
options.add_argument("--lang=de-DE")
#options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False) 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
initial_file = my_dir+'input.xlsx'
input_file = my_dir+'input_file.csv'
df = pd.read_excel(initial_file)
df.to_csv(input_file, index=False)
data_list = []
url_list = []
url2 = []
scraped_info= []
check_again = []
scraped_info2 = []
index = []
proxy_cookie = False
output = [['Category','Name', 'Scraped Name', 'Match','Percentage','Email','Industry','Scraped Industry','Phone1', 'Phone2',
            'Phone3','Scraped Phone','Match','Address', 'Scraped Address','Match', 'Percantage', 
            'Generated Url', 'Website','Scraped Website','Products/Services','Hours Open','Available Booking', 'Live Tracking', 
            'Peak Hours','Ratings', 'Are You the owner?','News','Contact','Questions and Answers','Photos','Social Media', 
            "Suggest Changes", "Booklink"]]
pattern = r'\(([^)]*)\)[^\d]*(\d)(\d*)'
input_csv_file = my_dir+'input_file.csv'

with open(input_csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        name = row[0] if len(row) > 0 else None
        address = row[5] if len(row) > 5 and row[5] != '' else 'Not Found'
        address_for_url = address_transform2(address)
        data_list.append([name, address_for_url])

for entry in data_list:
    encoded_address = quote(entry[1])
    encoded_name = quote(entry[0], safe='')
    url = f"http://www.google.com/search?q={encoded_name}+{encoded_address}"
    url_list.append(url)
    url = f"http://www.google.com/search?q={encoded_name}"
    url2.append(url)

i = 0
x = len(url_list)
root = tk.Tk()
root.title("Progress")

try:
    while(len(url_list)> i):
        driver.get(url_list[i])
        if(i==0):
            driver.maximize_window()
            label = tk.Label(root, text=f"Checked: {i} out of {x} entries")
            label.pack(pady=10)
            #time.sleep(45)
        captcha = driver.find_elements("xpath",'//form[contains(@id,"captcha-form")]')
        if(captcha==[]):
            no_cookies = driver.find_elements("xpath", '//div[contains(@class,"QS5gu sy4vM")]')
            if(no_cookies!=[]):
                no_cookies[0].click()
            name_list = driver.find_elements("xpath", '//h2[contains(@class,"qrShPb pXs6bb PZPZlf q8U8x aTI8gc hNKfZe")]') 
            if(name_list==[]):
                name_list = driver.find_elements("xpath", '//div[contains(@class,"SPZz6b")]')
                if(name_list==[]):
                    name_list = driver.find_elements("xpath", '//div[contains(@class,"PZPZlf ssJ7i")]')
                name = get_first_line(set(name_list,0))
            else:
                name = set(name_list,0)
            address_list=driver.find_elements("xpath",'//div[contains(@class,"gqkR3b hP3ybd")]')
            if(address_list == [] and name_list!=[]):
                address_list=driver.find_elements("xpath",'//span[contains(@class,"LrzXr")]')                
            address = set(address_list, 0)
            phone_list=driver.find_elements("xpath",'//span[contains(@class,"LrzXr zdqRlf kno-fv")]')
            phone = set(phone_list,0)
            if(name=='Not Found' and phone=='Not Found' and address=='Not Found'):
                if(url_list[i]!=url2[i]):    
                    url_list[i]=url2[i]
                else:
                    website = 'Not Found'
                    products = 'Not Found'
                    hours_open = 'Not Found'
                    available_booking = 'Not Found'
                    live_tracking = 'Not Found'
                    peak_hours = 'Not Found'
                    google_rating = 'Not Found'
                    are_you_the_owner = 'Not Found'
                    from_tab = 'Not Found'
                    contact = 'Not Found'
                    qna = 'Not Found'
                    closed = 'Not Found'   
                    photo = 'Not Found'
                    category = 'Not Found'
                    social = 'Not Found'
                    sug = 'Not Found'
                    scraped_info.append([name, address, phone, website, products, 
                                         hours_open, closed, available_booking, live_tracking, 
                                         peak_hours, google_rating, are_you_the_owner,
                                         from_tab, contact, qna, photo, category,social,sug])
                    increment()
            else:
                website_list = driver.find_elements("xpath",'//div[contains(@class,"IzNS7c duf-h")]')
                if(website_list==[]):
                    website_list = driver.find_elements("xpath",'//div[contains(@jsname,"UXbvIb")]')
                    if(website_list!=[]):
                        try:
                            website = set_link(website_list,0)
                            if(website == 'v class=' or website == 'v jsmodel='):
                                website = 'Not Found'
                        except:
                            website='Not Found'
                    else:
                        website='Not Found'
                else:
                    website = set_link(website_list,0)
                times_button = driver.find_elements("xpath",'//span[contains(@class,"BTP3Ac")]')
                if(times_button != []):
                    times_button[0].click()
                    table = driver.find_elements("xpath",'//table[contains(@class,"WgFkxc")]')
                    hours = table[0].find_elements("xpath", '//td')
                    hours_open = ''
                    for b in range(0,len(hours)):
                        if(b%2==0):
                            hours_open += hours[b].get_attribute('innerHTML') +' '
                        else:
                            hours_open += hours[b].get_attribute('innerHTML')
                            if(b!=len(hours)-1):
                                hours_open += '\n'
                elif(True):
                    hours_open = ''
                    times_button = driver.find_elements("xpath",'//span[contains(@class,"XCdOnb")]')
                    if(times_button != []):
                        times_button[0].click()
                        names = driver.find_elements("xpath",'//div[contains(@class,"xMiPL")]')
                        table = driver.find_elements("xpath",'//table[contains(@class,"WgFkxc CLtZU")]')
                        for a in range(0,len(names)):
                            hours_open += names[a].get_attribute('innerHTML')
                            hours_open += "\n"
                            hours = table[0].find_elements("xpath", '//td')
                            for b in range(a*14,(a+1)*14):
                                if(b%2==0):
                                    hours_open += hours[b].get_attribute('innerHTML') +' '
                                else:
                                    hours_open += hours[b].get_attribute('innerHTML')
                                    if(a != len(names) - 1 or b != len(names)*14 - 1):
                                        hours_open += '\n'
                if(hours_open == ''):
                    hours_open = 'Not Found'
                closed = str(driver.find_elements("xpath", '//span[contains(@class,"hBA2d Shyhc")]') != [])
                available_booking = str(driver.find_elements("xpath", '//span[contains(@class,"nuZrJf")]') != [])# VoAujc#KLcE6c
                live_tracking = str(driver.find_elements("xpath", '//div[contains(@class,"W1cfjc")]') != [])
                google_rating_list = driver.find_elements("xpath", '//div[contains(@class,"bBvbCc fUSQwd")]')
                if(google_rating_list == []):
                    google_rating_list = driver.find_elements("xpath", '//span[contains(@class,"Aq14fc")]')
                    google_rating_list.extend(driver.find_elements("xpath", '//span[contains(@class,"inaKse G5rmf")]'))
                name_rating_list = driver.find_elements("xpath",'//span[contains(@class,"xTA1xd")]')
                if(name_rating_list == []):
                    google_rating = ""
                    for s in range(0,len(google_rating_list)):    
                        google_rating += set_with_html(google_rating_list,s)
                        if(s!=len(google_rating_list)-1):
                            google_rating += "\n"
                else:
                    google_rating = ""
                    for s in range(0,len(google_rating_list)):    
                        google_rating += set_name_r(name_rating_list,s) + " " + set_with_html(google_rating_list,s)
                        if(s!=len(google_rating_list)-1):
                            google_rating += "\n"
                are_you_the_owner = str(driver.find_elements("xpath", '//a[contains(@jsname,"cQhrTd")]') != [])
                if(are_you_the_owner == 'False'):
                    are_you_the_owner = str(driver.find_elements("xpath", '//a[contains(@href,"https://business.google.com/create?")]') != [])
                sug = str(driver.find_elements("xpath", '//a[contains(@href,"#")]') != [])
                qna = str(driver.find_elements("xpath", '//span[contains(@class,"QlPmEd")]') != [] or
                          driver.find_elements("xpath", '//a[contains(@jsaction,"QLOnOe")]') != [])
                products = str(driver.find_elements("xpath", '//g-inner-card[contains(@class,"EanVoe wdQNof")]') != [])
                peak_hours_list = driver.find_elements("xpath",'//span[contains(@class,"qzixBd")]')
                peak_hours = set(peak_hours_list,0)
                photo_list = driver.find_elements("xpath",'//div[contains(@class,"luib")]')
                if(photo_list != []):    
                    photo_list = photo_list[0].find_elements("xpath",'//img[contains(@class,"YQ4gaf")]')
                if(len(photo_list) != 0):
                    photo = 'Found'
                else: 
                    photo = 'Not Found'
                contact = str(driver.find_elements("xpath", '//div[contains(@class,"JV5xkf")]') != [])
                from_tab = str(driver.find_elements("xpath", '//span[contains(@class,"FoAEQ")]') != [] or
                               driver.find_elements("xpath", '//div[contains(@jsaction,"click:DITn2")]') != [])
                category_list = driver.find_elements("xpath", '//span[contains(@class,"E5BaQ")]')
                if(set(category_list,0) == 'Not Found' or set(category_list,0) == ''):
                    category_list = driver.find_elements("xpath", '//span[contains(@class,"YhemCb")]')
                category = characters_before_in(set(category_list,0))
                social_list = driver.find_elements("xpath", '//g-link[contains(@class,"fl w23JUc ap3N9d")]')
                if(len(social_list)==0):
                    social = 'Not Found'
                else:
                    social = ''
                    for l in  range(0, len(social_list)):
                        try:    
                            social += categorize_social_media(get_social(str(social_list[l].get_attribute('innerHTML'))))
                            social += ' '
                            social += get_social(str(social_list[l].get_attribute('innerHTML')))
                            if(l != len(social_list)-1):
                                social +='\n'
                        except TypeError as e:
                            social = 'Not Found'
                            continue
                scraped_info.append([name, address, phone, website, products, 
                                     hours_open, closed, available_booking, live_tracking, 
                                     peak_hours, google_rating, are_you_the_owner,
                                     from_tab, contact, qna, photo, category,social,sug])
                increment()
        else:
            time.sleep(45)
        root.update()
except NoSuchWindowException as e:
    print("The browser window was closed manually")

root.destroy()

for i in range(1,len(scraped_info)+1):
    phone_out = compare_phone(my_dir+'input_file.csv',scraped_info,i )
    name_out = compare_name(my_dir+'input_file.csv',scraped_info,i)
    add_out = compare_address(my_dir+'input_file.csv',scraped_info,i)
    info = ['',get_specific_column(my_dir+'input_file.csv',i,0),scraped_info[i-1][0],name_out[1],name_out[0],
            get_specific_column(my_dir+'input_file.csv',i,6),get_specific_column(my_dir+'input_file.csv',i,1),scraped_info[i-1][16],
            get_specific_column(my_dir+'input_file.csv',i,2),get_specific_column(my_dir+'input_file.csv',i,3),
            get_specific_column(my_dir+'input_file.csv',i,4),scraped_info[i-1][2],phone_out,get_specific_column(my_dir+'input_file.csv',i,5),
            scraped_info[i-1][1],add_out[1],add_out[0],url_list[i-1],get_specific_column(my_dir+'input_file.csv',i,7),scraped_info[i-1][3], scraped_info[i-1][4],
            scraped_info[i-1][5],scraped_info[i-1][7], scraped_info[i-1][8],scraped_info[i-1][9], scraped_info[i-1][10], scraped_info[i-1][11],
            scraped_info[i-1][12], scraped_info[i-1][13], scraped_info[i-1][14],scraped_info[i-1][15],scraped_info[i-1][17],
            scraped_info[i-1][18], get_specific_column(my_dir+'input_file.csv',i,8)]
    if(name_out[0]>=0.3 and add_out[1]==True and info[2]!='Not Found'):
        info[3]=True
    if(scraped_info[i-1][6]=='True'):
        info[0]='Closed'
    else:
        info[0] = categorize(info)
    info[13]=address_transform2(info[13])
    output.append(info)

with open(my_dir+'output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(output)

df = pd.read_csv(my_dir+'output.csv')
df = df.apply(lambda x: x.astype(str) if x.dtype == bool else x)
excel_filename = my_dir+'output.xlsx'
df.to_excel(excel_filename, index=False, engine='openpyxl')

os.remove(my_dir+'input_file.csv')