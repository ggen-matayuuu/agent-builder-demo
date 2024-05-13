import os
from google.cloud import firestore


project_id = "matayuuu-agent-builder-demo"
db = firestore.Client(project=project_id, database="agent-database")

product_inventory_list = [
    {
        "category": "PC",
        "name": "Chromebook",
        "price": 100,
        "quantity": 10,
    },
    {
        "category": "PC",
        "name": "MacBook Pro",
        "price": 300,
        "quantity": 10,
    },
    {
        "category": "Phone",
        "name": "Google Pixel 8",
        "price": 100,
        "quantity": 10,
    },
    {
        "category": "Phone",
        "name": "iPhone 15 Pro",
        "price": 200,
        "quantity": 10,
    },
]

# 商品在庫の削除
for product_inventory in product_inventory_list:
    db.collection("products").document(product_inventory["name"]).delete()
print("Delete complate.")

# 商品在庫の作成
for product_inventory in product_inventory_list:
    db.collection("products").document(product_inventory["name"]).set(
        {
            "category"  : product_inventory["category"],
            "price"     : product_inventory["price"],
            "quantity"  : product_inventory["quantity"]
        },
        merge=True
    )
print("complate.")