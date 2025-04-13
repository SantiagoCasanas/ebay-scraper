from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import List
from scraper import search_items_on_stock
from notifier import send_items_on_stock

app = FastAPI()

class StockCheckRequest(BaseModel):
    items_list: List[str]
    emails: List[EmailStr]
    base_url_itm: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/send-emails")
def search_items(request: StockCheckRequest, background_tasks: BackgroundTasks):
    items_on_stock = search_items_on_stock(request.items_list, request.base_url_itm)

    if not items_on_stock:
        return {"message": "No items on stock"}
    
    background_tasks.add_task(send_items_on_stock, items_on_stock, request.emails)
    return {"message": f"The following items are on stock:", "items": items_on_stock}
