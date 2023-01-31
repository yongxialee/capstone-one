
from app import db
from models import Product
import requests
API_BASE_URL="https://api.sampleapis.com/coffee"
db.metadata.clear()
db.drop_all()
db.create_all()

def save_all_items():
    """Call to API for all items and save them to db."""

    res = requests.get(f"{API_BASE_URL}/hot")
    resp = requests.get(f"{API_BASE_URL}/iced")
    data = res.json()
    data_c=resp.json()
    for item in data:
        p = Product(
                title = item['title'],
                type = "hot",
                ingredients=item['ingredients'],
                image=item['image'],
                description =item['description'])
        db.session.add(p)
    for i in data_c:
        p_c = Product(
                title = i['title'],
                type = "iced",
                ingredients=i['ingredients'],
                image=i['image'],
                description =i['description'])
        db.session.add(p_c)
    
  
   
    db.session.commit()

save_all_items()