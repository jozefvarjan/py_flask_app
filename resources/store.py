import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store")
class Stores(MethodView):

    def post(self):
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {"id": store_id, **store_data}
        stores[store_id] = new_store
        return new_store


    def get(self):
        return {"stores": list(stores.values())}
    

    def delete(self):
        for store in list(stores.keys()):
            del stores[store]
        return {"msg": "all stores deleted"} 
    


@blp.route("/store/<string:store_id>")
class Store(MethodView):

    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message=f"store: {store_id} not found!")


    def put(self, store_id):
            store_data = request.get_json()
            try:
                stores[store_id] = {"id": store_id, "name": store_data["name"]}
                return {"store": stores[store_id]}
            except KeyError: abort(404, message="not found")


    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"msg": f"store: {store_id} deleted."}
        except KeyError:
            abort(404, message=f"store: {store_id} not found!")



