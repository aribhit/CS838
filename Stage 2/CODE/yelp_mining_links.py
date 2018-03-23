
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib.request
import re


# In[22]:


Yelp_restaurants = []
for num in range(0,1000,10):
    str1 = "https://www.yelp.com/search?find_loc=New+York,+NY&start="
    str2 = "&sortby=rating&attrs=RestaurantsPriceRange2.1&ed_attrs=RestaurantsPriceRange2.2,RestaurantsPriceRange2.3,RestaurantsPriceRange2.4"
    resp = urllib.request.urlopen(str1+str(num)+str2)
    soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
    temp = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith("/biz") and "hrid" not in link['href']  :
            if link["href"] not in temp :
                temp.append(link["href"])
    Yelp_restaurants.extend(temp)
print(len(Yelp_restaurants))
    


# In[24]:


for num in range(0,1000,10):
    str1 = "https://www.yelp.com/search?find_loc=New+York,+NY&start="
    str2 = "&sortby=rating&attrs=RestaurantsPriceRange2.2&ed_attrs=RestaurantsPriceRange2.3,RestaurantsPriceRange2.4,RestaurantsPriceRange2.1"
    resp = urllib.request.urlopen(str1+str(num)+str2)
    soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
    temp = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith("/biz") and "hrid" not in link['href']  :
            if link["href"] not in temp :
                temp.append(link["href"])
    Yelp_restaurants.extend(temp)
    if num%100 == 0 :
        print(num)
print(len(Yelp_restaurants))


# In[25]:


for num in range(0,1000,10):
    str1 = "https://www.yelp.com/search?find_loc=New+York,+NY&start="
    str2 = "&sortby=rating&attrs=RestaurantsPriceRange2.3&ed_attrs=RestaurantsPriceRange2.4,RestaurantsPriceRange2.1,RestaurantsPriceRange2.2"
    resp = urllib.request.urlopen(str1+str(num)+str2)
    soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
    temp = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith("/biz") and "hrid" not in link['href']  :
            if link["href"] not in temp :
                temp.append(link["href"])
    Yelp_restaurants.extend(temp)
    if num%100 == 0 :
        print(num)
print(len(Yelp_restaurants))


# In[26]:


for num in range(0,1000,10):
    str1 = "https://www.yelp.com/search?find_loc=New+York,+NY&start="
    str2 = "&sortby=rating&attrs=RestaurantsPriceRange2.4&ed_attrs=RestaurantsPriceRange2.1,RestaurantsPriceRange2.2,RestaurantsPriceRange2.3"
    resp = urllib.request.urlopen(str1+str(num)+str2)
    soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
    temp = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith("/biz") and "hrid" not in link['href']  :
            if link["href"] not in temp :
                temp.append(link["href"])
    Yelp_restaurants.extend(temp)
    if num%100 == 0 :
        print(num)
print(len(Yelp_restaurants))

