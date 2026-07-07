import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class ItemById(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message=f"item: {item_id} not found!")
        

    def put(self, item_id):
        item_data = request.get_json()
        try:
            items[item_id] = item_data
            return items[item_id]
        except KeyError:
            abort(404, message=f"item: {item_id} not found!")

    
    def delete(self, item_id):
        try:
            del items[item_id]
        except KeyError:
            abort(404, message=f"item: {item_id} not found!")



@blp.route("/item")
class Item(MethodView):

    def post(self):
        item_data = request.get_json()
       
        item_id = uuid.uuid4().hex
        item = {"id": item_id, **item_data}
        items[item_id] = item
        return items[item_id]



@blp.route("/items")
class Items(MethodView):
    
    def get(self):
        return {"items": list(items.values())}