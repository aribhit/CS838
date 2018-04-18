
# coding: utf-8

# # Project Stage 3: Entity Matching#
# 
# The entity we performed our match was on a set of restaurants in New York City. The data for the tables was taken from two different web sources, namely, Tripadvisor and Yelp.
# 
# We used the py_entitymatching package to help in this process.

# In[2]:


# Import py_entitymatching package
import py_entitymatching as em
import os
import pandas as pd


# ## Reading in Input Tables##
# 
# We read the CSV files and set 'ID' as the key attribute.
# 
# Input table A corresponds to data from TripAdvisor, and input table B corresponds to data from Yelp.

# In[3]:


#path_A = 'C:\\Users\\bharg\\Documents\\TripAdvisor_Restaurants.csv'
#path_B = 'C:\\Users\\bharg\\Documents\\Yelp_Restaurants.csv'
path_A = 'C:\\Users\\Aribhit\\TripAdvisor_Restaurants.csv'
path_B = 'C:\\Users\\Aribhit\\Yelp_Restaurants.csv'


# In[4]:


A = em.read_csv_metadata(path_A, key='Id', encoding = 'cp1252')


# In[5]:


B = em.read_csv_metadata(path_B, key='Id', encoding = 'cp1252')


# # Data Pre-processing#
# 
# Since there was a lot of variance in how *Address* attribute was defined, created a new attribute called *Street* that is extracted from *Address* (by considering the part of the string till the state appears).
# 
# Also converted every string type attribute to lower case.

# In[6]:


A['Street'] = A.apply(lambda row : row['Address'][0:row['Address'].find('New')],axis=1)
A['Name']=A['Name'].str.lower()
A['Street']=A['Street'].str.lower()
A['Address']=A['Address'].str.lower()


# In[7]:


def cleaning(row) :
    for string in ['New','Jersey','NY','NJ']:
        index = row['Address'].find(string)
        if index == -1 :
            continue
        return row['Address'][0:index]
    return row['Address']
    
B['Street'] = B.apply(cleaning,axis =1)
B['Name']=B['Name'].str.lower()
B['Street']=B['Street'].str.lower()
B['Address']=B['Address'].str.lower()


# Deleting *Phone* attribute in case it might act as an unique ID and game the system

# In[8]:


del A['Phone']
del B['Phone']


# ## Applying the Blocker##
# 
# We have used the combination of two blockers: 
# One blocks based on *Name* of the restaurant (Jaccard Measure with 3 grams with a constraint 0.3) and *Street* (Jaccard Measure with 3 grams with a constraint 0.3). 
# Next blocker is only on the *Street* attribute(Jaccard Measure with 3 grams with a constraint 0.6).
# 
# We use these blockers and then combine the results of two different blockers using union for the following reasons.
# *Street* (from *Address*) only because it can capture some pairs where names are same but differ by a new word. Ex. (alfa ristorante, alfa). The constraint is higher - 0.6
# *Name* only to capture restaurants that have similar names (constraint is 0.3). But added *Street* based rule on top of that to eliminate chain restaurants with multiple branches at different locations (eg: Shake shacks at Manhattan, Shake Shacks at Brooklyn). The constraint is lower threshold in this case compared to the earlier blocker.
# 
# First, get all possible features for blocking.

# In[9]:


block_f = em.get_features_for_blocking(A, B, validate_inferred_attr_types=False)


# First rule-based blocker uses *Name* and *Street* attributes

# In[10]:


rb = em.RuleBasedBlocker()
ab = em.AttrEquivalenceBlocker()
rb.add_rule(['Name_Name_jac_qgm_3_qgm_3(ltuple, rtuple) < 0.5'], block_f)
rb.add_rule(['Street_Street_jac_qgm_3_qgm_3(ltuple, rtuple) < 0.3'], block_f)


# In[11]:


C = rb.block_tables(A, B, l_output_attrs=['Name', 'Street', 'Address','Cuisines','Take Out'],                     r_output_attrs=['Name', 'Street', 'Address','Cuisines','Take Out'], show_progress=True)


# Second rule-based blocker uses only *Street* attribute

# In[12]:


rb2 = em.RuleBasedBlocker()
rb2.add_rule(['Street_Street_jac_qgm_3_qgm_3(ltuple, rtuple) < 0.6'], block_f)
E = rb2.block_tables(A, B, l_output_attrs=['Name', 'Street', 'Address','Cuisines','Take Out'],                      r_output_attrs=['Name', 'Street', 'Address','Cuisines','Take Out'], n_jobs=-1,show_progress=True)


# Combining blocker1 and blocker2 results to get candidate set C (which is named F in our code).

# In[13]:


F = em.combine_blocker_outputs_via_union([C, E])


# Running debugger to see if F is good. 41/50 outputs of debugger are bad matches.Therefore we are proceeding with the above 
# blocker

# In[14]:


dbg = em.debug_blocker(F, A, B, output_size=50)
dbg.head()


# In[15]:


F.to_csv("F.csv",index=False)


# Taking a sample of 600 tuples from the output, and then we label this sample manually.

# In[16]:


S = em.sample_table(F, 600)
S.to_csv('Sample.csv',encoding = 'cp1252')


# ## Reading the Labelled Sample##
# Loading the labeled data table, which is present in a file called 'Labelled_Sample_v2.csv'

# In[17]:


L = em.read_csv_metadata("Labelled_Sample_v2.csv", key='_id', encoding = 'cp1252',                         ltable=A, rtable=B,fk_ltable='ltable_Id', fk_rtable='rtable_Id')


