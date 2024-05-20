import gzip
import json

import urllib.request
import xml.etree.ElementTree as ET

# URL of the gzipped XML file
url = "https://www.daraz.com.bd/sitemap-categories-1.xml.gz"

# Download the gzipped XML file
urllib.request.urlretrieve(url, "sitemap-categories-1.xml.gz")

# Extract the gzipped file
with gzip.open("sitemap-categories-1.xml.gz", "rb") as f_in:
    with open("../../store/daraz.xml", "wb") as f_out:
        f_out.write(f_in.read())

# Parse the XML file
tree = ET.parse("data.xml")
root = tree.getroot()

# Access and process the XML data
# Example: Print the tag names of all elements

categories = []

for element in root.iter():
    if element.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc":
        categories.append(element.text)



# Extract category names from the links
category_names = [link.split("/")[3] for link in categories]
print (category_names)

# Create a dictionary with the category names
data = {"categories": category_names}

# Write the data to a JSON file
with open("../../store/daraz-categories.json", "w") as f:
    json.dump(data, f)