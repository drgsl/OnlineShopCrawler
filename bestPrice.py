from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions

import colorama
from colorama import Fore, Back, Style

import sys
import re

import json

"""
Se va crea un crawler pentru a prelua informatii despre pretul unor produse date ca lista de input. 
Se va crea un fisier json in care se vor retine urmatoarele informatii: 
>numele produsului,
>pretul cel mai bun, 
>pretul cel mai mare, 
>numarul de oferte. 

Site-ul ce va fi utilizat ca si suport: https://www.compari.ro.

INPUT: compari.py <urls of products>
OUTPUT: Un fisier json in care se afla informatiile despre preturile produselor.
"""

def getDriver():
    try:
        driver = webdriver.Chrome()
        print(Back.BLUE + "Firefox Driver created")
    except exceptions.SessionNotCreatedException:
        driver = webdriver.Firefox(), print(Back.BLUE + "Chrome Driver created")
    
    driver.minimize_window()
    return driver    

def printProductInfo(url):
    colorama.init(autoreset=True)

    productDict = dict()

    """
    Driver Setup
    """
    driver = getDriver()

    try:
        driver.get(url)
    except Exception as e:
        print(Back.RED + f"Could not access url -> {e} ")
        print(Back.RED + f"url: {url} ")


    """
    Brand Name
    """
    productDetails = driver.find_element(By.CLASS_NAME, "product-details")
    productBrand = productDetails.find_element(By.XPATH, "//*[contains(@itemprop, 'brand')]")
    print(Back.GREEN + f"Product Brand:", end="")
    print(f" {productBrand.text}")
    
    productDict["productBrand"] = productBrand.text

    """
    Product Name
    """
    productName = productDetails.find_elements(By.XPATH, "//span[contains(@itemprop, 'name')]")[1]
    print(Back.GREEN + f"Product Name:", end="")
    print(f"{productName.text}")

    productDict["productName"] = productName.text

    """
    Lowest Price
    """
    try:
        lowestPriceText = productDetails.find_element(By.XPATH, "//*[contains(@itemprop, 'lowPrice')]")
        lowestPrice = getNumber(lowestPriceText.text)
        print(Back.GREEN + f"Lowest Price: ", end="")
        print(f"{lowestPrice}")
    except Exception as e:
        print(Back.RED + f"Lowest Price could not be found -> {e} ")
        
    productDict["lowestPrice"] = lowestPrice

    """
    Biggest Price
    """
    # try:
    #     highestPriceText = productDetails.find_elements(By.XPATH, "//*[contains(@itemprop, 'highPrice')]")
    #     for price in highestPriceText:
    #         print(price.text)
    #     highestPrice = float(highestPriceText[1].text)
    #     print(Back.GREEN + f"Highest Price: ", end="")
    #     print(f"{highestPrice}")
    # except Exception as e:
    #     print(Back.RED + f"Highest Price could not be found -> {e} ")

    """
    All prices
    """
    prices = driver.find_elements(By.CLASS_NAME, "row-price")
    print(f"{len(prices)} prices found")
    highestPrice = 0
    for price in prices:g
        if(getNumber(price.text) > highestPrice):
            highestPrice = getNumber(price.text)
        # print(price.get_attribute('innerHTML'))
        # print(price.get_attribute('class'))

    print(Back.GREEN + f"Highest Price: ", end="")
    print(f"{highestPrice}")
    
    productDict["highestPrice"] = highestPrice

    """
    Offer Count
    """
    try:
        offerCountText = driver.find_element(By.CLASS_NAME, "offer-count")
        offerCount = re.findall(r'\d+', offerCountText.text)[0]
        print(Back.GREEN + f"Found:", end="")
        print(f" {offerCount} offers ", end="")
        print(Back.GREEN + f"available")
    except Exception as e:
        print(Back.RED + f"No offer count found -> {e} ")

    productDict["offerCount"] = offerCount

    driver.close()
    return productDict


def getNumber(text):
    numbers = re.findall(r'\d+', text)
    return int("".join(numbers))

if __name__ == '__main__':

    urls = []

    with open("urls.txt") as file:
        for line in file:
            urls.append(line)

    for url in urls:
        urlDict = printProductInfo(url)
        urlJson = json.dumps(urlDict)
        open(f'{urlDict["productBrand"]}_{urlDict["productName"]}.json', 'w').write(urlJson)

        
    # productNames = productDetails.find_element(By.XPATH, "//*[contains(@itemprop, 'name')]")
    # for name in productNames:
    #     print(name.text)

    # productPageTop = driver.find_elements(By.CLASS_NAME, "product-page-top")
    # print(len(productPageTop))
    # productName = productPageTop[0].find_elements(By.CLASS_NAME, "visible-xs")
    # print(len(productName))
    # print(productName[1].text)

    # for name in productName:
    #     print(name.text)


