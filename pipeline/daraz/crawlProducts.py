from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from xata.client import XataClient
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

xata = XataClient(api_key="xau_vhTUq5SIpC2R5u7ua6zDHPKjQhkpGT9e2",db_url="https://Mobin-Chowdhury-s-workspace-eh41hn.us-east-1.xata.sh/db/productSearch:main")

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


# # Usage example:
# category = "stand-$&-%-fan$${}"
# camel_case_category = to_camel_case(remove_special_characters(category))
# print(camel_case_category)

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
        
    
# Open the browser
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')

options.add_argument("start-maximized"); 
options.add_argument("disable-infobars"); 
options.add_argument("--disable-extensions"); 
options.add_argument("--disable-gpu"); 
options.add_argument("--disable-dev-shm-usage"); 
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)


result = {}

def addInErrorProducts(category, productLink):
    table_name = "error_products"
    table_schema = {
        "columns": [
            {
                "name": "category",
                "type": "string",
            },
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
            "category": category,
            "link": productLink
         }
        respi = xata.records().insert(table_name, record)
        assert respi.is_success(), respi
    except AssertionError as error:
        
        record = {
            "category": category,
            "link": productLink
         }
        respi = xata.records().insert(table_name, record)
        assert respi.is_success(), respi

def addInErrorCategories(category):
    table_name = "error_categories"
    table_schema = {
        "columns": [
            {
                "name": "category",
                "type": "string",
            },
        ]
    }
    try:
        
        assert xata.table().create(table_name).is_success()
        resp = xata.table().set_schema(table_name, table_schema)
        assert resp.is_success(), resp
         
        record = {
            "category": category
         }
        respi = xata.records().insert(table_name, record)
        assert respi.is_success(), respi
    except AssertionError as error:
        
        record = {
            "category": category
         }
        respi = xata.records().insert(table_name, record)
        assert respi.is_success(), respi

def updateTotalProducts(totalProducts):
    table_name = "total_productx"
    table_schema = {
        "columns": [
            {
                "name": "total_products",
                "type": "string",
            },
        ]
    }
    try:
        assert xata.table().create(table_name).is_success()
        resp = xata.table().set_schema(table_name, table_schema)
        assert resp.is_success(), resp
        record = {
                "total_products": str(totalProducts)
            }
        respi = xata.records().insert_with_id(table_name, table_name, record)
        assert respi.is_success(), respi
    except AssertionError as error:
        try:
            print(f"Error creating total products: {str(error)}")
            record = {
                "total_products": str(totalProducts)
            }
            respi = xata.records().insert_with_id(table_name, table_name, record)
            assert respi.is_success(), respi
        except Exception as error:
            print(f"Error inserting total products: {str(error)}")
            try:
                print(f"Error updating total products: {str(error)}")
                record = {
                    "total_products": str(totalProducts)
                }
                respi = xata.records().update(table_name, table_name, record)
                assert respi.is_success(), respi
            except Exception as error:
                print(f"Error updating total products: {str(error)}")
                return False

def getTotalProducts():
    table_name = "total_productx"
    try:
        resp = xata.records().get(table_name,table_name)
        assert resp.is_success(), resp
        return int(resp['total_products'])
    except AssertionError as error:
        return 0

def setLastPageCount(category, lastPageCount):
    table_name = "last_page_countx"
    table_schema = {
        "columns": [
            {
                "name": "category",
                "type": "string",
            },
            {
                "name": "last_page_count",
                "type": "string",
            },
        ]
    }
    try:
        
        assert xata.table().create(table_name).is_success()
        resp = xata.table().set_schema(table_name, table_schema)
        assert resp.is_success(), resp
         
        record = {
            "category": category,
            "last_page_count": str(lastPageCount)
         }
        respi = xata.records().insert_with_id(table_name, table_name, record)
        assert respi.is_success(), respi
    except AssertionError as error:
        try:
            print(f"Error SetLastPageCount: {str(error)}")
            record = {
                "category": category,
                "last_page_count": str(lastPageCount)
            }
            respi = xata.records().insert_with_id(table_name, table_name, record)
            assert respi.is_success(), respi
        except Exception as error:
            print(f"Error inserting last page count: {str(error)}")
            try: 
                record = {
                    "category": category,
                    "last_page_count": str(lastPageCount)
                }
                respi = xata.records().update(table_name, table_name, record)
                assert respi.is_success(), respi
            except Exception as error:
                print(f"Error updating last page count: {str(error)}")
                return False

def getLastPageCount():
    table_name = "last_page_countx"
    try:
        resp = xata.records().get(table_name,table_name)
        assert resp.is_success(), resp
        return {"category":resp["category"], "lastPageCount":int(resp["last_page_count"])}
    except AssertionError as error:
        return {"category":None, "lastPageCount":0}

# **** Main Segment ****
# Open and parse JSON file
isDriverOpen = False
with open('../../store/daraz-categories.json') as file:
    data = json.load(file)
    categories = data.get('categories')
    #organize the categories alphabetically
    categories.sort()
    print(f"Total categories: {len(categories)}")
    lastPageCount = getLastPageCount()
    totalProducts = getTotalProducts()
    print(f"Total products: {totalProducts}")
    if(lastPageCount["category"] is not None):
        #Skip all the categories before the last category
        print(f"Last category: {lastPageCount['category']}")
        new_categories = []
        found = False
        for category in categories:
            if category == lastPageCount["category"]:
                found = True
            if found:
                new_categories.append(category)
            else:
                print(f"Skipping category: {category}")
        categories = new_categories
    # for category in skippedCategories:
    #     categories.remove(category)
    print(f"Total categories: {len(categories)}")

    for category in categories:
        try:
            print(f'Category: {category} converted to {remove_special_characters(category)}')
            url = f'https://www.daraz.com.bd/{category}/'
            print(f"Processing category: {category}")
            if not isDriverOpen:
                isDriverOpen = True
                driver = webdriver.Chrome(options=options)
            driver.get(url)
            # totalProducts = driver.find_element(By.XPATH, "(//div[@class=' tips--QRnmZ']//span)[1]").text
            # totalProducts = totalProducts.replace(" items found for", "")
            # totalProducts = totalProducts.replace(",", "")
            # totalProducts = int(totalProducts)
            # print(f"Total products: {totalProducts}")
            # if(totalProducts == 0):
            #     print(f"Skipping category {category} as it has no products")
            #     continue
            products = driver.find_elements(By.ID, "id-a-link")
            productPagesCount = driver.find_element(By.XPATH, "//ul[@unselectable='unselectable']/*[last()-1]").text
            if (lastPageCount["category"] is not None and category == lastPageCount["category"] and (lastPageCount["lastPageCount"] +1) == int(productPagesCount)):
                continue
            print(f"Total pages: {productPagesCount}")
            
            
            for i in range(lastPageCount["lastPageCount"] +1, int(productPagesCount)+1):
                if not isDriverOpen:
                    isDriverOpen = True
                    driver = webdriver.Chrome(options=options)
                print(f"Processing page {i} of category {category}")
                driver.get(f'{url}?page={i}')
                productLinks = []
                productImgLinks = []
                products = driver.find_elements(By.ID, "id-a-link")
                for product in products:
                    try:
                        productLinks.append(product.get_attribute("href"))
                        uploadProductLinks((f'{remove_special_characters(category)}-links'), product.get_attribute("href"))
                        img = product.find_element(By.TAG_NAME, "img").get_attribute("src")
                        productImgLinks.append(img)
                        print(img)
                        print(product.get_attribute("href"))
                        totalProducts += 1
                        updateTotalProducts(totalProducts)
                    except Exception as e:
                        print(f"Error processing product: {str(e)}")
                        addInErrorProducts(category, product.get_attribute("href"))
                        continue
                for iLink in range(len(productLinks)):
                    try:
                        driver.get(productLinks[iLink])
                        try:
                            name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pdp-mod-product-badge-title"))).text
                        except Exception as e:
                            print(f"Error getting name: {str(e)}")
                            name = ""
                        try:
                            price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'pdp-price pdp-price_type_normal')]"))).text
                        except Exception as e:
                            print(f"Error getting price: {str(e)}")
                            price = ""
                        try:
                            desc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='html-content pdp-product-highlights']"))).text
                        except Exception as e:
                            print(f"Error getting description: {str(e)}")
                            desc = ""
                        try:
                            details = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@class='html-content detail-content']"))).text
                        except Exception as e:
                            print(f"Error getting details: {str(e)}")
                            details = ""
                        try:
                            discount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pdp-product-price__discount"))).text  
                        except Exception as e:
                            print(f"Error getting discount: {str(e)}")
                            discount = "0%"
                        try:
                            imgs = driver.find_element(By.CLASS_NAME, "next-slick-list").find_elements(By.TAG_NAME, "img")
                            imgSrc = [im.get_attribute("src") for im in imgs]
                            print(imgSrc)
                        except Exception as e:
                            print(f"Error getting image source: {str(e)}")
                            imgSrc = []

                        try:
                            mainImg = driver.find_element(By.CLASS_NAME, "gallery-preview-panel__image").get_attribute("src")
                        except:
                            mainImg = ""
                        
                        full_text = f'''
                        name: {name}
                        price: {price}
                        discount: {discount}
                        description:
                        {desc}
                        details:
                        {details}
                        img: {mainImg}
                        '''

                        print(full_text)
                    except Exception as e:
                        print(f"Error processing product: {str(e)}")
                        addInErrorProducts(category, productLinks[iLink])
                        continue
                
                # driver.quit()
                # isDriverOpen = False
                setLastPageCount(category, i)
            # print(f"Total Main products: {totalMainProducts + totalProducts}")
            # totalMainProducts += totalProducts
            # uploadProductLinks("total_products", str(totalProducts))
            result[category] = productLinks
        except Exception as e:
            print(f"Error processing category {category}: {str(e)}")
            addInErrorCategories(category)
            continue

       


# # Write the result to a JSON file
# with open('../../store/daraz-products.json', 'w') as file:
#     json.dump(result, file)

