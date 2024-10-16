from datetime import datetime
from .extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))
    category = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    internal_reference = db.Column(db.String(100))
    shell_id = db.Column(db.Integer)
    inventory_status = db.Column(db.Enum('INSTOCK', 'LOWSTOCK', 'OUTOFSTOCK', name='inventory_status'), nullable=False)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "internalReference": self.internal_reference,
            "shellId": self.shell_id,
            "inventoryStatus": self.inventory_status,
            "rating": self.rating,
            "createdAt": self.created_at.timestamp(),
            "updatedAt": self.updated_at.timestamp(),
        }
