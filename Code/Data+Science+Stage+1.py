
# coding: utf-8

# In[490]:


import re
import random
import pandas as pd
import numpy as np
import sklearn
import statistics
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn import svm 
from sklearn.tree import DecisionTreeClassifier


# In[491]:


def featureCheck(list1, list5):
    finalRes = []
    positive_list = ["honda","chevrolet","toyota","nissan","jaguar","fiat","ford","chrysler","bmw",
                 "mercedes","mercedes-benz","kia","hyundai","gm","audi","volkswagen","mazda", "lexus","subaru"]               
    
    #final_negative_list = negative_list + negative_list1 + negative_list2 + negative_list3 + negative_list4
    
    for x in range(0,len(list5)):
        res = []
        # Feature to tell if previous word is the.
        if list5[x][0] - 1 >= 0 and list1[list5[x][0] - 1].lower() =='the':
            res.append(1)
        else:
            res.append(0)
            
        # Feature to tell if previous to previous word is the.
        if list5[x][0] - 2 >= 0 and list1[list5[x][0] - 2].lower() =='the':
            res.append(1)
        else:
            res.append(0)        
        
        #Feature to tell if preious word is year        
        if list5[x][0] - 1 >= 0 and len(list1[list5[x][0] - 1]) == 4 and list1[list5[x][0] - 1].isdigit() :
            res.append(1)
        else:
            res.append(0)
            
        #Feature to tell if next word is year        
        if  list5[x][0] + 1 < len(list1) and len(list1[list5[x][0] + 1]) == 4 and list1[list5[x][0] + 1].isdigit():
            res.append(1)
        else:
            res.append(0)            
           
        #Feature to tell if previous word is the end of sentence
        if list5[x][0] -1 >= 0 :
            text = list1[list5[x][0]-1]
            if(text[-1] == '.'):
                res.append(1)
            else:
                res.append(0)
        else :
            res.append(0)
        
        # Add a feature for whitelist
        if list5[x][1].lower() in positive_list:
            res.append(1)
        else:
            res.append(0)
        
        finalRes.append(res)
        #Total 6 features (As of now 5, 1 needs to be added - whitelist)
    return finalRes


# In[492]:


def createFrame(list1, list2, posFeatList, negFeatList):
    newList = []
    #labels = ['Word','Feature1','Feature2','Feature3','Feature4', 'Feature5', 'Feature6', 'Class']
    
    for i in range(0,len(list1)):
        newList.append((list1[i][1],posFeatList[i][0],posFeatList[i][1],posFeatList[i][2], posFeatList[i][3],
                        posFeatList[i][4],posFeatList[i][5], 1)) 
    
    for i in range(0,len(list2)):
        newList.append((list2[i][1],negFeatList[i][0],negFeatList[i][1],negFeatList[i][2],negFeatList[i][3],negFeatList[i][4],
                        negFeatList[i][5],0))
        
    #df = pd.DataFrame.from_records(newList, columns = labels)
    
    return newList


# In[493]:


path ="C:\\Users\\Owner\\Desktop\\2nd Semester\\Data Science\\Stage 1\\Final Documents\\DevSet\\"
#test_files = random.sample(range(1,220), k=110)
stupid_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
                'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
               'under',"about","upon","these","those","this","that","i","they","them"]
bigDataList = []
for j in range(1,221):
    if True :
        fileIndex = str(j).zfill(3)
        filePath = path + fileIndex + '.txt'         
        F = open(filePath,"r") 
        read_data = F.read()    
        examples = read_data.split()
        examples = [word.strip(" .,;:()") for word in examples]
        neg_examples = []
        pos_examples = []
        
        for i,word in enumerate(examples):
            word = re.sub("\'s","",word)
            word = re.sub("\’s","",word) 
            if 'carMake' in word :
                if word.count("carMake") == 2 :
                    temp = re.sub('<[^>]*>', '',word)
                    pos_examples.append([i,temp])
                else :
                    temp = word+" "+examples[i+1]
                    temp = re.sub('<[^>]*>', '',temp)
                    pos_examples.append([i,temp])
                    examples[i+1] = "__"
            else : #word[0].isupper() and
                if word[0].isupper() and word.lower() not in stupid_words and not (any(ch.isdigit() for ch in word)) :
                    neg_examples.append([i,word])
                    temp2 = examples[i+1] if i<len(examples)-1 else "__"
                    if temp2.lower() not in stupid_words and 'carMake' not in temp2 and not (any(ch.isdigit() for ch in temp2)):
                        if random.random() <1:
                            neg_examples.append([i,word+" "+temp2])              
        featureList1 = featureCheck(examples, pos_examples)
        featureList2 = featureCheck(examples, neg_examples)
        fileList = createFrame(pos_examples,neg_examples,featureList1,featureList2)
        bigDataList.extend(fileList)
        F.close()
