from sqlalchemy_utils import URLType

from grocery_app import db
from grocery_app.utils import FormEnum

from flask_login import UserMixin

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

    def __repr__(self):
      return f'{self.title}, address: {self.address}'
class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(URLType)
    store_id = db.Column(
        db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users_shopping_list = db.relationship(
        'User', secondary='shopping_list_table', back_populates='shopping_list_items')

    def __repr__(self):
      return f'{self.name}, price: {self.price}'

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(128), nullable = False)
  shopping_list_items = db.relationship(
      "GroceryItem", secondary='shopping_list_table', back_populates="users_shopping_list")

shopping_list_table = db.Table('shopping_list',
    db.Column( 'user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('grocery_item_id', db.Integer, db.ForeignKey('grocery_item.id'))
)