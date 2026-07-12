from db import db
from models.item import ItemTable


def item_select_id(id):
    return db.session.get(ItemTable, id)


def item_select_all():
    return db.session.execute(db.select(ItemTable)).scalars().all()


def item_save(item):
    db.session.add(item)
    db.session.commit()
    return item


def item_delete(item):
    db.session.delete(item)
    db.session.commit()
