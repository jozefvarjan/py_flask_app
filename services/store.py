from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import StoreModel
from repositories import store_repository as stores

from validation.schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            stores.store_save(store)
        except SQLAlchemyError:
            abort(500, message="error creating store")

        return store


@blp.route("/store/<int:store_id>")
class StoreById(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = stores.store_select_id(store_id)
        if store is None:
            abort(404, message=f"store: {store_id} not found!")
        return store

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = stores.store_select_id(store_id)
        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(id=store_id, **store_data)

        try:
            stores.store_save(store)
        except SQLAlchemyError:
            abort(500, message="error saving store")

        return store

    def delete(self, store_id):
        store = stores.store_select_id(store_id)
        if store is None:
            abort(404, message=f"store: {store_id} not found!")
        stores.store_delete(store)
        return {"msg": f"store: {store_id} deleted."}


@blp.route("/stores")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.store_select_all()

    def delete(self):
        stores.store_delete_all()
        return {"msg": "stores deleted"}
