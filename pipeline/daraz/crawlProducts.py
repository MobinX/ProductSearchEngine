from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')

options.add_argument("start-maximized"); 
options.add_argument("disable-infobars"); 
options.add_argument("--disable-extensions"); 
options.add_argument("--disable-gpu"); 
options.add_argument("--disable-dev-shm-usage"); 

driver = webdriver.Chrome(options=options)

print("running")
driver.get('https://www.daraz.com.bd/smartphones/')
totalProducts = driver.find_element(By.XPATH, "//div[@class=' tips--QRnmZ']//span[1]").text
totalProducts = totalProducts.replace(" items found for", "")
totalProducts = int(totalProducts)
print(totalProducts)

products = driver.find_elements(By.ID, "id-a-link")
productPagesCount = int(totalProducts / len(products)) + 1
print(productPagesCount)
driver.quit()

for i in range(1, productPagesCount):
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://www.daraz.com.bd/smartphones/?page={i}')
    products = driver.find_elements(By.ID, "id-a-link")
    for product in products:
        print(product.get_attribute("href"))
    driver.quit()
