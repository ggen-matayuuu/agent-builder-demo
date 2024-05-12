import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


project_id = "matayuuu-agent-builder-demo"
db = firestore.Client(project=project_id, database="agent-database")


product = "MacBook Pro"
quantity = 2

product_doc_ref = db.collection('products').document(product)
product_dict = product_doc_ref.get().to_dict()

print(product_dict)
product_dict["quantity"] = product_dict["quantity"] - quantity
print(product_dict)

if product_dict["quantity"] <= 0: # product_dict["quantity"] < 0 の場合の処理はデモのため省略
    product_doc_ref.delete()
    print("complate remove!")
else:
    product_doc_ref.set(product_dict, merge=True)
    print("complate update!")

# query = product_doc_ref.where(filter=FieldFilter("name", "==", product))
# sort_product_doc = query.get()
# sort_product_dict = sort_product_doc[0].to_dict()

# # print(sort_product_doc[0].to_dict())
# # print(type(sort_product_doc[0]))
# # print(len(sort_product_doc))
# # print(dir(sort_product_doc[0]))

# print(sort_product_dict)
# sort_product_dict["quantity"] = sort_product_dict["quantity"] - quantity
# print(sort_product_dict)

# if sort_product_doc["quantity"] <= 0:
# sort_product_doc.pop()