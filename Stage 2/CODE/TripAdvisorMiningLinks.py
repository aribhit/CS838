
# coding: utf-8

# In[1]:


import urllib.request
from bs4 import BeautifulSoup
resp = urllib.request.urlopen("https://www.tripadvisor.com/RestaurantSearch-g60763-p1-New_York_City_New_York.html#EATERY_LIST_CONTENTS")
soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
tripAdvisor_restaurants = []
temp = []
flag = True
strFinal = ""
for num in range(30,2000,30):
    if flag:
        strFinal = "https://www.tripadvisor.com/RestaurantSearch-g60763-p1-New_York_City_New_York.html#EATERY_LIST_CONTENTS"
        flag = False
    else:
        s1 = "https://www.tripadvisor.com/RestaurantSearch-g60763-"
        s2 = "oa" + str(num)
        s3 = "-p1-New_York_City_New_York.html#EATERY_LIST_CONTENTS"
        strFinal = s1+s2+s3
    resp = urllib.request.urlopen(strFinal)
    soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
            if link['href'].startswith("/Restaurant_Review-") and "#REVIEWS" not in link['href']  :
                if link["href"] not in temp:
                    temp.append(link["href"])
    tripAdvisor_restaurants.extend(temp)


temp = []
flag = True
strFinal = ""
for num in range(30,2000,30):
    if flag:
        strFinal = "https://www.tripadvisor.com/RestaurantSearch-g60763-p6-New_York_City_New_York.html#EATERY_LIST_CONTENTS"
        flag = False
    else:
        s1 = "https://www.tripadvisor.com/RestaurantSearch-g60763-"
        s2 = "oa" + str(num)
        s3 = "-p6-New_York_City_New_York.html#EATERY_LIST_CONTENTS"
        strFinal = s1 + s2 + s3
    resp = urllib.request.urlopen(strFinal)
    soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
            if link['href'].startswith("/Restaurant_Review-") and "#REVIEWS" not in link['href']  :
                if link["href"] not in temp:
                    temp.append(link["href"])
    tripAdvisor_restaurants.extend(temp)
    

thefile = open('tripadvisor.txt', 'w+')
for item in tripAdvisor_restaurants:
  thefile.write("%s\n" % item)
thefile.close()

