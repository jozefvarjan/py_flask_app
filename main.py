from flask import Flask, request, Response



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

class ResponseMsgObj:
    def __new__(self, err_msg:dict[str, str | Response]):
        return err_msg


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
    response = Response()
    return ResponseMsgObj(
        {
        "status": response.status,
        "status_code": response.status_code,
        "data": new_store
        }
    )
    


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    response = Response()
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_item)
            return ResponseMsgObj(
                {
                    "status": response.status, 
                    "status_code": response.status_code
                }
            )
    return ResponseMsgObj(
        {
            "status_code": 404, 
            "message": f"{name} not found!"
        }
    )


@app.get("/store/<string:name>")
def get_store_item(name):
    for store in stores:
        if store["name"] == name:
            return ResponseMsgObj(
                {
                    "items": store["items"]
                }
            )
    return ResponseMsgObj(
        {
            "status_code": 404,
            "message": f"{name}: not found!"
        }
    )
    