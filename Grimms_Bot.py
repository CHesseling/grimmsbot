#%%
# coding: utf-8

import tweepy
import requests
import json
from bs4 import BeautifulSoup
import re
from tweepy import OAuthHandler
#from tweepy.streaming import StreamListener
from string import ascii_lowercase
import pandas as pd
import numpy as np
import time
from PIL import Image
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


# In[3]:


consumer_key = os.getenv('twitter_consumer_key')
consumer_secret = os.getenv('twitter_consumer_secret')
access_token = os.getenv('twitter_access_token')
access_secret = os.getenv('twitter_access_secret')

 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


# In[19]:


def texttopic(wort2, id2):
    font = ImageFont.truetype("RobotoCondensed-Regular.ttf",40)
    font2 = ImageFont.truetype("RobotoCondensed-Regular.ttf",20)
    img=Image.new("RGBA", (440,220),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.text((220, 180), "#GrimmsWort",(0,0,0),font=font2)
    draw.text((45, 30), wort2,(0,0,0),font=font)
    draw = ImageDraw.Draw(img)
    #dateiname = "wort_{}.png".format(wort2) 
    dateiname = "wort.png"
    img.save(dateiname)


# In[4]:


df = pd.read_csv('woerter.csv')


# In[5]:


df["tweeted"] = ""
df["Index"] = df["lemid"]
df.set_index('Index', inplace=True)


# In[6]:


df2 = df


# In[21]:


while len(df2) > 0:
    df_sample = df2.sample()
    wort = df_sample.iloc[0]['match']
    wort_id = df_sample.iloc[0]['lemid']
    texttopic(wort, wort_id)
    adresse = 'http://woerterbuchnetz.de/cgi-bin/WBNetz/wbgui_py?sigle=DWB&mode=Vernetzung&hitlist=&patternlist=&lemid={}'.format(wort_id)
    meldung = "#GrimmsWort: {} \n\n\nMehr: {}".format(wort,adresse)
    #    filename = "wort_{}.png".format(wort)
    filename = "wort.png"

    #print (meldung)
    api.update_with_media(filename, status=meldung)
    bla = str(wort_id)
    #df2[df2.lemid != bla]
    df2 = df2.drop([bla])
    #print ("Dropped", bla)
    df2.to_csv('woerter.csv')
    time.sleep(3600)


# In[20]:




