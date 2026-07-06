import uuid
from flask import Flask, request, Response
from flask_smorest import abort
from db import stores, items


app = Flask(__name__)


class ResponseMsgObj:
    def __new__(self, err_msg:dict[str, str | Response]):
        return err_msg



# --- store(s)

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
    

@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    try:
        stores[store_id] = {"id": store_id, "name": store_data["name"]}
        return {"store": stores[store_id]}
    except KeyError: abort(404, message="not found")


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"msg": f"store: {store_id} deleted."}
    except KeyError:
        abort(404, message=f"store: {store_id} not found!")


@app.delete("/stores")   
def delete_stores():
    for store in list(stores.keys()):
        del stores[store]
    return {"msg": "all stores deleted"} 


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


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    try:
        items[item_id] = item_data
        return items[item_id]
    except KeyError:
        abort(404, message=f"item: {item_id} not found!")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
    except KeyError:
        abort(404, message=f"item: {item_id} not found!")
    