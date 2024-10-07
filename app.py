from flask import Flask, jsonify, request
import sqlite3
import requests

app = Flask(__name__)

def db_connection():
    conn = sqlite3.connect('database.db')
    return conn


@app.route('/')
def home():
    return jsonify({'status': 'Ok'}), 200
    return jsonify({'message': 'Olá, mundo!'})

if __name__ == "__main__":
app.run(debug=True)


def swapi_request(endpoint):
    try:
        response = requests.get(f'https://swapi.dev/api/{endpoint}')
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": str(err)}), 400


@app.route('/people', methods=['GET'])
def get_characters():
    data, status = swapi_request('people/')
    return jsonify(data), status


@app.route('/people/<int:id>', methods=['GET'])
def get_character(id):
    data, status = swapi_request(f'people/{id}/')
    return jsonify(data), status


@app.route('/people/<int:id>/save', methods=['POST'])
def save_character(id):
    conn = db_connection()
    cursor = conn.cursor()
    data, status = swapi_request(f'people/{id}/')

    if status == 200:
        cursor.execute(
            """INSERT INTO characters (name, birth_year) VALUES (?, ?)""",
            (data['name'], data['birth_year'])
        )
        conn.commit()
        return jsonify({"message": "Personagem salvo com sucesso!"}), 201
    else:
        return jsonify({"error": "Erro ao salvar personagem"}), status


@app.route('/people/<int:id>/delete', methods=['DELETE'])
def delete_character(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters WHERE id=?", (id,))
    conn.commit()
    return jsonify({"message": "Personagem deletado com sucesso!"}), 200


@app.route('/favorito/save', methods=['POST'])
def save_favorite():
    data = request.json
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO favoritos (character_name, movie_name, ship_name, vehicle_name, species_name, planet_name)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (data['character'], data['movie'], data['ship'], data['vehicle'], data['species'], data['planet'])
    )
    conn.commit()
    return jsonify({"message": "Favorito salvo com sucesso!"}), 201


@app.route('/getFavorito', methods=['GET'])
def get_favorite():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favoritos")
    data = cursor.fetchone()
    
    favorito = {
        "character": data[0],
        "movie": data[1],
        "ship": data[2],
        "vehicle": data[3],
        "species": data[4],
        "planet": data[5],
        "aluno1": "Anderson Richard",
        "matricula1": "12345",
        "curso": "Sistemas de Informação",
        "universidade": "Univás"
    }
    return jsonify(favorito), 200

@app.route('/favorito/save', methods=['POST'])
def save_favorite_route():
    conn = db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO favoritos (character, film, starship, vehicle, species, planet) VALUES (?, ?, ?, ?, ?, ?)""",
        ("Luke Skywalker", "A New Hope", "X-wing", "Speeder", "Human", "Tatooine")
    )
    conn.commit()
    return jsonify({"message": "Favorito salvo com sucesso!"}), 201


@app.route('/getFavorito', methods=['GET'])
def get_favorite():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favoritos")
    data = cursor.fetchone()
    
    favorito = {
        "character": data[0],
        "movie": data[1],
        "ship": data[2],
        "vehicle": data[3],
        "species": data[4],
        "planet": data[5],
        "aluno1": "Anderson Richard",
        "matricula1": "12345",
        "curso": "Sistemas de Informação",
        "universidade": "Univás"
    }
    return jsonify(favorito), 200