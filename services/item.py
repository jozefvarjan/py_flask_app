from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import ItemTable
from repositories import item_repository as items

from validation.schemas import ItemSchema



blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class ItemById(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = items.item_select_id(item_id)
        if item is None:
            abort(404, message=f"item: {item_id} not found!")
        return item

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = items.item_select_id(item_id)
        if item:
            item.title = item_data["title"]
            item.format = item_data["format"]
            item.year = item_data["year"]
            item.price = item_data["price"]
        else:
            item = ItemTable(id=item_id, **item_data)

        try:
            items.item_save(item)
        except SQLAlchemyError:
            abort(500, message="error saving item")

        return item

    def delete(self, item_id):
        item = items.item_select_id(item_id)
        if item is None:
            abort(404, message=f"item: {item_id} not found!")
        items.item_delete(item)
        return {"msg": f"item: {item_id} deleted"}


@blp.route("/item")
class Item(MethodView):

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemTable(**item_data)
        try:
            items.item_save(item)
        except SQLAlchemyError:
            abort(500, message="error creating item")

        return item


@blp.route("/items")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.item_select_all()
