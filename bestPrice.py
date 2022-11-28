from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions

url = "https://banda-led.compari.ro/epistar/banda-digitala-ws2812b-60-led-dream-magic-p689796393/"

def getDriver():
    try:
        driver = webdriver.Firefox()
    except exceptions.SessionNotCreatedException:
        driver = webdriver.Chrome()
    
    driver.minimize_window()
    return driver    

if __name__ == '__main__':

    driver = getDriver()
    
    try:
        driver.get(url)
    except exceptions.WebDriverException:
        print("bad url")

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

    prices = driver.find_elements(By.CLASS_NAME, "row-price")
    print(f"{len(prices)} prices found")
    for price in prices:
        print(price.text)

    driver.close()
