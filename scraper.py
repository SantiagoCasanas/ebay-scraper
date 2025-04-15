import time
import re
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def search_items_on_stock(items) -> List[str]:
    options = Options()
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    options.add_argument("--enable-unsafe-swiftshadere")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920x1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    items_on_stock = []

    try:
        for item in items:
            search_url = item[1]
            max_price = float(item[2])
            max_price = max_price+(max_price*0.1)
            driver.get(search_url)
            time.sleep(3)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            try:
                spans = [span.get_text(strip=True) for span in soup.find_all("span", class_="ux-textspans")]
                prices = soup.find_all("div", class_="x-price-primary")
                price_ebay = prices[0].get_text(strip=True)
                price_ebay = re.search(r'\d+[\.,]?\d*', price_ebay)
                price_ebay = float(price_ebay.group().replace(',', '')) if price_ebay else 0.0
                agotado = any("Este artículo está agotado." in texto for texto in spans)

                if not agotado and price_ebay < max_price:
                    items_on_stock.append(search_url)


            except Exception as e:
                print(f"Error al analizar el contenido de {search_url}: {e}")
    finally:
        driver.quit()
    print(f"Items on stock: {items_on_stock}")
    return items_on_stock
