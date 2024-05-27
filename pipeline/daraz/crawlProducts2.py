from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from xata.client import XataClient
import re

import concurrent.futures

xata = XataClient(api_key="xau_vhTUq5SIpC2R5u7ua6zDHPKjQhkpGT9e2", db_url="https://Mobin-Chowdhury-s-workspace-eh41hn.us-east-1.xata.sh/db/productSearch:main")

skippedCategories = [
    "medicine-hospital-dental-equipments",
    "microwave",
    "stand-fan",
    "vacuum-cleaners",
    "humidifier-parts-&-accessories"
]

def remove_special_characters(word):
    # Remove special characters and replace with space
    stri = ''.join(letter for letter in word if letter.isalnum())
    return stri

def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(s) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])


def uploadProductLinks(table_name, productLink):
    table_schema = {
        "columns": [
            {
                "name": "link",
                "type": "string",
            },
        ]
    }
    try:
        assert xata.table().create(table_name).is_success()
        resp = xata.table().set_schema(table_name, table_schema)
        assert resp.is_success(), resp

        record = {
            "link": productLink
        }
        respi = xata.records().insert(table_name, record)
        assert respi.is_success(), respi
    except AssertionError as error:
        record = {
            "link": productLink
        }
        respi = xata.records().insert(table_name, record)
        assert respi.is_success(), respi


def process_category(category):
    print(f'Category: {category} converted to {to_camel_case(remove_special_characters(category))}')
    url = f'https://www.daraz.com.bd/{category}/'
    print(f"Processing category: {category}")
    driver.get(url)
    totalProducts = driver.find_element(By.XPATH, "//div[@class=' tips--QRnmZ']//span[1]").text
    totalProducts = totalProducts.replace(" items found for", "")
    totalProducts = totalProducts.replace(",", "")
    totalProducts = int(totalProducts)
    print(f"Total products: {totalProducts}")
    if totalProducts == 0:
        print(f"Skipping category {category} as it has no products")
        return category, []

    products = driver.find_elements(By.ID, "id-a-link")
    productPagesCount = driver.find_element(By.XPATH, "//ul[@unselectable='unselectable']/*[last()-1]").text
    print(f"Total pages: {productPagesCount}")
    productLinks = []

    # for i in range(1, int(productPagesCount)):
    #     print(f"Processing page {i} of category {category}")
    #     driver.get(f'{url}?page={i}')
    #     products = driver.find_elements(By.ID, "id-a-link")
    #     for product in products:
    #         productLinks.append(product.get_attribute("href"))
    #         uploadProductLinks(to_camel_case(remove_special_characters(category)), product.get_attribute("href"))
    #         print(product.get_attribute("href"))

    return category, productLinks


# Open the browser
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')

options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Open and parse JSON file
with open('../../store/daraz-categories.json') as file:
    data = json.load(file)
    categories = data.get('categories')
    print(f"Total categories: {len(categories)}")
    for category in skippedCategories:
        categories.remove(category)

    # Create a ThreadPoolExecutor with max_workers set to the number of categories
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(categories)) as executor:
        # Submit each category to the executor
        futures = [executor.submit(process_category, category) for category in categories]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

        # Get the results from the completed futures
        result = {future.result()[0]: future.result()[1] for future in futures}

# Write the result to a JSON file
with open('../../store/daraz-products.json', 'w') as file:
    json.dump(result, file)
