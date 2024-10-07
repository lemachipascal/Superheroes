#!/usr/bin/env python3

from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os
import logging


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    try:
       heroes = Hero.query.all()
       return jsonify([hero.to_dict() for hero in heroes]),200
    except Exception as e:
        app.logger.error(f"Error retrieving heroes:{e}")
        return jsonify({'error': 'An unexpected error occured'}), 500

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.to_dict()),200

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.to_dict())

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    
    data = request.get_json()

    if 'description' in data:
        try:  
           power.description = data['description']
           db.session.commit()
           return jsonify(power.to_dict()), 200
        except ValueError as e:
           return jsonify({'error':[str(e)]}), 400
        
    return jsonify({'errors': ['No description provided']}), 400
    
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
        return jsonify({'errors': ['validation errors']}), 400
    try:
        new_hero_power = HeroPower(**data)
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify(new_hero_power.to_dict()), 201
    except Exception as e:
        return jsonify({'errors': ['validation errors']}), 400
    
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"ERROR: {str(e)}")
    return jsonify({'error':'An unexpected error occured'}), 500