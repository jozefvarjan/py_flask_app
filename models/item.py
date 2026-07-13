from db import db


class ItemTable(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    format = db.Column(db.String(5), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    def __repr__(self):
        return f"item: {self.title, self.format, self.year, self.price}"
 