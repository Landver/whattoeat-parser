import re
import csv
import json
import time

# urllib is needed to convert hebrew language
import urllib

import requests

from bs4 import BeautifulSoup


all_attributes = [
    "Name",
    "Url",
    "Picture",
    "contains",
    "May contain",
    "Nutritional value",
    "category",
]
products = []


def get_content():
    with open("data.csv", "w", encoding="utf-8", newline="") as writer_file:
        csv_writer = csv.writer(writer_file, quoting=csv.QUOTE_ALL, delimiter="\t")
        csv_writer.writerow(all_attributes)
        with open("links.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                product = {}
                html_content = requests.get(line[0]).content
                soup = BeautifulSoup(html_content, "html.parser")
                name = (
                    soup.find("h1", class_="product_title")
                    .get_text()
                    .replace("\n", "")
                    .replace(".", "")
                )
                info = soup.find(
                    "div", {"class": "woocommerce-product-details__short-description"}
                )
                product["name"] = name
                product["url"] = urllib.parse.unquote(line[0])
                product["picture"] = soup.find("img", {"class": "wp-post-image"}).get(
                    "src"
                )
                # getting info about what ingridients product contains and cleaning it from unnecessary words
                try:
                    product["Contains"] = (
                        info.find(
                            re.compile("(p|h3|span)"),
                            string=re.compile("(מוצר זה |מוצר זה מכיל|מכיל)"),
                        )
                        .get_text()
                        .replace(":", "")
                        .replace(".", "")
                    )
                    product["Contains"] = (
                        product["Contains"]
                        .replace("מוצר זה מכיל", "")
                        .replace("מוצר זה", "")
                        .replace(".", "")
                    )
                    product["Contains"] = (
                        product["Contains"].replace(r".\xa0", "").replace("מכיל", "")
                    )
                except:
                    product["Contains"] = ""
                # getting info about what ingridients product may contain and cleaning it from unnecessary words
                try:
                    product["May contain"] = (
                        info.find(
                            re.compile("p|h3|span"), string=re.compile("עלול להכיל")
                        )
                        .get_text()
                        .replace(":", "")
                        .replace(".", "")
                    )
                    product["May contain"] = (
                        product["May contain"]
                        .replace("עלול להכיל", "")
                        .replace(r".\xa0", "")
                        .replace(r"מוצר זה", "")
                        .replace(".", "")
                    )
                except:
                    product["May contain"] = ""
                try:
                    table = soup.find("table")
                    # searcing header with names of columns
                    thead = table.find("thead")
                    th = thead.find_all("th")
                    product["Nutritional value"] = ""
                    # getting that names
                    for el in th:
                        if el != th[0]:
                            product["Nutritional value"] = " | ".join(
                                [
                                    product["Nutritional value"],
                                    el.get_text().replace("\n", ""),
                                ]
                            )
                        else:
                            product["Nutritional value"] = "".join(
                                [
                                    product["Nutritional value"],
                                    el.get_text().replace("\n", ""),
                                ]
                            )
                    product["Nutritional value"] = f"{product['Nutritional value']}\\n"
                    # going through all rows in table and getting info from it
                    tbody = table.find("tbody")
                    trs = tbody.find_all("tr")
                    for tr in trs:
                        tds = tr.find_all("td")
                        for td in tds:
                            text = td.get_text().replace("\n", "")
                            if not text:
                                text = "-"
                            if td != tds[0]:
                                product["Nutritional value"] = " | ".join(
                                    [
                                        product["Nutritional value"],
                                        text.replace(".", ""),
                                    ]
                                )
                            else:
                                product["Nutritional value"] = "".join(
                                    [
                                        product["Nutritional value"],
                                        text.replace(".", ""),
                                    ]
                                )
                        product[
                            "Nutritional value"
                        ] = f"{product['Nutritional value']}\\n"
                except:
                    # If table does not exist
                    product["Nutritional value"] = ""
                product["Category"] = ""
                with open(
                    "category_product_links.csv", "r", encoding="utf-8"
                ) as read_file:
                    csv_reader = csv.reader(read_file, delimiter="\t")
                    for line in csv_reader:
                        if urllib.parse.unquote(line[0]) == product["url"]:
                            product["Category"] = product["Category"] + f"{line[1]} | "
                            # print(product["url"])
                            # print(urllib.parse.unquote(line[0]))
                product["Category"] = product["Category"][0:-3]
                products.append(product)
                csv_writer.writerow(
                    [
                        product["name"],
                        product["url"],
                        product["picture"],
                        product["Contains"],
                        product["May contain"],
                        product["Nutritional value"],
                        product["Category"],
                    ]
                )
                time.sleep(2)

    # Making json file from given data
    with open("data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(products, indent=4, ensure_ascii=False))
