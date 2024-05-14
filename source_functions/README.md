# 仮想環境のアクティブ化
```
# 仮想環境をアクティブ化
source env/bin/activate
```
# Flask サーバ立ち上げ方法
```
# 環境変数設定
project_id=matayuuu-agent-builder-demo
GOOGLE_APPLICATION_CREDENTIALS=key.json
FLASK_ENV=development

# 環境選択
# FLASK_APP=main.py
FLASK_APP=dev.py

# Flask 起動
flask run
```

# ローカルにリクエスト
```
# [共通]セッション ID を設定
session_id=12345
```

```
# add_to_shopping_cart
curl -X POST http://127.0.0.1:5000/add_to_shopping_cart?session_id=$session_id \
-H "Content-Type: application/json" \
-d '{"product": "MacBook Pro", "quantity": 7}'

# view_shopping_cart
curl -X POST http://127.0.0.1:5000/view_shopping_cart?session_id=$session_id

# remove_from_shopping_cart
curl -X POST http://127.0.0.1:5000/remove_from_shopping_cart?session_id=$session_id \
-H "Content-Type: application/json" \
-d '{"product": "MacBook Pro", "quantity": 6}'

# place_order
curl -X POST http://127.0.0.1:5000/place_order?session_id=$session_id \
-H "Content-Type: application/json" \
-d '{"shipping_address": "okinawa-ken"}'

# get_categories
curl -X POST http://127.0.0.1:5000/get_categories?session_id=$session_id

# get_product_names
curl -X POST http://127.0.0.1:5000/get_product_names?session_id=$session_id \
-H "Content-Type: application/json" \
-d '{"category": "PC"}'
```