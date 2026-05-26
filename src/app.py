"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text
from utils import APIException
from admin import setup_admin
from models import db, Favorite, People, Planet, User, Vehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

CURRENT_USER_ID = 1


PEOPLE_SEED = [
    {"id": 1, "name": "Luke Skywalker", "gender": "male", "height": "172", "eye_color": "blue", "hair_color": "blond", "birth_year": "19BBY"},
    {"id": 2, "name": "C-3PO", "gender": "n/a", "height": "167", "eye_color": "yellow", "hair_color": "n/a", "birth_year": "112BBY"},
    {"id": 3, "name": "R2-D2", "gender": "n/a", "height": "96", "eye_color": "red", "hair_color": "n/a", "birth_year": "33BBY"},
    {"id": 4, "name": "Darth Vader", "gender": "male", "height": "202", "eye_color": "yellow", "hair_color": "none", "birth_year": "41.9BBY"},
    {"id": 5, "name": "Leia Organa", "gender": "female", "height": "150", "eye_color": "brown", "hair_color": "brown", "birth_year": "19BBY"},
    {"id": 6, "name": "Owen Lars", "gender": "male", "height": "178", "eye_color": "blue", "hair_color": "brown, grey", "birth_year": "52BBY"},
    {"id": 7, "name": "Beru Whitesun Lars", "gender": "female", "height": "165", "eye_color": "blue", "hair_color": "brown", "birth_year": "47BBY"},
    {"id": 8, "name": "R5-D4", "gender": "n/a", "height": "97", "eye_color": "red", "hair_color": "n/a", "birth_year": "unknown"},
    {"id": 9, "name": "Biggs Darklighter", "gender": "male", "height": "183", "eye_color": "brown", "hair_color": "black", "birth_year": "24BBY"},
    {"id": 10, "name": "Obi-Wan Kenobi", "gender": "male", "height": "182", "eye_color": "blue-gray", "hair_color": "auburn, white", "birth_year": "57BBY"}
]

PLANET_SEED = [
    {"id": 1, "name": "Tatooine", "population": "200000", "climate": "arid", "terrain": "desert", "diameter": "10465"},
    {"id": 2, "name": "Alderaan", "population": "2000000000", "climate": "temperate", "terrain": "grasslands, mountains", "diameter": "12500"},
    {"id": 3, "name": "Yavin IV", "population": "1000", "climate": "temperate, tropical", "terrain": "jungle, rainforests", "diameter": "10200"},
    {"id": 4, "name": "Hoth", "population": "unknown", "climate": "frozen", "terrain": "tundra, ice caves, mountain ranges", "diameter": "7200"},
    {"id": 5, "name": "Dagobah", "population": "unknown", "climate": "murky", "terrain": "swamp, jungles", "diameter": "8900"},
    {"id": 6, "name": "Bespin", "population": "6000000", "climate": "temperate", "terrain": "gas giant", "diameter": "118000"},
    {"id": 7, "name": "Endor", "population": "30000000", "climate": "temperate", "terrain": "forests, mountains, lakes", "diameter": "4900"},
    {"id": 8, "name": "Naboo", "population": "4500000000", "climate": "temperate", "terrain": "grassy hills, swamps, forests, mountains", "diameter": "12120"},
    {"id": 9, "name": "Coruscant", "population": "1000000000000", "climate": "temperate", "terrain": "cityscape, mountains", "diameter": "12240"},
    {"id": 10, "name": "Kamino", "population": "1000000000", "climate": "temperate", "terrain": "ocean", "diameter": "19720"}
]

