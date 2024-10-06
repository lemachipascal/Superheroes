from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    hero_power = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # add serialization rules
    serialize_only = ('id ', 'name', 'super_name')

    def __repr__(self):
        return f'<Hero {self.name}>'

# class Restaurant (db.Model, SerializerMixin):
#     __tablename__ = 'restaurants'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     address = db.Column(db.String)
    
#     #add relationship
#     restaurant_pizza = db.relationship('RestaurantPizza', backref='restaurant', cascade='all, delete-orphan')
#     #add serialization rules
#     serialize_only = ('id ', 'name', 'address')

#     def __repr__(self):
#         return f'<Restaurant {self.name}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    hero_powers = db.relationship('HeroPower', back_populates='power')

    # add serialization rules   
    serialize_only = ('id ', 'name', 'description')


    # add validation
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description

    def __repr__(self):
        return f'<Power {self.name}>'

# class Pizaa (db.Model, SerializerMixin):
#     __tablename__ = 'pizzas'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     ingredients = db.Column(db.String)

#     #add relationship
#     restaurant_pizza = db.relationship('RestaurantPizza', backref='pizza')
#     #add serialization rules
#     serialize_only = ('id ', 'name', 'ingredients')

#     def __repr__(self):
#         return f'<Pizza {self.name}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # add relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # add serialization rules
    serialize_only = ('id ', 'strength', 'hero_id', 'power_id')

    # add validation
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak']:
            raise ValueError('Strength must be either "Strong" or "Weak"')
        return strength


    def __repr__(self):
        return f'<HeroPower {self.id}>'

# class RestaurantPizza (db.Model, SerializerMixin):
#     __tablename__ = 'restaurant_pizzas'

#     id = db.Column(db.Integer, primary_key=True)
#     price = db.Column(db.Integer)
#     pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
#     restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

#     #add relationship
#     pizza = db.relationship('Pizaa', backref='restaurant_pizza')
#     restaurant = db.relationship('Restaurant', backref='restaurant_pizza')
#     #add serialization rules
#     serialize_only = ('id ', 'price', 'pizaa', 'restaurant', 'pizza_id', 'restaurant_id')
#     #add validation
#     @validates('price')
#     def validate_price(self, key, price):
#         if price < 1 or price > 30:
#             raise ValueError('Price must be between 1 and 30')
#         return price    

    # def __repr__(self):
    #     return f'<RestaurantPizza {self.id}>'