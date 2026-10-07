from flask import Flask, request, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL,
            marks REAL NOT NULL,
            contact TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADD STUDENT ----------------

@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()

    name = data.get("name", "").strip()
    roll_no = data.get("roll_no", "").strip()
    class_name = data.get("class_name", "").strip()
    marks = data.get("marks")
    contact = data.get("contact", "").strip()

    # Validation
    if not name or not roll_no or not class_name or marks is None or not contact:
        return jsonify({"error": "All fields are required"}), 400

    try:
        marks = float(marks)

        if marks < 0 or marks > 100:
            return jsonify({"error": "Marks must be between 0 and 100"}), 400

    except ValueError:
        return jsonify({"error": "Marks must be a number"}), 400

    if not re.fullmatch(r"[0-9]{10}", contact):
        return jsonify({"error": "Contact must contain 10 digits"}), 400

    conn = get_db()

    try:
        conn.execute("""
            INSERT INTO students
            (name, roll_no, class_name, marks, contact)
            VALUES (?, ?, ?, ?, ?)
        """, (name, roll_no, class_name, marks, contact))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Roll number already exists"}), 400

    conn.close()

    return jsonify({"message": "Student added successfully"}), 201


# ---------------- VIEW ALL STUDENTS ----------------

@app.route("/students", methods=["GET"])
def get_students():

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ---------------- SEARCH STUDENT ----------------

@app.route("/students/search", methods=["GET"])
def search_student():

    name = request.args.get("name", "").strip()
    roll_no = request.args.get("roll_no", "").strip()

    conn = get_db()

    if roll_no:
        students = conn.execute(
            "SELECT * FROM students WHERE roll_no = ?",
            (roll_no,)
        ).fetchall()

    elif name:
        students = conn.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ("%" + name + "%",)
        ).fetchall()

    else:
        students = conn.execute(
            "SELECT * FROM students"
        ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ---------------- UPDATE STUDENT ----------------

@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json()

    name = data.get("name", "").strip()
    roll_no = data.get("roll_no", "").strip()
    class_name = data.get("class_name", "").strip()
    marks = data.get("marks")
    contact = data.get("contact", "").strip()

    if not name or not roll_no or not class_name or marks is None or not contact:
        return jsonify({"error": "All fields are required"}), 400

    try:
        marks = float(marks)

        if marks < 0 or marks > 100:
            return jsonify({"error": "Marks must be between 0 and 100"}), 400

    except ValueError:
        return jsonify({"error": "Marks must be a number"}), 400

    if not re.fullmatch(r"[0-9]{10}", contact):
        return jsonify({"error": "Contact must contain 10 digits"}), 400

    conn = get_db()

    try:
        cursor = conn.execute("""
            UPDATE students
            SET name = ?,
                roll_no = ?,
                class_name = ?,
                marks = ?,
                contact = ?
            WHERE id = ?
        """, (name, roll_no, class_name, marks, contact, id))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Roll number already exists"}), 400

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.close()

    return jsonify({"message": "Student updated successfully"})


# ---------------- DELETE STUDENT ----------------

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.close()

    return jsonify({"message": "Student deleted successfully"})


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)