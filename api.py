from flask import Flask, request, jsonify
import sqlite3
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("DevHorizon.db")

# Swagger UI setup
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Project Management API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route("/users", methods=["GET", "POST"])
def users():
    connection = connect_db()
    cursor = connection.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        connection.close()
        return jsonify(users)

    if request.method == "POST":
        data = request.json
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role_id, email, qualification_level) VALUES (?, ?, ?, ?, ?)",
                (data["username"], data["password"], data["role_id"], data.get("email"), data.get("qualification_level", 0))
            )
            connection.commit()
            connection.close()
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            connection.close()
            return jsonify({"error": str(e)}), 400

@app.route("/roles", methods=["GET"])
def roles():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    connection.close()
    return jsonify(roles)

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    connection = connect_db()
    cursor = connection.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        connection.close()
        return jsonify(tasks)

    if request.method == "POST":
        data = request.json
        try:
            cursor.execute(
                "INSERT INTO tasks (title, description, assigned_user_id, status, deadline) VALUES (?, ?, ?, ?, ?)",
                (data["title"], data.get("description"), data.get("assigned_user_id"), data.get("status", "новая"), data.get("deadline"))
            )
            connection.commit()
            connection.close()
            return jsonify({"message": "Task created successfully"}), 201
        except Exception as e:
            connection.close()
            return jsonify({"error": str(e)}), 400

@app.route("/qualifications", methods=["GET", "POST"])
def qualifications():
    connection = connect_db()
    cursor = connection.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM qualifications")
        qualifications = cursor.fetchall()
        connection.close()
        return jsonify(qualifications)

    if request.method == "POST":
        data = request.json
        try:
            cursor.execute(
                "INSERT INTO qualifications (user_id, points, evaluation_date) VALUES (?, ?, ?)",
                (data["user_id"], data["points"], data["evaluation_date"])
            )
            connection.commit()
            connection.close()
            return jsonify({"message": "Qualification added successfully"}), 201
        except Exception as e:
            connection.close()
            return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)