VEHICLE_SEED = [
    {"id": 4, "name": "Sand Crawler", "model": "Digger Crawler", "manufacturer": "Corellia Mining Corporation", "vehicle_class": "wheeled", "crew": "46", "passengers": "30"},
    {"id": 6, "name": "T-16 skyhopper", "model": "T-16 skyhopper", "manufacturer": "Incom Corporation", "vehicle_class": "repulsorcraft", "crew": "1", "passengers": "1"},
    {"id": 7, "name": "X-34 landspeeder", "model": "X-34 landspeeder", "manufacturer": "SoroSuub Corporation", "vehicle_class": "repulsorcraft", "crew": "1", "passengers": "1"},
    {"id": 8, "name": "TIE/LN starfighter", "model": "Twin Ion Engine/Ln Starfighter", "manufacturer": "Sienar Fleet Systems", "vehicle_class": "starfighter", "crew": "1", "passengers": "0"},
    {"id": 14, "name": "Snowspeeder", "model": "t-47 airspeeder", "manufacturer": "Incom Corporation", "vehicle_class": "airspeeder", "crew": "2", "passengers": "0"},
    {"id": 16, "name": "TIE bomber", "model": "TIE/sa bomber", "manufacturer": "Sienar Fleet Systems", "vehicle_class": "space/planetary bomber", "crew": "1", "passengers": "0"},
    {"id": 18, "name": "AT-AT", "model": "All Terrain Armored Transport", "manufacturer": "Kuat Drive Yards, Imperial Department of Military Research", "vehicle_class": "assault walker", "crew": "5", "passengers": "40"},
    {"id": 19, "name": "AT-ST", "model": "All Terrain Scout Transport", "manufacturer": "Kuat Drive Yards, Imperial Department of Military Research", "vehicle_class": "walker", "crew": "2", "passengers": "0"},
    {"id": 20, "name": "Storm IV Twin-Pod cloud car", "model": "Storm IV Twin-Pod", "manufacturer": "Bespin Motors", "vehicle_class": "repulsorcraft", "crew": "2", "passengers": "0"},
    {"id": 24, "name": "Sail barge", "model": "Modified Luxury Sail Barge", "manufacturer": "Ubrikkian Industries Custom Vehicle Division", "vehicle_class": "sail barge", "crew": "26", "passengers": "500"}
]

def reset_postgres_sequences():
    if db.engine.dialect.name != "postgresql":
        return

    for table_name in ["user", "people", "planet", "vehicle"]:
        quoted_table = f'"{table_name}"'
        db.session.execute(
            text(
                f"SELECT setval("
                f"pg_get_serial_sequence('{quoted_table}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {quoted_table}), 1), "
                f"true"
                f")"
            )
        )


def seed_database():
    user = db.session.get(User, CURRENT_USER_ID)
    if user is None:
        user = User(
            id=CURRENT_USER_ID,
            email="luke@rebellion.test",
            password="secret",
            first_name="Luke",
            last_name="Skywalker",
            is_active=True
        )
        db.session.add(user)

    for data in PEOPLE_SEED:
        person = db.session.get(People, data["id"])
        if person is None:
            db.session.add(People(**data))
        else:
            for key, value in data.items():
                setattr(person, key, value)

    for data in PLANET_SEED:
        planet = db.session.get(Planet, data["id"])
        if planet is None:
            db.session.add(Planet(**data))
        else:
            for key, value in data.items():
                setattr(planet, key, value)

    for data in VEHICLE_SEED:
        vehicle = db.session.get(Vehicle, data["id"])
        if vehicle is None:
            db.session.add(Vehicle(**data))
        else:
            for key, value in data.items():
                setattr(vehicle, key, value)

    db.session.commit()
    reset_postgres_sequences()
    db.session.commit()


def get_current_user():
    return db.session.get(User, CURRENT_USER_ID)


def favorite_exists(**filters):
    return Favorite.query.filter_by(user_id=CURRENT_USER_ID, **filters).first()


def get_json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, ({"message": "Request body must be valid JSON"}, 400)

    return data, None


def get_required_payload(required_fields):
    data, error = get_json_body()
    if error:
        return None, error

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return None, ({"message": "Missing required fields", "fields": missing_fields}, 400)

    return data, None


def update_model_fields(instance, data, fields):
    for field in fields:
        if field in data:
            setattr(instance, field, data[field])


PEOPLE_FIELDS = ["name", "gender", "height", "eye_color", "hair_color", "birth_year"]
PLANET_FIELDS = ["name", "population", "climate", "terrain", "diameter"]
VEHICLE_FIELDS = [
    "name",
    "model",
    "manufacturer",
    "vehicle_class",
    "crew",
    "passengers"
]


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def api_home():
    return jsonify({
        "message": "StarWars Blog API",
        "resources": {
            "people": "/people",
            "planets": "/planets",
            "vehicles": "/vehicles",
            "users": "/users",
            "favorites": "/users/favorites"
        }
    }), 200


