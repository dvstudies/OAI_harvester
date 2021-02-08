#!/usr/bin/env python
# coding: utf-8

# # OAI harvester
# Based upon recommendations from https://github.com/hertzphoto/RomaFototeca/blob/master/documentation/oai-pmh.md
# 
# *This harvester makes use of Sickle: OAI-PMH for Humans Copyright (c) 2013 by Mathias Loesch.*
# 
# [@author](https://github.com/VBernasconi) V. Bernasconi
# 
# @date 02.2021
# 
# Please run __pip install -r requirements.txt__

# In[2]:


import requests
import pickle
import os
import sys
import time
import sqlite3
import jmespath
import pandas as pd
import xmltodict, json
from sickle import Sickle
import xml.etree.ElementTree as ET


# In[10]:


oai_url = "https://oai.biblhertz.it/foto/oai-pmh"

oai_getRecord = {'verb': 'GetRecord', 'identifier': '', 'metadataPrefix':'raw'}
oai_listIDs = {'verb': 'ListIdentifiers', 'set': '', 'metadataPrefix':'raw'}
oai_listRecords = {'verb': 'ListRecords', 'set': 'obj', 'metadataPrefix':'raw'}
oai_resumptionToken = {'resumptionToken':''}

img_url = "http://fotothek.biblhertz.it/bh/2048px/"

db_name = 'biblhertz.db'


# In[4]:


#DICTIONARY
IMAGE_INFO = 'a8450'
DIGITAL_IMAGE = 'a8540'
ARTIST_INFO = 'aob30'
ARTIST_NAME = 'a31nn'
ARTIST_GND = 'a30gn'
DATE_INFO = 'a5060'
DATE = 'a5064'
LOCATION_INFO = 'aob26'
LOCATION_NAME = 'a2664'
MUSEUM = 'aob28'
MUSEUM_NAME = 'a2900'
MUSEUM_LOCATION = 'a2864'
TITLE = 'a5200'
TYPE = 'a5230'
MEDIUM = 'a5260'
DIMENSIONS = 'a5360'


# In[5]:


"""
getDate

Split a string in "from" "to" values

@param string date: a date in a string format ("1560", "1560/1561", "1560-1570")
@return date_from and date_to
"""
def getDate(date):
    if '-' in date:
        return date.split('-', 1)
    elif '/' in date:
        return date.split('/', 1)
    else:
        return date, date


# In[6]:


"""
getImages

Create a folder and store the images downloaded from their identifiers provided 
in the list of image identifiers given as a parameter

@param listIDs a list of digital image IDs
@return a list of image IDs for which it was not possible to download images
"""
def getImages(listIDs):
    errorIDs = []
    #create a folder to store the images
    os.makedirs("biblhertz_images", exist_ok=True)
    for id_ in listIDs:
        response = requests.get(img_url+id_+".jpg")
        if response: #if the image request is positive, download the image in the local folder "images_bb"
            name = "biblhertz_images/biblhertz_"+str(id_)+".jpg"
            file = open(name, "wb")
            file.write(response.content)
            file.close()
        else:
            errorIDs.append(id_)
    return errorIDs


# In[7]:


"""
getIdentifiers

Make a GET request to the oai_url with the given resumptionToken. Extract from the response a list of Ids
and the next resumptionToken to request the next GET page

@param string reumptionToken: get a resumptionToken as an input, default 'None'
@param string set_ : the set, can be obj, kue, kon, objkue, default 'obj'
@return the list of objects'ids and new resumptionToken
"""

def getIdentifiers(resumptionToken = 'None', set_ = 'obj'):
    
    print("Collecting identifiers from the fototeca database -- this might take several minutes.")
    
    objects_list_ = []
    resumptionToken_ = resumptionToken
    
    while resumptionToken_ != '':
        
        oai_listIDs['set'] = set_
        if resumptionToken_ != 'None' :
            oai_listIDs['resumptionToken'] = resumptionToken_

        r = requests.get(url = oai_url, params = oai_listIDs)
        json_content = xmltodict.parse(r.text)
        
        resumptionToken_ = ''

        for (key, value) in json_content['OAI-PMH']['ListIdentifiers'].items():
            if key == "header":
                for object_ in value:
                    if "oai::obj::08" in object_['identifier']: #check for biblhertz id
                        objects_list_.append(object_['identifier'])
            if key == "resumptionToken":
                resumptionToken_ = value["#text"]
            object_[DATE_INFO][DATE]
    return objects_list_, resumptionToken_


# In[8]:


objectsSet = []
iteration = 0

sickle = Sickle(oai_url)
records = sickle.ListRecords(metadataPrefix='raw', set='obj', ignore_deleted=True)

conn = sqlite3.connect(db_name, isolation_level=None)
cur = conn.cursor()
    
#Quickly create a database with the different fields needed
columns_ = ['object_ID', 'title', 'artist_GND', 'artist_name','date_begin','date_end','current_location', 'type', 'medium', 'dimensions','img_digital']
df = pd.DataFrame(columns=columns_)
df.to_sql('Objects', conn, index = False, if_exists ='replace')

print(f"Connection to {oai_url} successful, retrieving objects data")
print(f"Creation/connection to {db_name} successful")
print(f"WARNING - Full retrieval of images takes time")

insert_cmd = 'INSERT INTO Objects VALUES (?,?,?,?,?,?,?,?,?,?,?)'

start_time = time.time()

for record in records:
    object_ID = record.metadata['a5000'][0]
    if object_ID.startswith('08'):
        iteration +=1
        
        #set the variables for the different object's fields
        artist_GND = 'unknown'
        artist_name = 'unknown'
        date_begin = 'unknown'
        date_end = 'unknown'
        current_location = 'unknown'
        title = 'unknown'
        type_ = 'unknown'
        medium = 'unknown'
        dimensions = 'unknown'
        img_digital = []

        if LOCATION_NAME in record.metadata:
            current_location = record.metadata[LOCATION_NAME][0]
        if ARTIST_NAME in record.metadata:
            artist_name = record.metadata[ARTIST_NAME][0]
        if ARTIST_GND in record.metadata:
            artist_GND = record.metadata[ARTIST_GND][0]
        if TITLE in record.metadata:
            title = record.metadata[TITLE][0]
        if TYPE in record.metadata:
            type_ = record.metadata[TYPE][0]
        if MEDIUM in record.metadata:
            medium = record.metadata[MEDIUM][0]
        if DIMENSIONS in record.metadata:
            dimensions = record.metadata[DIMENSIONS][0]
        if DIGITAL_IMAGE in record.metadata:
            for img_ in record.metadata[DIGITAL_IMAGE]:
                img_digital.append(img_)
        if DATE in record.metadata:
            date_begin, date_end = getDate(record.metadata[DATE][0])
        
        if img_digital:
            for img_ in img_digital:
                objectsSet.append((object_ID, title, artist_GND, artist_name, date_begin, date_end, 
                                       current_location, type_, medium, dimensions, img_))
        else:
            objectsSet.append((object_ID, title, artist_GND, artist_name, date_begin, date_end,
                               current_location, type_, medium, dimensions, "unavailable"))
        if iteration > 500 :
            print(f"-", end="")
            cur.executemany(insert_cmd, objectsSet)
            objectsSet = []
            iteration = 0
            conn.commit()
if objectsSet:
    cur.executemany(insert_cmd, objectsSet)
    conn.commit()
print(f"\nFinal objects added to the database")           
conn.close()
nd_time = time.time()
print("Total execution time = %.6f seconds" % (end_time-start_time))    


# In[ ]:




