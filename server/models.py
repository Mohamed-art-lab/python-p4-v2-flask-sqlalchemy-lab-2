from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# Define metadata for the database
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Create SQLAlchemy instance with custom metadata
db = SQLAlchemy(metadata=metadata)

# Define Customer model
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    # Define columns
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define relationship with reviews
    reviews = relationship('Review', back_populates='customer')

    # Define association proxy to get items through reviews relationship
    items = association_proxy('reviews', 'item')

    # Serialization rules
    serialize_rules = ('-reviews.customer', )

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

# Define Item model
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    # Define columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(db.Float)

    # Define relationship with reviews
    reviews = relationship('Review', back_populates='item')

    # Serialization rules
    serialize_rules = ('-reviews.item', )

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

# Define Review model
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    # Define columns
    id = Column(Integer, primary_key=True)
    comment = Column(String)

    # Define foreign keys and relationships
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='reviews')

    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship('Item', back_populates='reviews')

    # Serialization rules
    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __repr__(self):
        return f'<Review {self.id}>'