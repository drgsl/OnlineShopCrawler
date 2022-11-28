from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions

import colorama
from colorama import Fore, Back, Style

url = "https://drujba.compari.ro/active/39-39-p46942144/"

def getDriver():
    try:
        driver = webdriver.Firefox()
        print(Back.GREEN + "Firefox Driver created")
    except exceptions.SessionNotCreatedException:
        driver = webdriver.Chrome(), print(Back.GREEN + "Chrome Driver created")
    
    driver.minimize_window()
    return driver    

def printProductInfo(driver, url):
    if driver is None:
        driver = getDriver()
    
    try:
        driver.get(url)
    except Exception as e:
         print(e)

    try:
        offerCount = driver.find_element(By.CLASS_NAME, "offer-count")
        print(offerCount.text)
    except Exception as e:
        print(Back.RED + f"No offer count found -> {e} ")
    
    printPrices(driver=driver)



def printPrices(driver = None):
    
    if driver is None:
        driver = getDriver()

    prices = driver.find_elements(By.CLASS_NAME, "row-price")
    print(f"{len(prices)} prices found")
    for price in prices:
        print(price.text)

    driver.close()




if __name__ == '__main__':
    colorama.init(autoreset=True)
    driver = getDriver()

    printProductInfo(driver, url)


    productDetails = driver.find_element(By.CLASS_NAME, "product-details")

    productBrand = productDetails.find_element(By.XPATH, "//*[contains(@itemprop, 'brand')]")
    print(productBrand.text)

    try:
        offerCount = driver.find_element(By.CLASS_NAME, "offer-count")
        print(offerCount.text)
    except exceptions.NoSuchElementException:
        print("No offer count found")

        
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