@app.route('/people', methods=['GET'])
def get_people():
    return jsonify([person.serialize() for person in People.query.order_by(People.id).all()]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = db.session.get(People, people_id)
    if person is None:
        return jsonify({"message": "Person not found"}), 404

    return jsonify(person.serialize()), 200


@app.route('/people', methods=['POST'])
def create_person():
    data, error = get_required_payload(PEOPLE_FIELDS)
    if error:
        return jsonify(error[0]), error[1]

    person = People()
    update_model_fields(person, data, PEOPLE_FIELDS)
    db.session.add(person)
    db.session.commit()

    return jsonify(person.serialize()), 201


@app.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    person = db.session.get(People, people_id)
    if person is None:
        return jsonify({"message": "Person not found"}), 404

    data, error = get_json_body()
    if error:
        return jsonify(error[0]), error[1]

    update_model_fields(person, data, PEOPLE_FIELDS)
    db.session.commit()

    return jsonify(person.serialize()), 200


@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = db.session.get(People, people_id)
    if person is None:
        return jsonify({"message": "Person not found"}), 404

    Favorite.query.filter_by(people_id=people_id).delete()
    db.session.delete(person)
    db.session.commit()

    return jsonify({"message": "Person deleted"}), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    return jsonify([planet.serialize() for planet in Planet.query.order_by(Planet.id).all()]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = db.session.get(Planet, planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404

    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    data, error = get_required_payload(PLANET_FIELDS)
    if error:
        return jsonify(error[0]), error[1]

    planet = Planet()
    update_model_fields(planet, data, PLANET_FIELDS)
    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.serialize()), 201


@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = db.session.get(Planet, planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404

    data, error = get_json_body()
    if error:
        return jsonify(error[0]), error[1]

    update_model_fields(planet, data, PLANET_FIELDS)
    db.session.commit()

    return jsonify(planet.serialize()), 200


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = db.session.get(Planet, planet_id)
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404

    Favorite.query.filter_by(planet_id=planet_id).delete()
    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": "Planet deleted"}), 200


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify([vehicle.serialize() for vehicle in Vehicle.query.order_by(Vehicle.id).all()]), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle is None:
        return jsonify({"message": "Vehicle not found"}), 404

    return jsonify(vehicle.serialize()), 200


@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data, error = get_required_payload(VEHICLE_FIELDS)
    if error:
        return jsonify(error[0]), error[1]

    vehicle = Vehicle()
    update_model_fields(vehicle, data, VEHICLE_FIELDS)
    db.session.add(vehicle)
    db.session.commit()

    return jsonify(vehicle.serialize()), 201


@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle is None:
        return jsonify({"message": "Vehicle not found"}), 404

    data, error = get_json_body()
    if error:
        return jsonify(error[0]), error[1]

    update_model_fields(vehicle, data, VEHICLE_FIELDS)
    db.session.commit()

    return jsonify(vehicle.serialize()), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle is None:
        return jsonify({"message": "Vehicle not found"}), 404

    Favorite.query.filter_by(vehicle_id=vehicle_id).delete()
    db.session.delete(vehicle)
    db.session.commit()

    return jsonify({"message": "Vehicle deleted"}), 200


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify([user.serialize() for user in User.query.order_by(User.id).all()]), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = get_current_user()
    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify([favorite.serialize() for favorite in user.favorites]), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = get_current_user()
    planet = db.session.get(Planet, planet_id)

    if user is None or planet is None:
        return jsonify({"message": "User or planet not found"}), 404

    if favorite_exists(planet_id=planet_id):
        return jsonify({"message": "Planet is already in favorites"}), 400

    favorite = Favorite(user_id=CURRENT_USER_ID, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user = get_current_user()
    person = db.session.get(People, people_id)

    if user is None or person is None:
        return jsonify({"message": "User or person not found"}), 404

    if favorite_exists(people_id=people_id):
        return jsonify({"message": "Person is already in favorites"}), 400

    favorite = Favorite(user_id=CURRENT_USER_ID, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user = get_current_user()
    vehicle = db.session.get(Vehicle, vehicle_id)

    if user is None or vehicle is None:
        return jsonify({"message": "User or vehicle not found"}), 404

    if favorite_exists(vehicle_id=vehicle_id):
        return jsonify({"message": "Vehicle is already in favorites"}), 400

    favorite = Favorite(user_id=CURRENT_USER_ID, vehicle_id=vehicle_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite = favorite_exists(planet_id=planet_id)
    if favorite is None:
        return jsonify({"message": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite = favorite_exists(people_id=people_id)
    if favorite is None:
        return jsonify({"message": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed"}), 200


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    favorite = favorite_exists(vehicle_id=vehicle_id)
    if favorite is None:
        return jsonify({"message": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed"}), 200


@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.cli.command("seed")
def seed_command():
    """Seed the database with sample Star Wars data."""
    db.create_all()
    seed_database()
    print("Database seeded with Star Wars sample data.")


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
