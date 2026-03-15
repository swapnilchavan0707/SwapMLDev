from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the db object; it will be bound to the app in app.py
db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_cost = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    competitor_price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, default=10)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to track every price change for the graph
    logs = db.relationship('PriceLog', backref='product', lazy=True)


class PriceLog(db.Model):
    __tablename__ = 'price_logs'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)