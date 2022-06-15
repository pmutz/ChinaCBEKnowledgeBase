import logging
# -- Uncomment for Azure -- 
import azure.functions as func
import json
import csv
import datetime
from random import randint
from time import sleep
import uuid, json, requests

from bs4 import BeautifulSoup

from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# abosulte path to copied binary
driver = webdriver.Chrome('/home/site/wwwroot/MTCBEFunction/chromedriver',chrome_options=chrome_options)
# -- Uncomment for local -- driver = webdriver.Chrome('C:\\Users\\Localpath\\ChinaCBEKnowledgeBase\\azfunc-mtcbefunctions\\MTCBEFunction\\chromedriver.exe',options=chrome_options)

# from defaultVariables import *
# *********************************************

# Global Variables

# Base URL for Google Queries
googleQueryBaseURL = "https://www.google.ch/search?q="

# XPath query to identify Google highligted search result (answer box)
googleHighlightedResultXPath = "//block-component//b"

# Translation source language
languageFrom = "zH-hans"

# Translation target language (exactly two, formatted as list element)
languagesTo = ['en', 'de']

# Azure Translator authentication
subscription_key = "AZURETRANSLATORSUBSCRIPTIONKEY"
# -- Use for local -- endpoint = "https://api.cognitive.microsofttranslator.com"
endpoint = "https://api.cognitive.microsofttranslator.com"

# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "switzerlandnorth"

# API path
path = '/translate?api-version=3.0'
constructed_url = endpoint + path

# CBE Platform Variables List
platformVariablesList = []

header = []
header.append('PlatformFriendlyName')
header.append('Parseable')
header.append('URL')
header.append('CategoryIdentificationMethod')
header.append('MultipleElementsReturned')
header.append('CategoryIdentificationQuery')
header.append('RemovalOfUnwantedCharacterRequired')
header.append('UnwantedCharacterToBeRemoved')
header.append('AdditionalParsingRequired')
header.append('AdditionalParsingElement')
header.append('AdditionalParsingAttributeFilterRequired')
header.append('AdditionalParsingAttributeFilterName')
header.append('AdditionalParsingAttributeFilterValue')
header.append('FullGoogleSearchURL')
platformVariablesList.append(header)

# Tmall
datarow = []
# Platform Friendly Name
datarow.append("Tmall")
# Platform pareseable or not
datarow.append(True)
# Platform Home URL
datarow.append("https://www.tmall.com")
# Applied Category Identification Method (parsing instruction)
datarow.append("xpath")
# Will mulimple elements be returned by the method defined above or not
datarow.append(False)
# Query which is passed to the parsing instruction defined above
datarow.append("/html/body/div[1]/div[3]/div[2]")
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(False)
# Unwanted character to be removed from the returned string after the parsing
datarow.append(None)
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(True)
# After which HTML element the program has to look
datarow.append("span")
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(True)
# If the above value is set to true, which attribute is it
datarow.append("class")
# Define the value of the attribute defined above
datarow.append("rax-text-v2 Category--categoryText--1dv1tJM")
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"tmall+monthly+active+users&as_qdr=y1")
platformVariablesList.append(datarow)

# Taobao
datarow = []
# Platform Friendly Name
datarow.append("Taobao")
# Platform pareseable or not
datarow.append(True)
# Platform Home URL
datarow.append("https://world.taobao.com")
# Applied Category Identification Method (parsing instruction)
datarow.append("classname")
# Will mulimple elements be returned by the method defined above or not
datarow.append(True)
# Query which is passed to the parsing instruction defined above
datarow.append("category-link")
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(True)
# Unwanted character to be removed from the returned string after the parsing
datarow.append("/")
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(False)
# After which HTML element the program has to look
datarow.append(None)
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(False)
# If the above value is set to true, which attribute is it
datarow.append(None)
# Define the value of the attribute defined above
datarow.append(None)
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"taobao+monthly+active+users&as_qdr=y1")
platformVariablesList.append(datarow)

# Kaola
datarow = []
# Platform Friendly Name
datarow.append("Kaola")
# Platform pareseable or not
datarow.append(True)
# Platform Home URL
datarow.append("https://kaola.com")
# Applied Category Identification Method (parsing instruction)
datarow.append("classname")
# Will mulimple elements be returned by the method defined above or not
datarow.append(True)
# Query which is passed to the parsing instruction defined above
datarow.append("t")
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(False)
# Unwanted character to be removed from the returned string after the parsing
datarow.append(None)
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(False)
# After which HTML element the program has to look
datarow.append(None)
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(False)
# If the above value is set to true, which attribute is it
datarow.append(None)
# Define the value of the attribute defined above
datarow.append(None)
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"kaola+number+of+users&as_qdr=y1")
platformVariablesList.append(datarow)

