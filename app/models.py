import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pytz as pytz
from app import db


"""
class User(db.Model):
    # ...

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

"""

class Sales(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now(tz=pytz.timezone('America/Mexico_City')))
    quantity = db.Column(db.Integer)


db.Table('transaction',
         db.Column('product_id', db.Integer(), db.ForeignKey('product.id')),
         db.Column('sales_id', db.Integer(), db.ForeignKey('sales.id'))
         )


class Prices(db.Model):
    __tablename__ = 'price'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))




class Products(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cost_price = db.Column(db.Float)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer)
    prices = db.relationship("Prices", lazy='dynamic')
    sales = db.relationship("Sales", secondary='transaction', backref='products', lazy='dynamic')