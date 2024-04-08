#!/usr/bin/env python
# coding: utf-8

# # keywords Research Toll
# # Name Is: "Tera Ye Do Keywords Muje De De Kaliya"

# In[5]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# # All Extra Import Here

# In[6]:


#after all import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[7]:


driver.get("https://chrome.google.com/webstore/detail/amz-suggestion-expander/cpeaihkccbeemkfefcapijechkbfjlhb?hl=en")


# # Amazon Part Start

# In[8]:


driver.get("https://www.amazon.com")


# # Amazon Search

# In[53]:


def giveMeThisTopicAllRelatedDatas(completeDataset):
    
    # 1st side loop
    try:
        ARD1st = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "s-suggestion-container")))
    except:
        ARD1st = None
        print("ARD1st up timeout.")
    
    if ARD1st:
        for i in range(len(ARD1st)):
            # call this here for memory changing error
            try:
                ARD1st = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "s-suggestion-container")))
                thistextis = ARD1st[i].text
                if thistextis == "?":
                    thistextis = thistextis.split()[:-1]
                    thistextis = " ".join(thistextis)
                elif thistextis.endswith("\n?"):
                    thistextis = thistextis.replace("\n?", "")
                if thistextis not in completeDataset:
                    completeDataset.append(thistextis)
            except:
                print("ARD1st bottom timeout.")
            
        
    
    # 2nd side loop
    try:
        ARD2nd = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ase-suggestion")))
    except:
        ARD2nd = None
        print("ARD2nd up timeout.")
    
    if ARD2nd:
        for i in range(len(ARD2nd)):
            # call this here for memory changing error
            try:
                ARD2nd = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ase-suggestion")))
                thistextis = ARD2nd[i].text
                if thistextis == "?":
                    thistextis = thistextis.split()[:-1]
                    thistextis = " ".join(thistextis)
                elif thistextis.endswith("\n?"):
                    thistextis = thistextis.replace("\n?", "")
                if thistextis not in completeDataset:
                    completeDataset.append(thistextis)
            except:
                print("ARD1st bottom timeout.")
    
    return completeDataset
    

# ^^^^^^^^ function 2nd *********    


# suggestion data making 
def giveMecompleteData(search_query, dataset_size):
    
    # main dataset
    completeDataset = []
    
    # adding first main data
    completeDataset.append(search_query)
    
    print()
    # loop for gain datas
    for i in range(dataset_size):
        
        # searching and suggestion genareting
        search_imput_section_for_amazon = driver.find_element(By.XPATH, "//*[@id='twotabsearchtextbox']")
        search_imput_section_for_amazon.clear()
        search_imput_section_for_amazon.send_keys(completeDataset[i]);
        time.sleep(10)
        
        
        # going for looking suggestion
        completeDataset = giveMeThisTopicAllRelatedDatas(completeDataset)
        if len(completeDataset) >= dataset_size:
            break
            
    print("len of the list", len(completeDataset))
    print(completeDataset)
    return completeDataset


# # Total Products Available

# In[54]:


# total Products Available
def totalProductsAvailable(querys):
    AllKeywordsResultsAmounts = [-1] * len(querys)
    
    print()
    for i in range(len(querys)):
        base_url = f"https://www.amazon.com/s?k={querys[i].replace(' ', '+')}"
        try:
            driver.get(base_url)
        except:
            print("link search get timeout.")
            time.sleep(1)
            
        try:
            amountOfResult = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//*[@id='search']/span[2]/div/h1/div/div[1]/div/div/span[1]")))
            amountOfResult = amountOfResult.text.split()
            int_values = [int(item.replace(",", "")) for item in amountOfResult if item.replace(",", "").isdigit()]
            amountOfResult = int_values[0]
            AllKeywordsResultsAmounts[i] = amountOfResult
        except:
            print("after link search get product ammount timeout.")
        
        print("amount geting done", i+1)
    
    print(AllKeywordsResultsAmounts)
    return AllKeywordsResultsAmounts


# # All Amazon Keyword Based Page link

# In[55]:


def aakbpf(keywords):
    linksOfQuerys = []
    
    for query in keywords:
        base_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
        linksOfQuerys.append(base_url)
    
    return linksOfQuerys


# # Google Search Trand

# In[56]:


def GSTF(keywords):
    links = []
    
    for i in keywords:
        link = f"https://trends.google.com/trends/explore?date=today%205-y&gprop=froogle&q={i.replace(' ', '%20')}&hl=en-US"
        links.append(link)
        
    return links


# # Google Search Volmes

# In[57]:


def GSVsf(keywords):
    base_url = "https://ads.google.com/aw/keywordplanner/ideas/new"
    links = []

    for keyword in keywords:
        encoded_keyword = keyword.replace(" ", "%20")
        link = f"{base_url}?ocid=1412291644&authuser=1&ecl&uscid=1412291644&__c=2915025756&euid=968679260&__u=5702991740&cmpnInfo=%7B%228%22%3A%22f87f1ee2-6994-4417-94eb-09aeb482a391%22%7D&workflowSessionId=a4CAD356A-649A-46BE-881D-642E7E2042B9--1&currentStep=expert&q={encoded_keyword}"
        links.append(link)

    return links


# # MAIN

# In[60]:


# MAIN Start
search_query = input("\nEnter your search query \n(if you went to search lots of topics in same time, then use this formate -> cat, cat food, cat house): \n\n").split(', ')
dataset_size = input("\nEnter your data amount \n(give data ammount for all search query, \nBUT if your data ammount is same for search query then just give single ammount): \n\n").split(', ')
file_name = input("\nEnter your file name \n(give file name for all search query): \n\n").split(', ')

# code for dataset size array
if search_query == dataset_size:
    dataset_size = [int(num) for num in dataset_size]
else:
    dataset_size = [int(dataset_size[0])] * len(search_query)

totalFiles = len(search_query)

result = [i * 10 for i in dataset_size]

# time calculation
print()
print("maybe this much time need: ", (sum(dataset_size)*0.054)) # per key need "0.054 MIN".
print()

for i in range(totalFiles):
    keywords = giveMecompleteData(search_query[i], dataset_size[i]) # keywords
    KBTPA = totalProductsAvailable(keywords); # key word based total product available
    AAKBP = aakbpf(keywords) # all amazon keyword based page link
    GSVs = GSVsf(keywords) # google search volumes
    GST = GSTF(keywords) # google search trand
    
    # 2nd part for saving file*********************
    # dataframe making
    data1 = {'keywords': keywords}
    data2 = {'Search Results Sizes': KBTPA}
    data3 = {'Amazon Pages': AAKBP}
    data4 = {'Google Search Volumes': GSVs}
    data5 = {'Google Shopping Search trand Pages': GST}
    
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)
    df4 = pd.DataFrame(data4)
    df5 = pd.DataFrame(data5)
    
    # Concatenate the two DataFrames horizontally (axis=1) to create a two-column DataFrame
    combined_df = pd.concat([df1, df2, df3, df4, df5], axis=1)
    
    
    # saving as a xlsx file
    folderPath =r"Documents\tool_files" 
    fileName = file_name[i]
    excel_file_path = f"{folderPath}\{fileName}.xlsx" 
    combined_df.to_excel(excel_file_path, index=False) #file saving
    


#done
print()
print("DONE")
print()


# In[ ]:





# In[ ]:





# In[ ]:




