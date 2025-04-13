import asyncio
import time
import os
from dotenv import load_dotenv
import threading
from scraper import search_items_on_stock
from notifier import send_items_on_stock

load_dotenv()

# Configura aquí tus datos
ITEMS = ["276553848381", "256574025033"]
EMAILS = ["santiago.casanas@correounivalle.edu.co"]
BASE_URL = "https://www.ebay.com/itm/"

INTERVAL_SECONDS = os.getenv("INTERVAL_SECONDS", 60)

def scheduled_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        print("Ejecutando tarea programada...")
        try:
            items_on_stock = search_items_on_stock(ITEMS, BASE_URL)
            print(f"Items on stock: {items_on_stock}")
            #if items_on_stock:
            #    send_items_on_stock(items_on_stock, EMAILS)
        except Exception as e:
            print(f"Error en la tarea programada: {e}")
        time.sleep(INTERVAL_SECONDS)  # este no es await

def start_scheduler():
    thread = threading.Thread(target=scheduled_task, daemon=True)
    thread.start()