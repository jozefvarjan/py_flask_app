from db import db
from models.store import StoreModel


def store_select_id(id):
    return db.session.get(StoreModel, id)


def store_select_all():
    return db.session.execute(db.select(StoreModel)).scalars().all()


def store_save(store):
    db.session.add(store)
    db.session.commit()
    return store


def store_delete(store):
    db.session.delete(store)
    db.session.commit()


def store_delete_all():
    db.session.execute(db.delete(StoreModel))
    db.session.commit()
