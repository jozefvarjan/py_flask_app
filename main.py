import uuid
from flask import Flask, request, Response
from db import stores, items


app = Flask(__name__)


class ResponseMsgObj:
    def __new__(self, err_msg:dict[str, str | Response]):
        return err_msg



# --- store(s)

@app.get('/stores')
def get_stores():
    return {
        "stores": list(stores.values())
        }


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return {"store": stores[store_id]}
    except KeyError:
        response = Response()
        return ResponseMsgObj(
            {
                "status_code": response.status_code,
                "status": response.status,
                "err_msg": f"store: {stores[store_id]} not found!"
            }
        )


@app.post('/store')
def create_store(): 
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {"id": store_id, **store_data}
    stores[store_id] = new_store
    response = Response()
    return ResponseMsgObj(
        {
        "status": response.status,
        "status_code": response.status_code,
        "data": new_store
        }
    )



# --- item(s)

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return ResponseMsgObj(
            {
                "status_code": 404,
                "message": f"{items[item_id]}: not found!"
            }
        )
    

@app.get("/items")
def get_items():
    return {"items": list(items.values())}


@app.post("/item")
def create_item():
    item_data = request.get_json()
    response = Response()

    item_id = uuid.uuid4().hex
    item = {"id": item_id, **item_data}
    items[item_id] = item
    return ResponseMsgObj(
        {
            "status": response.status, 
            "status_code": response.status_code,
            "payload": items[item_id]
        }
    )


    