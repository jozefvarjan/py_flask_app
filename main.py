from flask import Flask, request



app = Flask(__name__)


stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]


@app.route('/')
def root(): 
    return '<b>This is root app screen!</b>'


@app.route('/stores')
def get_stores():
    return {
        "stores": stores
        }


@app.route('/users/<user>')
def get_user(user):
    import os
    return {
        "user": user,
        "uname": str(os.environ['USERNAME'])
    }


@app.post('/store')
def create_store(): 
    request_data = request.get_json()
    new_store = {"name": request_data['name'], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for obj in stores:
        if obj["name"] == name:
            obj["items"].append({"name": request_data["name"], "price": 0.00})
    return "updated", 201

