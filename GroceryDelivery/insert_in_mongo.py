from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['food_delivery']  # Replace 'your_database' with your actual database name
collection = db['g_data']
coll=db['cart']# Replace 'your_collection' with your actual collection name

# Sample data to be stored
grocery_data = [
    # {"name": "Nascafe Coffee", "price": 170, "description": "Best Coffee", "dicount": -30, "rate": 3.5,
    #  "image_url": "/static/images/Cofee.jpg"},
    # {"name": "Nascafe Gold", "price": 350, "description": "Best Coffee", "dicount": 0, "rate": 4.5,
    #  "image_url": "/static/images/gold_cofee.jpg"},
    # {"name": "Maggi", "price": 12, "description": "Chhoti Bhukh Ka ilaj...", "dicount": 0, "rate": 4,
    #  "image_url": "/static/images/magee2.jpg"},
    # {"name": "Maggi Jumbo Pack", "price": 50, "description": "Chhoti Bhukh Ka ilaj...", "dicount": -5, "rate": 4.5,
    #  "image_url": "/static/images/magee.jpg"},
    # {"name": "Pasta", "price": 100, "description": "Pasta", "dicount": -10, "rate": 3.5,
    #  "image_url": "/static/images/pasta.jpg"},
    # {"name": "TATA Tea", "price": 252, "description": "Best Tea", "dicount": -5, "rate": 4.8,
    #  "image_url": "/static/images/tata_tea.jpg"},
    # {"name": "RedBull", "price": 125, "description": "Red Bull Gives you Weengs", "dicount": 0, "rate": 4.5,
    #  "image_url": "/static/images/redbull.jpg"},
    # {"name": "Pasta", "price": 100, "description": "Pasta", "dicount": -10, "rate": 3.5,
    #  "image_url": "/static/images/pasta.jpg"},
    {"total"}

]

# Insert data into MongoDB collection
def insert():
    coll.insert_many(grocery_data)
