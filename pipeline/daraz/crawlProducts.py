from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

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

result = {}
# Open and parse JSON file
with open('../../store/daraz-categories.json') as file:
    data = json.load(file)
    categories = data.get('categories')
    for category in categories:
        url = f'https://www.daraz.com.bd/{category}/'
        print(f"Processing category: {category}")
        driver.get(url)
        totalProducts = driver.find_element(By.XPATH, "//div[@class=' tips--QRnmZ']//span[1]").text
        totalProducts = totalProducts.replace(" items found for", "")
        totalProducts = totalProducts.replace(",", "")
        totalProducts = int(totalProducts)
        products = driver.find_elements(By.ID, "id-a-link")
        productPagesCount = int(totalProducts / len(products)) + 1
        productLinks = []
        for i in range(1, productPagesCount):
            print(f"Processing page {i} of category {category}")
            driver.get(f'{url}?page={i}')
            products = driver.find_elements(By.ID, "id-a-link")
            for product in products:
                productLinks.append(product.get_attribute("href"))
                print(product.get_attribute("href"))
        result[category] = productLinks


# Write the result to a JSON file
with open('../../store/daraz-products.json', 'w') as file:
    json.dump(result, file)
# Process the data
# ...

# Example: Print the contents of the JSON file
# print(data)

# print("running")
# driver.get('https://www.daraz.com.bd/smartphones/')
# totalProducts = driver.find_element(By.XPATH, "//div[@class=' tips--QRnmZ']//span[1]").text
# totalProducts = totalProducts.replace(" items found for", "")
# totalProducts = int(totalProducts)
# print(totalProducts)

# products = driver.find_elements(By.ID, "id-a-link")
# productPagesCount = int(totalProducts / len(products)) + 1
# print(productPagesCount)
# driver.quit()

# for i in range(1, productPagesCount):
#     driver = webdriver.Chrome(options=options)
#     driver.get(f'https://www.daraz.com.bd/smartphones/?page={i}')
#     products = driver.find_elements(By.ID, "id-a-link")
#     for product in products:
#         print(product.get_attribute("href"))
#     driver.quit()
