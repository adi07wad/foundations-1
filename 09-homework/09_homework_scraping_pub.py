
# coding: utf-8

# ## Scraping Helsingin Sanomat 
# I work there (it's the largest newspaper in Finland) - that's why I wanted to scrape it

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# In[2]:
#This makes webdriver work on a server
from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(chrome_options=options)

# In[3]:


driver.get('https://www.hs.fi/')


# In[4]:
#submitting the "accept cookies"-form

driver.find_element_by_class_name("sccm-button").click()


# In[5]:
#scraping:

article_list = driver.find_elements_by_class_name('full-width')

list_of_article_dicts = []
for each_article in article_list:
    article_dict = {}

    try:
        cat = each_article.find_element_by_class_name('teaser-category')
        print(cat.text)
        article_dict['category'] = cat.text
    except:
        article_dict['category'] = "NaN"

    head = each_article.find_element_by_tag_name('h2')
    article_dict['headline'] = head.text
    print(head.text)
    
    url_cont = each_article.find_element_by_class_name('teaser-main-article')    
    article_dict['url'] = url_cont.get_attribute('href')
            
    list_of_article_dicts.append(article_dict)
    
    


# In[6]:


list_of_article_dicts


# In[7]:


import pandas as pd


# In[8]:
#making a dataframe

df = pd.DataFrame(list_of_article_dicts)
pd.set_option('display.max_colwidth', -1)
df.head()


# In[9]:


import datetime
right_now = datetime.datetime.now()
date_string = right_now.strftime("%Y-%B-%d-%I%p")
right_now
date_string
hour_string = right_now.strftime("%I%p")


# In[10]:
#creating a csv-file

df.to_csv("hs_articles"+date_string+".csv", index = False)


# In[11]:


import requests


# In[12]:
#creating e-mail

response = requests.post(
        "https://api.mailgun.net/v3/sandbox9920c0a83293435ba524b7c63a30ba3d.mailgun.org/messages",
        auth=("api", "API_KEY"),
        files=[("attachment", open("hs_articles"+date_string+".csv"))],
        data={"from": "Paivi <pja2123@columbia.edu>",
              "to": ["pja2123@columbia.edu"],
              "subject": "Your "+ hour_string +" briefing on Helsingin Sanomat",
              "text": "Look! There is so much happening in the world! See current Helsingin Sanomat headlines attached."}) 
response.text