# JD.com
datarow = []
# Platform Friendly Name
datarow.append("JD.com")
# Platform pareseable or not
datarow.append(True)
# Platform Home URL
datarow.append("https://global.jd.com")
# Applied Category Identification Method (parsing instruction)
datarow.append("classname")
# Will mulimple elements be returned by the method defined above or not
datarow.append(True)
# Query which is passed to the parsing instruction defined above
datarow.append("cate-menu-link")
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(False)
# Unwanted character to be removed from the returned string after the parsing
datarow.append(None)
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(False)
# After which HTML element the program has to look
datarow.append(None)
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(False)
# If the above value is set to true, which attribute is it
datarow.append(None)
# Define the value of the attribute defined above
datarow.append(None)
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"jd.com+monthly+active+users&as_qdr=y1")
platformVariablesList.append(datarow)

# VIP.com
datarow = []
# Platform Friendly Name
datarow.append("VIP.com")
# Platform pareseable or not
datarow.append(True)
# Platform Home URL
datarow.append("https://www.vip.com")
# Applied Category Identification Method (parsing instruction)
datarow.append("classname")
# Will mulimple elements be returned by the method defined above or not
datarow.append(True)
# Query which is passed to the parsing instruction defined above
datarow.append("menu-item-tit")
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(False)
# Unwanted character to be removed from the returned string after the parsing
datarow.append(None)
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(False)
# After which HTML element the program has to look
datarow.append(None)
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(False)
# If the above value is set to true, which attribute is it
datarow.append(None)
# Define the value of the attribute defined above
datarow.append(None)
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"vip.com+number+of+active+users+e-commerce&as_qdr=y1")
platformVariablesList.append(datarow)

# Little Red Book (RED)
datarow = []
# Platform Friendly Name
datarow.append("Little Red Book (RED)")
# Platform pareseable or not
datarow.append(False)
# Platform Home URL
datarow.append(None)
# Applied Category Identification Method (parsing instruction)
datarow.append(None)
# Will mulimple elements be returned by the method defined above or not
datarow.append(None)
# Query which is passed to the parsing instruction defined above
datarow.append(None)
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(False)
# Unwanted character to be removed from the returned string after the parsing
datarow.append(None)
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(False)
# After which HTML element the program has to look
datarow.append(None)
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(False)
# If the above value is set to true, which attribute is it
datarow.append(None)
# Define the value of the attribute defined above
datarow.append(None)
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"little+red+book+monthly+active+users&as_qdr=y1")
platformVariablesList.append(datarow)

# WeChat Mini Porgrams
datarow = []
# Platform Friendly Name
datarow.append("WeChat Mini Programs")
# Platform pareseable or not
datarow.append(False)
# Platform Home URL
datarow.append(None)
# Applied Category Identification Method (parsing instruction)
datarow.append(None)
# Will mulimple elements be returned by the method defined above or not
datarow.append(None)
# Query which is passed to the parsing instruction defined above
datarow.append(None)
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(False)
# Unwanted character to be removed from the returned string after the parsing
datarow.append(None)
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(False)
# After which HTML element the program has to look
datarow.append(None)
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(False)
# If the above value is set to true, which attribute is it
datarow.append(None)
# Define the value of the attribute defined above
datarow.append(None)
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"wechat+mini+program+monthly+active+users&as_qdr=y1")
platformVariablesList.append(datarow)

# Pinduoduo
datarow = []
# Platform Friendly Name
datarow.append("Pinduoduo")
# Platform pareseable or not
datarow.append(False)
# Platform Home URL
datarow.append(None)
# Applied Category Identification Method (parsing instruction)
datarow.append(None)
# Will mulimple elements be returned by the method defined above or not
datarow.append(None)
# Query which is passed to the parsing instruction defined above
datarow.append(None)
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(False)
# Unwanted character to be removed from the returned string after the parsing
datarow.append(None)
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(False)
# After which HTML element the program has to look
datarow.append(None)
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(False)
# If the above value is set to true, which attribute is it
datarow.append(None)
# Define the value of the attribute defined above
datarow.append(None)
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"pinduoduo+monthly+active+users&as_qdr=y1")
platformVariablesList.append(datarow)

