
# coding: utf-8

# In[1]:


import requests


# In[2]:
#get the data for desired location

response = requests.get('https://api.darksky.net/forecast/API_KEY/40.7306,-73.9352')
new_york = response.json()
print(new_york)


# In[3]:


print(new_york.keys())


# In[8]:
#coding the desired forecast info

current_temp = str(new_york['currently']['temperature'])
summary = new_york['minutely']['summary'].lower()
temp_high = str(new_york['daily']['data'][0]['temperatureHigh'])
temp_low = str(new_york['daily']['data'][0]['temperatureLow'])

temp_feeling = []
if float(temp_high) > 80:
    temp_feeling.append("a hot day")
elif temp_high > 70:
    temp_feeling.append("a warm day")
elif temp_high > 60:
    temp_feeling.append("a moderate day")
else:
    temp_feeling.append("a cold day")

rain_warning =[] 
rain_prob = new_york['daily']['data'][0]['precipProbability'] 
if rain_prob > 50:
    rain_warning.append("It probably rains, so remember your umbrella.")
else:
    rain_warning.append("")


# In[9]:
#creating the forecast sentence

message = "Right now it is " + current_temp + " degrees out and " + summary + " Today will be " + temp_feeling[0] + " with a high of "+ temp_high + " and a low of " + temp_low+"." + rain_warning[0]
message


# In[6]:


import datetime
right_now = datetime.datetime.now()
date_string = right_now.strftime("%Y-%B-%d")
right_now
#date_string


# In[7]:

#making the email

response = requests.post(
        "https://api.mailgun.net/v3/sandbox9920c0a83293435ba524b7c63a30ba3d.mailgun.org/messages",
        auth=("api", "API_KEY"),
        data={"from": "Paivi <pja2123@columbia.edu>",
              "to": ["pja2123@columbia.edu"],
              "subject": "8AM Weather forecast for "+ date_string,
              "text": message}) 
response.text

