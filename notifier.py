import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

def send_items_on_stock(items, emails):
	if len(items) > 0:
		print(os.environ['EMAIL_USER'])
		print(os.environ['EMAIL_PASS'])
		yag = yagmail.SMTP(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
		subject = "Items on stock"
		body = f"The next items are on stock:\n\n" + "\n".join(items)
		yag.send(to=emails, subject=subject, contents=body)
