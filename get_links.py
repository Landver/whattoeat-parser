import time
import csv
from bs4 import BeautifulSoup
import requests


def get_links():
    with open("links.csv", "w", encoding="utf-8", newline="") as file:
        csv_writer = csv.writer(file)
        for i in range(1, 9):
            html_content = requests.get(
                f"https://whattoeat.co.il/?jsf=epro-products&pagenum={i}"
            ).content
            soup = BeautifulSoup(html_content, "html.parser")
            # Getting table with products
            ul = soup.find("ul", class_="products")
            # finding a tags of products
            links = ul.find_all(
                "a",
                {
                    "class": "woocommerce-LoopProduct-link woocommerce-loop-product__link"
                },
            )
            # getting links from tags and writing it in csv file
            for link in links:
                csv_writer.writerow([link.get("href")])
