import re
import csv
import time
import requests
import urllib.parse

from bs4 import BeautifulSoup

def get_category_products_links():
    with open("category_product_links.csv", "w", newline="", encoding="utf-8") as write_file:
        csv_writer = csv.writer(write_file, delimiter="\t")
        with open("category_links.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for page in csv_reader:
                for i in range(1, 9):
                    print(page[0]+str(i))
                    http_content = requests.get(page[0]+str(i)).content
                    soup = BeautifulSoup(http_content, "html.parser")
                    links = soup.find_all("a", {"class": "woocommerce-LoopProduct-link woocommerce-loop-product__link"})
                    if links:
                        for link in links:
                            csv_writer.writerow([urllib.parse.unquote(link.get("href")), page[1]])
                            print(urllib.parse.unquote(link.get("href")))
                    else:
                        continue
                    time.sleep(1)
