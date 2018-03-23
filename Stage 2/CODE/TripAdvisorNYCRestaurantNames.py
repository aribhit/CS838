
# coding: utf-8

# In[4]:


import urllib.request
import re
import csv
from bs4 import BeautifulSoup
LastList = []
SiteLink = "https://www.tripadvisor.com"
Path = "C:\\Users\\Owner\\Desktop\\tripadvisor.txt"


# In[5]:


f = open(Path, "r" )
badList = []
NameList = ["Name","Address","Phone","Cuisines","Saturday Opening time","Saturday Closing time","Sunday Opening time","Sunday Closing time","Take Out"]
LastList.append(NameList)
with open(Path,'r') as infile:
    for ResLink in infile:
        FinalLink = SiteLink + ResLink
        try:
            resp = urllib.request.urlopen(FinalLink)
            soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
            CompleteList = []

            #Get Name of the Restaurent
            name = ""
            name = soup.find('h1', class_ = "heading_title")
            name = name.text
            if name:
                CompleteList.append(name)
            else:
                CompleteList.append('NaN')

            #Get Address of the Restaurent
            address = ""
            addressStreetRaw = soup.find('span', class_ = "street-address")
            addressStreet = addressStreetRaw.text.strip(" \t\n")
            addressLocalityRaw = soup.find('span', class_ = "locality")
            addressLocality = addressLocalityRaw.text.strip(" \t\n")
            address = addressStreet + " " + addressLocality
            if address:
                CompleteList.append(address)
            else:
                CompleteList.append('NaN')

            #Get Contact Number of the Restaurent
            contact = soup.find('div', class_ = "blEntry phone")
            contact = contact.text
            res = any(i.isdigit() for i in contact)
            if res:
                CompleteList.append(contact)
            else:
                CompleteList.append('NaN')

            #Get Cuisine list
            finalList = ""
            cuisines = soup.find('span', class_="header_links rating_and_popularity")
            if cuisines:
                cuisines = cuisines.text.strip(" \t\n")
                cuisinesList = re.split(',',cuisines)
                for cuisine in cuisinesList:
                    cuisine = cuisine.strip()
                    finalList = finalList + cuisine + ";"
                finalList = finalList[:-1]
            if finalList:
                CompleteList.append(finalList)
            else:
                CompleteList.append('NaN')

            #Open and close time on Saturday and Sunday
            finalList = {}
            i = 1
            value = ""
            time = soup.find('div', class_="hours content")
            if time:
                time = time.text.strip(" \t\n")
                List = time.split('\n')
                while '' in List: List.remove('')
                while i <= len(List):
                    finalList[List[i-1]] = List[i]
                    i = i+2
            #Saturday content starts here
            opening = 'NaN'
            closing = 'NaN'
            if 'Saturday' in finalList.keys():
                Saturday = finalList['Saturday']
                Time = Saturday.split('-')
                opening = Time[0].strip()
                closing = Time[1].strip()
                CompleteList.append(opening)
                CompleteList.append(closing)
            else:
                CompleteList.append(opening)
                CompleteList.append(closing)
            #Saturday content ends here

            #Sunday content starts here
            opening = 'NaN'
            closing = 'NaN'
            if 'Sunday' in finalList.keys():
                Sunday = finalList['Sunday']
                Time = Sunday.split('-')
                opening = Time[0].strip()
                closing = Time[1].strip()
                CompleteList.append(opening)
                CompleteList.append(closing)
            else:
                CompleteList.append(opening)
                CompleteList.append(closing)
            #Sunday content ends here

            #Take out
            flag = False
            takeOut = soup.find_all('div', class_="details_tab")
            for take in takeOut:
                take1 = str(take)
                if 'Takeout' in take1 or 'takeout' in take1:
                    CompleteList.append("Yes")
                    flag = True
                    break
            if flag!=True:
                CompleteList.append("No")

            #Final List of Contents
            LastList.append(CompleteList)
        except:
            badList.append(FinalLink)


# In[6]:


filename = "TripAdvisorNYCRestaurants.csv"
with open(filename,'w',newline='') as f:
        w = csv.writer(f)
        for List in LastList:
            w.writerow(List)

