
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd


# In[ ]:


counter = 0
dintwork= []
Table = []
with open("yelprestaurants.txt",'r') as infile:
    for line in infile:
        print(counter)
        counter+=1
        link  = line
        try :
            resp = urllib.request.urlopen(link)
            soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
            name = soup.find('h1', class_ ="biz-page-title embossed-text-white")
            if not name :
                name = soup.find('h1', class_ ="biz-page-title embossed-text-white shortenough")    
            name = name.text.strip(" \t\n")
            name = re.sub(",","",name)
            #Names.append(name)
            adrs = soup.find('address')
            adrs = adrs.text.strip(" \t\n")
            adrs = re.sub(",","",adrs)
            #Address.append(adrs)
            phone = soup.find('span', class_ ="biz-phone")
            phone = phone.text.strip(" \t\n")
            phone = re.sub(",","",phone)
            #Phone.append(phone)
            cuisines = soup.find('span', class_ ="category-str-list")
            cuisines = cuisines.text.strip(" \t\n")
            regex = re.compile("\t|\n|,")
            regex2 = re.compile(" {2,}")
            cuisines = re.sub(regex,"",cuisines)
            cuisines = re.sub(regex2,";",cuisines)
            #Cuisines.append(cuisines)
            table = soup.find('table', {'class': "table table-simple hours-table"})
            times = {}
            for week in ['Mon',"Tue","Wed","Thu","Fri","Sat","Sun"] :
                th = table.find('th', text=week)
                td = th.findNext('td')
                td = td.text.strip(" \t\n")
                td = re.sub(",","",td)
                times[week] = td
            #Times.append(times)
            tkout = soup.find('div', class_ ="short-def-list")
            dt = tkout.find_all('dt')
            option = "No"
            for elem in dt :
                if elem.text.strip("\t \n") == "Take-out":
                    dd = elem.findNext("dd")
                    option = dd.text.strip("\t\n ")
                    break
            #Option.append(option)
            Table.append([name,adrs,phone,cuisines,times,option])
            print(name)
        except :
            dintwork.append(link) 


# In[ ]:


Table2 = [(x[0],x[1],x[2],x[3],";".join(list(x[4].values())),x[5]) for x in Table]
df = pd.DataFrame(Table2,columns= ["Name","Address","Phone","Cuisines","Closing times","Take Out"])
df.to_csv("Yelp_table2.csv",index=False)


# In[ ]:


with open("remaining_again.txt",'w+') as outfile :
    outfile.write("\n".join(dintwork))

