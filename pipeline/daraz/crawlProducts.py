from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
html = driver.page_source
print(html)
driver.quit()