# Suning
datarow = []
# Platform Friendly Name
datarow.append("Suning")
# Platform pareseable or not
datarow.append(True)
# Platform Home URL
datarow.append("https://www.suning.com")
# Applied Category Identification Method (parsing instruction)
datarow.append("classname")
# Will mulimple elements be returned by the method defined above or not
datarow.append(False)
# Query which is passed to the parsing instruction defined above
datarow.append("index-list")
# Are there characters which must be removed in the returned string after the parsing or not
datarow.append(False)
# Unwanted character to be removed from the returned string after the parsing
datarow.append(None)
# Is there further processing of the result needed (in case the returned value after parsing still is HTML) or not
datarow.append(True)
# After which HTML element the program has to look
datarow.append("a")
# In case more than one of the elements defined above are returned, is there an attribute to further narrow down the result or not
datarow.append(False)
# If the above value is set to true, which attribute is it
datarow.append(None)
# Define the value of the attribute defined above
datarow.append(None)
# Define the query to search at google for the active users of the platform. Please not to only type queries which result in Google displaying a highlighted answer box as first result
datarow.append(googleQueryBaseURL+"suning+number+of+active+users")
platformVariablesList.append(datarow)

# from parseCBEWebsite import parseCBEWebsite
# *********************************************

def parseCBEWebsite(URL, categoryIdentificationMethod, multipleElementsReturned, categoryIdentificationQuery, removalOfUnwantedCharacterRequired, unwantedCharacterToBeRemoved, additionalParsingRequired, additionalParsingElement, additionalParsingAttributeFilterRequired, additionalParsingAttributeFilterName, additionalParsingAttributeFilterValue):
    
    driver.get(URL)

    if categoryIdentificationMethod == "classname" and multipleElementsReturned == False:
        element = driver.find_element_by_class_name(categoryIdentificationQuery)
    elif categoryIdentificationMethod == "classname" and multipleElementsReturned == True:
        elements = driver.find_elements_by_class_name(categoryIdentificationQuery)
    elif categoryIdentificationMethod == "xpath" and multipleElementsReturned == False:
        element = driver.find_element_by_xpath(categoryIdentificationQuery)

    if additionalParsingRequired == True:
        content = element.get_attribute('innerHTML')

        soup = BeautifulSoup(content, "html.parser")

        if additionalParsingAttributeFilterRequired == True:
            result = soup.find_all(additionalParsingElement,{additionalParsingAttributeFilterName:additionalParsingAttributeFilterValue})
        elif additionalParsingAttributeFilterRequired == False:
            result = soup.find_all(additionalParsingElement)

        value = ';'.join((r.text) for r in result)
    else:
        value = ';'.join((element.text) for element in elements)

    if removalOfUnwantedCharacterRequired == True:
        value = value.translate({ord(unwantedCharacterToBeRemoved): None})

    return value
    
# from parseGoogleHighlightedResult import getGoogleHighlightedResult
# *********************************************

def getGoogleHighlightedResult(GoogleSearchURL, xPath):

    driver.get(GoogleSearchURL)

    try:
        element = driver.find_element_by_xpath(xPath)
        parentelement = element.find_element_by_xpath('./..')
        content = parentelement.get_attribute('innerHTML')
        highlightedText = content.split('<b>')[1].split('</b>')[0]
        content = content.replace('<b>', '')
        content = content.replace('</b>', '')
        content = content + ' [' + highlightedText + ']'
    except:
        content = 'No highlighted answer box returned for Google query [No value]'
    
    return content

# from translateOnAzure import translateOnAzure
# *********************************************

def translateOnAzure(expressionToTranslate):

    params = {
        'api-version': '3.0',
        'from': languageFrom,
        'to': languagesTo
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': expressionToTranslate
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    return json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))

# from constructCategoryList import constructCategoryList
# *********************************************

def constructCategoryList(FirstRun, InputList, PlatformName, ZHString, ENString, DEString):
    if FirstRun == True:
        translationsList = []

        header = []
        header.append('strFKPlatform')
        header.append('strProductCategoryNameZH')
        header.append('strProductCategoryNameEN')
        header.append('strProductCategoryNameDE')
        header.append('bolFetchedAutomatically')
        translationsList.append(header)
    else:
        translationsList = InputList

    ENList = list(ENString.split(';'))
    DEList = list(DEString.split(';'))
    
    counter = 0

    for word in ZHString.split(';'):
        datarow = []
        datarow.append(PlatformName)
        datarow.append(word.lstrip())
        datarow.append(ENList[counter])
        datarow.append(DEList[counter])
        datarow.append(True)
        translationsList.append(datarow)
        counter = counter + 1
    
    return translationsList

# from constructMAUList import constructMAUList
# *********************************************

def constructMAUList(FirstRun, InputList, PlatformName, GoogleSearchURL, QueryResult):
    if FirstRun == True:
        GoogleResultsList = []

        header = []
        header.append('strFKPlatform')
        header.append('strGoogleSearchURL')
        header.append('strQueryResult')
        header.append('strHighlightedResult')
        header.append('bolFetchedAutomatically')
        GoogleResultsList.append(header)
    else:
        GoogleResultsList = InputList

    HighlightedQueryResult = QueryResult.split('[')[1].split(']')[0]
    QueryResult = QueryResult[:QueryResult.find('[')] + QueryResult[QueryResult.rfind(']') + 1:].strip()

    datarow = []
    datarow.append(PlatformName)
    datarow.append(GoogleSearchURL)
    datarow.append(QueryResult)
    datarow.append(HighlightedQueryResult)
    datarow.append(True)
    GoogleResultsList.append(datarow)

    return GoogleResultsList


