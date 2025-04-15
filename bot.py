from notifier import send_items_on_stock
from scraper import search_items_on_stock
import pandas as pd

def main():
    items = pd.read_excel("items.xlsx")
    items = items.values.tolist()

    items_on_stock = search_items_on_stock(items)
    
    if items_on_stock:
        send_items_on_stock(items_on_stock, ["partesyaccesoriostec@gmail.com", "santiago.casanas@correounivalle.edu.co"])
    else:
        print("No items on stock")

if __name__ == "__main__":
    main()