# Deleting *Phone* attribute again, because it can help determine matches trivially.

# In[18]:


del L['ltable_Phone']
del L['rtable_Phone']


# ## Splitting the Labelled Set##
# 
# Splitting the labelled set into training and test set, by putting half the tuple pairs in each.<br>
# The development set is called I<br>
# The evaluation set is called J

# In[19]:


IJ = em.split_train_test(L, train_proportion=0.5, random_state=0)
I = IJ['train']
J = IJ['test']
I.to_csv('I.csv',encoding = 'cp1252')
J.to_csv('J.csv',encoding = 'cp1252')


# ## Creating ML-matchers##
# 
# Initiating 6 different classifiers (Decision Tree, Random Forest, SVM, Naive Bayes, Logistic Regression, Linear Regression) and then, cross validating them on I set.

# In[20]:


dt = em.DTMatcher(name='DecisionTree', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
nb = em.NBMatcher(name ='NaiveBayes')
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')


# ## Selecting Best Matcher ##
# 
# First, we obtain all the features we could use for matching. Ft is our feature table

# In[21]:


Ft = em.get_features_for_matching(A, B, validate_inferred_attr_types=False)


# Use the system to generate feature vectors from set I. This is called set H

# In[22]:


H = em.extract_feature_vecs(I, 
                            feature_table=Ft, 
                            attrs_after='label',
                            show_progress=False)


# Perform matches and display results below (after performing cross-validation)

# In[23]:


H = em.impute_table(H, 
                exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'],
                strategy='mean')


# In[24]:


result = em.select_matcher([dt, rf, svm, ln, lg,nb], table=H, 
        exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'],
        k=5,
        target_attr='label', metric_to_select_matcher='f1', random_state=0)
result['cv_stats']


# Picking Random Forest as it has the highest average F1 score. We are not adding any rule based matchers as the precision,recall and F1 scores are already above the required thresholds.

# ## Evaluating Best Matcher##
# 
# As we picked Random Forest as the best matcher, now we apply it on the evaluation set (set J; defined earlier) to find how well it performs.
# 
# Create a new Random Forest matcher and train it on set H (feature table obtained from set I):

# In[25]:


rf = em.RFMatcher(name='RF', random_state=0)


# In[26]:


rf.fit(table=H, 
       exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
       target_attr='label')


# Extracting features from set J:

# In[27]:


Test_Ft = em.extract_feature_vecs(J, feature_table=Ft,
                            attrs_after='label', show_progress=False)


# In[28]:


Test_Ft = Test_Ft.dropna(axis =0,how ='any')
Test_Ft.to_csv("Test_Ft.csv",index=False)


# In[29]:


Test_Ft = em.read_csv_metadata("Test_Ft.csv", key='_id', encoding = 'cp1252',                         ltable=A, rtable=B,fk_ltable='ltable_Id', fk_rtable='rtable_Id')


# Computing predictions on set J:

# In[30]:


predictions = rf.predict(table=Test_Ft, exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
              append=True, target_attr='predicted', inplace=False, return_probs=True,
                        probs_attr='proba')


# In[31]:


predictions[['_id', 'ltable_Id', 'rtable_Id', 'predicted', 'proba']].head()


# In[32]:


eval_result = em.eval_matches(predictions, 'label', 'predicted')
em.print_eval_summary(eval_result)


# ## Evaluating Other Matchers ##
# 
# Now, we evaluate the performance of other matchers on set J:

# In[33]:


dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name ='NaiveBayes')


# In[34]:


dt.fit(table=H, 
       exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
       target_attr='label')
svm.fit(table=H, 
       exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
       target_attr='label')
lg.fit(table=H, 
       exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
       target_attr='label')
ln.fit(table=H, 
       exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
       target_attr='label')
nb.fit(table=H, 
       exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
       target_attr='label')


# In[35]:


predictions2 = dt.predict(table=Test_Ft, exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
              append=True, target_attr='predicted', inplace=False, return_probs=True,
                        probs_attr='proba')
predictions3 = svm.predict(table=Test_Ft, exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
              append=True, target_attr='predicted', inplace=False)
predictions4 = lg.predict(table=Test_Ft, exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
              append=True, target_attr='predicted', inplace=False, return_probs=True,
                        probs_attr='proba')
predictions5 = ln.predict(table=Test_Ft, exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
              append=True, target_attr='predicted', inplace=False)
predictions6 = nb.predict(table=Test_Ft, exclude_attrs=['_id', 'ltable_Id', 'rtable_Id', 'label'], 
              append=True, target_attr='predicted', inplace=False, return_probs=True,
                        probs_attr='proba')


# Decision Tree

# In[36]:


eval_result2 = em.eval_matches(predictions2, 'label', 'predicted')
em.print_eval_summary(eval_result2)


# SVM

# In[37]:


eval_result3 = em.eval_matches(predictions3, 'label', 'predicted')
em.print_eval_summary(eval_result3)


# Logistic Regression

# In[38]:


eval_result4 = em.eval_matches(predictions4, 'label', 'predicted')
em.print_eval_summary(eval_result4)


# Linear Regression

# In[39]:


eval_result5 = em.eval_matches(predictions5, 'label', 'predicted')
em.print_eval_summary(eval_result5)


# Naive Bayes

# In[40]:


eval_result6 = em.eval_matches(predictions6, 'label', 'predicted')
em.print_eval_summary(eval_result6)