def convertListToCSVString(inputList):
    
    outputCSVString = ""

    for row in inputList:
        counter = 0
        
        for value in row:
            if value == True or value == False:
                outputCSVString += ';' + str(value)
            elif value == None:
                outputCSVString += ';Not set'
            else:
                if counter == 0:
                    outputCSVString += value
                else:
                    outputCSVString += ';' + value
            counter = counter + 1
        
        outputCSVString += "\n"
    
    return outputCSVString


def MTCBEMainFunction(platformVariablesList):
    counter = 0

    for platform in platformVariablesList[1:]:
        
        # Parse all parseable platfoms based on the platformVariablesList list object

        if platform[1] == True:
        
            # Call the parsing function to gather the categories navigation content
            parsingResult = parseCBEWebsite(platform[2], platform[3], platform[4], platform[5], platform[6], platform[7], platform[8], platform[9], platform[10], platform[11], platform[12])

            # Send the result, separated with semicolons, to the Microsoft translator service
            translationResult = translateOnAzure(parsingResult)
            json_result = json.loads(translationResult)

            # Store results of translation into variables, one per translated language
            translatedTextEN = json_result[0]['translations'][0]['text']
            translatedTextDE = json_result[0]['translations'][1]['text']

            if counter == 0:
                firstRun = True
                
                #Initialize list for storing the translations
                translatedCategoriesList = []
                # Initialize list for storing the parsed MAU data
                googleResultsList = []

            else:
                firstRun = False

            # Append to the list object, which will in the end be used to store the values in the target system (special: initial call to include the header row)
            translatedCategoriesList = constructCategoryList(firstRun, translatedCategoriesList, platform[0], parsingResult, translatedTextEN, translatedTextDE)
        
        else:
            if counter == 0:
                firstRun = True
                
                #Initialize list for storing the translations
                translatedCategoriesList = []
                # Initialize list for storing the parsed MAU data
                googleResultsList = []

            else:
             firstRun = False
        
        # Get monthly active users numbers for platfom based on the platformVariablesList list object from Google

        # Get highlighted result from Google regarding MAU of the respective platform
        googleHighlightedResult = getGoogleHighlightedResult(platform[13], googleHighlightedResultXPath)

        # Append to the list object, which will in the end be used to store the values in the target system (special: initial call to include the header row)
        googleResultsList = constructMAUList(firstRun, googleResultsList, platform[0], platform[13], googleHighlightedResult)

        # Random sleep between 3 and 10 seconds to avoid blockage by Google, Provider or Platform services
        sleep(randint(3,10))

        counter = counter + 1

    return translatedCategoriesList, googleResultsList


def main(req: func.HttpRequest, categoriestoblob: func.Out[str],  mautoblob: func.Out[str]) -> func.HttpResponse:
    
    logging.info('*************************************************************************\n')
    logging.info('********Python HTTP trigger function started processing a request********\n')
    logging.info('*************************************************************************\n')

    logging.info('\n\n*************************************************************************\n')
    logging.info('*****************************Translator test*****************************\n')
    logging.info('*************************************************************************\n')
    translationtest = translateOnAzure("翻译API响应并返回一个德语和一个英语的结果!")
    logging.info(translationtest)
    logging.info('\n\n*************************************************************************\n')
    logging.info('*********************Translator test end, continuing*********************\n')
    logging.info('*************************************************************************\n')

    platformVariablesListOverwrite = req.params.get('platformVariablesListOverwrite')
    if not platformVariablesListOverwrite:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            platformVariablesListOverwrite = req_body.get('platformVariablesListOverwrite')

    if platformVariablesListOverwrite:
        global platformVariablesList
        platformVariablesList = platformVariablesListOverwrite

    translatedCategoriesList, googleResultsList = MTCBEMainFunction(platformVariablesList)
    
    logging.info('*************************************************************************\n')
    logging.info('**********************Converting results for export**********************\n')
    logging.info('*************************************************************************\n')

      
    categoriestoblob.set(convertListToCSVString(translatedCategoriesList).encode())
    mautoblob.set(convertListToCSVString(googleResultsList))

    logging.info('\n\n*************************************************************************\n')
    logging.info('***********************************DOne**********************************\n')
    logging.info('*************************************************************************\n')
    
    return func.HttpResponse(f"Function ran successfully", status_code=200)
