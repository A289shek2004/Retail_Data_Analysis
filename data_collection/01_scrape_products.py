import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://pexpo.in"

collections = {
    "Best Sellers": "https://pexpo.in/collections/home-page-best-sellers",
    "Kids": "https://pexpo.in/collections/home-page-kids-collection",
    "Art": "https://pexpo.in/collections/home-page-art-collection",
    "Accessories": "https://pexpo.in/collections/accessories"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_products = []
product_id = 1
def scrape_collection(collection_name, url):
    global product_id

    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("div", class_="card-wrapper")

    for product in products:
        try:
            name_tag = product.find("h3")
            price_tag = product.find("span", class_="price-item")
            link_tag = product.find("a", href=True)

            if not name_tag or not link_tag:
                continue

            product_name = name_tag.text.strip()
            raw_price = price_tag.text.strip() if price_tag else None
            product_url = BASE_URL + link_tag["href"]

            all_products.append({
                "product_id": f"P{product_id}",
                "product_name": product_name,
                "raw_price": raw_price,          # ← RAW
                "collection": collection_name,
                "product_url": product_url
            })

            product_id += 1

        except Exception as e:
            print(f"Skipping product due to error: {e}")

for collection, url in collections.items():
    print(f"Scraping {collection}...")
    scrape_collection(collection, url)
    time.sleep(2)  # polite delay

df = pd.DataFrame(all_products)
df.to_csv(r"E:\pexpo_sales_analysis\data\raw\products.csv", index=False)
print("RAW product data saved successfully.")
print("Scraping completed. products.csv saved.")
