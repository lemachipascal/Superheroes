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
    serialize_only = ('id', 'name', 'super_name')

    def __repr__(self):
        return f'<Hero {self.name}>'




class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    hero_powers = db.relationship('HeroPower', back_populates='power')

    # add serialization rules   
    serialize_only = ('id', 'name', 'description')


    # add validation
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description

    def __repr__(self):
        return f'<Power {self.name}>'



class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # add relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    hero = relationship('Hero', back_populates='hero_power')
    power = relationship('Power', back_populates='hero_powers')

    # add serialization rules
    serialize_only = ('id', 'strength', 'hero_id', 'power_id')

    # add validation
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak']:
            raise ValueError('Strength must be either "Strong" or "Weak"')
        return strength


    def __repr__(self):
        return f'<HeroPower {self.id}>'