labels = ['Word','F1','F2','F3','F4','F5','F6','Class']
df = pd.DataFrame.from_records(bigDataList, columns = labels)


# In[494]:


features = df.columns[1:7]


# In[495]:


clf_m1 = RandomForestClassifier(n_jobs=2, random_state=0)
scores_m1 = cross_val_score(clf_m1, df[features], df['Class'], cv=10, scoring = 'roc_auc')
print(sum(scores_m1) / 10)


# In[496]:


clf_m2 = svm.SVC(kernel='linear', C=1)
scores_m2 = cross_val_score(clf_m2, df[features], df['Class'], cv=10, scoring = 'roc_auc')
print(sum(scores_m2) / 10)


# In[497]:


clf_m3 = LogisticRegression()
scores_m3 = cross_val_score(clf_m3, df[features], df['Class'], cv=10, scoring = 'roc_auc')
print(sum(scores_m3) / 10)


# In[498]:


clf_m5 = LinearRegression()
scores_m5 = cross_val_score(clf_m5, df[features], df['Class'], cv=10, scoring = 'roc_auc')
print(sum(scores_m5) / 10)


# In[499]:


clf_m4 = DecisionTreeClassifier()
scores_m4 = cross_val_score(clf_m4, df[features], df['Class'], cv=10, scoring = 'roc_auc')
print(sum(scores_m4) / 10)


# In[500]:


df['Class'].value_counts()


# In[501]:


df['is_train'] = np.random.uniform(0,1,len(df)) <= 0.8
df.head
train, test = df[df['is_train']==True], df[df['is_train']==False]


# In[502]:


clf = DecisionTreeClassifier(class_weight = 'balanced')

clf.fit(train[features], train['Class'])
preds = clf.predict(test[features])


# In[503]:


sklearn.metrics.precision_score(test['Class'],preds)


# In[504]:


sklearn.metrics.recall_score(test['Class'],preds)


# In[505]:


sklearn.metrics.f1_score(test['Class'],preds)


# In[506]:


path ="C:\\Users\\Owner\\Desktop\\2nd Semester\\Data Science\\Stage 1\\Final Documents\\TestSet\\"
#test_files = random.sample(range(1,220), k=110)
stupid_words = ['a','an','the','have','has','been','was','is','by','to','at','for','in','of','from','like','with','were',
                'are','what','where','how','why','who','it',"it's",'and','but','on',"its",'we','our','over',
               'under',"about","upon","these","those","this","that","i","they","them"]
testDataList = []
for j in range(1,111):
    if True :
        fileIndex = str(j).zfill(3)
        filePath = path + fileIndex + '.txt'         
        F = open(filePath,"r") 
        read_data = F.read()    
        examples = read_data.split()
        examples = [word.strip(" .,;:()") for word in examples]
        neg_examples = []
        pos_examples = []
        
        for i,word in enumerate(examples):
            word = re.sub("\'s","",word)
            word = re.sub("\’s","",word) 
            if 'carMake' in word :
                if word.count("carMake") == 2 :
                    temp = re.sub('<[^>]*>', '',word)
                    pos_examples.append([i,temp])
                else :
                    temp = word+" "+examples[i+1]
                    temp = re.sub('<[^>]*>', '',temp)
                    pos_examples.append([i,temp])
                    examples[i+1] = "__"
            else : #word[0].isupper() and
                if word[0].isupper() and word.lower() not in stupid_words and not (any(ch.isdigit() for ch in word)) :
                    neg_examples.append([i,word])
                    temp2 = examples[i+1] if i<len(examples)-1 else "__"
                    if temp2.lower() not in stupid_words and 'carMake' not in temp2 and not (any(ch.isdigit() for ch in temp2)):
                        if random.random() <1:
                            neg_examples.append([i,word+" "+temp2])              
        featureList1 = featureCheck(examples, pos_examples)
        featureList2 = featureCheck(examples, neg_examples)
        fileList = createFrame(pos_examples,neg_examples,featureList1,featureList2)
        testDataList.extend(fileList)
        F.close()
labels = ['Word','F1','F2','F3','F4','F5','F6','Class']
test_df = pd.DataFrame.from_records(testDataList, columns = labels)


# In[507]:


test_df['Class'].value_counts()


# In[508]:


preds2 = clf.predict(test_df[features])


# In[509]:


sklearn.metrics.precision_score(test_df['Class'],preds2)


# In[510]:


sklearn.metrics.recall_score(test_df['Class'],preds2)


# In[511]:


sklearn.metrics.f1_score(test_df['Class'],preds2)

