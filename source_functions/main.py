"""Retail recommendations and search"""

import json
import os
import random
import string

import firebase_admin
from firebase_functions import https_fn
import flask
import google.auth
import google.auth.transport.requests
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

firebase_admin.initialize_app()
app = flask.Flask(__name__)

creds, project = google.auth.default()
project_id = os.environ.get("project_id", "Specified environment variable is not set.")
db = firestore.Client(project=project_id, database="agent-database")


@app.post("/add_to_shopping_cart")
def add_to_shopping_cart():
  """Add an product to the shopping cart.

  Returns:
    status and shopping cart.
  """
  if not (flask.request.args and "session_id" in flask.request.args):
    return flask.jsonify({"status": "error: session_id not found"})
  session_id = flask.request.args["session_id"]
  session_doc_ref = db.collection("google_store_sessions").document(session_id)
  session_doc = session_doc_ref.get().to_dict()

  if "product" not in flask.request.get_json():
    return {"status": "error: Missing product"}
  product = flask.request.get_json()["product"]
  if "quantity" not in flask.request.get_json():
    return {"status": "error: Missing quantity"}
  quantity = flask.request.get_json()["quantity"]

  shopping_cart = {}
  if session_doc and "shopping_cart" in session_doc:
    shopping_cart = session_doc["shopping_cart"]
  if product in shopping_cart:
    shopping_cart[product] = shopping_cart[product] + quantity
  else:
    shopping_cart[product] = quantity
  session_doc_ref.set({"shopping_cart": shopping_cart}, merge=True)
  return {"status": "success", "shopping_cart": shopping_cart}


@app.post("/view_shopping_cart")
def view_shopping_cart():
  """View products in shopping cart.

  Returns:
    status and shopping cart.
  """
  if not (flask.request.args and "session_id" in flask.request.args):
    return flask.jsonify({"status": "error: session_id not found"})
  session_id = flask.request.args["session_id"]
  session_doc_ref = db.collection("google_store_sessions").document(session_id)
  session_doc = session_doc_ref.get().to_dict()

  shopping_cart = {}
  if session_doc and "shopping_cart" in session_doc:
    shopping_cart = session_doc["shopping_cart"]
  return {"status": "success", "shopping_cart": shopping_cart}


@app.post("/remove_from_shopping_cart")
def remove_from_shopping_cart():
  """Remove product from shopping cart.

  Returns:
    status and shopping cart.
  """
  if not (flask.request.args and "session_id" in flask.request.args):
    return flask.jsonify({"status": "error: session_id not found"})
  session_id = flask.request.args["session_id"]
  session_doc_ref = db.collection("google_store_sessions").document(session_id)
  session_doc = session_doc_ref.get().to_dict()

  product = flask.request.get_json()["product"]
  quantity = flask.request.get_json()["quantity"]
  shopping_cart = {}
  if session_doc and "shopping_cart" in session_doc:
    shopping_cart = session_doc["shopping_cart"]
  if product not in shopping_cart:
    return {"status": "error: product not found"}
  shopping_cart[product] = shopping_cart[product] - quantity
  if shopping_cart[product] <= 0:
    shopping_cart.pop(product, None)
  session_doc_ref.set({"shopping_cart": shopping_cart}, merge=True)
  return {"status": "success", "shopping_cart": shopping_cart}


@app.post("/place_order")
def place_order():
  """Place an order.

  Returns:
    status, shopping cart, and confirmation number.
  """
  if not (flask.request.args and "session_id" in flask.request.args):
    return flask.jsonify({"status": "error: session_id not found"})
  session_id = flask.request.args["session_id"]
  session_doc_ref = db.collection("google_store_sessions").document(session_id)
  session_doc = session_doc_ref.get().to_dict()

  shopping_cart = {}
  if session_doc and "shopping_cart" in session_doc:
    shopping_cart = session_doc["shopping_cart"]
  if len(shopping_cart) == 0:
    return {"status": "error: shopping cart is empty"}
  confirmation_number = "".join(
      random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
  )

  ### 開発中 ###
  # 住所の取得
  shipping_address = "未入力"
  if "shipping_address" in flask.request.get_json():
    shipping_address = flask.request.get_json()["shipping_address"]
  # 注文の作成
  order_session_doc_ref = db.collection("orders").document(session_id)
  order_session_doc_ref.set({"order_details": shopping_cart, "shipping_address": shipping_address}, merge=True)

  # カートの削除
  session_doc_ref.delete()
  #############

  return {"status": "success", "shopping_cart": shopping_cart, "confirmation_number": confirmation_number}


@app.post("/get_product_names")
def get_product_names():
  """Get product names from product catalog.

  Returns:
    status and list of product name.
  """
  input_category = flask.request.get_json()["category"]

  exist_category_list = []
  product_doc_ref = db.collection('products')
  product_docs = product_doc_ref.get()
  for product_doc in product_docs:
    product = product_doc.to_dict()
    exist_category_list.append(product["category"])

  product_name_list = []
  if input_category in exist_category_list:
    query = product_doc_ref.where(filter=FieldFilter("category", "==", input_category))
    sort_name_docs = query.get()
    for sort_name_doc in sort_name_docs:
      sort_name = sort_name_doc.to_dict()
      product_name_list.append(sort_name["name"])
  return {"status": "success", "product_names": product_name_list}

@app.post("/get_categories")
def get_categories():
  """Get categories from store.

  Returns:
    status and list of categories.
  """
  product_doc_ref = db.collection('products')
  product_docs = product_doc_ref.get()

  category_list = []

  for product_doc in product_docs:
      product = product_doc.to_dict()
      category_list.append(product["category"])

  # リスト内要素の重複排除
  distinct_category_list = list(set(category_list))
  print(f"distinct_category_list: {distinct_category_list}")
  return {"status": "success", "categories": distinct_category_list}

@https_fn.on_request()
def main(req: https_fn.Request) -> https_fn.Response:
  auth_req = google.auth.transport.requests.Request()
  creds.refresh(auth_req)
  print("Creds", creds)
  with app.request_context(req.environ):
    return app.full_dispatch_request()