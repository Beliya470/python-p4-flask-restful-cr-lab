#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate  # Only importing Migrate, not MigrateCommand
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

db.init_app(app)
migrate = Migrate(app, db)  # Initializing migrate with app and db

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.serialize() for plant in plants])

    def post(self):
        data = request.get_json()
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.serialize())

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get_or_404(plant_id)
        return jsonify(plant.serialize())

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

if __name__ == '__main__':
    app.run(debug=True)  # Changed from manager.run() to app.run(debug=True)
