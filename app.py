from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import random
import string
import json
import os

app = Flask(__name__)
app.secret_key = "quiznova-secret-key"

DATABASE = "quiz.db"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            code TEXT UNIQUE NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def generate_code():
    conn = get_db()

    while True:
        code = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

        existing = conn.execute(
            "SELECT id FROM quizzes WHERE code = ?",
            (code,)
        ).fetchone()

        if not existing:
            conn.close()
            return code


# ---------------- HOME ----------------

@app.route("/")
def index():
    return render_template("index.html")


# ---------------- CREATE QUIZ ----------------

@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")

        questions_json = request.form.get("questions")

        if not title or not questions_json:
            flash("Please enter quiz details.")
            return redirect(url_for("create"))

        try:
            questions = json.loads(questions_json)
        except:
            flash("Invalid questions.")
            return redirect(url_for("create"))

        if len(questions) == 0:
            flash("Add at least one question.")
            return redirect(url_for("create"))

        code = generate_code()

        conn = get_db()

        cursor = conn.execute(
            """
            INSERT INTO quizzes (title, description, code)
            VALUES (?, ?, ?)
            """,
            (title, description, code)
        )

        quiz_id = cursor.lastrowid

        for q in questions:

            conn.execute(
                """
                INSERT INTO questions
                (quiz_id, question, option_a, option_b,
                 option_c, option_d, answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    quiz_id,
                    q["question"],
                    q["a"],
                    q["b"],
                    q["c"],
                    q["d"],
                    q["answer"]
                )
            )

        conn.commit()
        conn.close()

        return render_template(
            "create.html",
            success=True,
            code=code,
            title=title
        )

    return render_template("create.html")


# ---------------- JOIN ----------------

@app.route("/join", methods=["GET", "POST"])
def join():

    if request.method == "POST":

        name = request.form.get("student_name")
        code = request.form.get("code", "").upper().strip()

        if not name or not code:
            flash("Enter your name and quiz code.")
            return redirect(url_for("join"))

        conn = get_db()

        quiz = conn.execute(
            "SELECT * FROM quizzes WHERE code = ?",
            (code,)
        ).fetchone()

        conn.close()

        if not quiz:
            flash("Quiz code not found.")
            return redirect(url_for("join"))

        session["student_name"] = name

        return redirect(
            url_for("quiz", quiz_id=quiz["id"])
        )

    return render_template("join.html")


# ---------------- QUIZ ----------------

@app.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
def quiz(quiz_id):

    conn = get_db()

    quiz_data = conn.execute(
        "SELECT * FROM quizzes WHERE id = ?",
        (quiz_id,)
    ).fetchone()

    questions = conn.execute(
        "SELECT * FROM questions WHERE quiz_id = ?",
        (quiz_id,)
    ).fetchall()

    conn.close()

    if not quiz_data:
        return "Quiz not found", 404

    if "student_name" not in session:
        return redirect(url_for("join"))

    if request.method == "POST":

        score = 0

        for q in questions:

            selected = request.form.get(
                f"question_{q['id']}"
            )

            if selected == q["answer"]:
                score += 1

        student_name = session["student_name"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO results
            (quiz_id, student_name, score, total)
            VALUES (?, ?, ?, ?)
            """,
            (
                quiz_id,
                student_name,
                score,
                len(questions)
            )
        )

        conn.commit()
        conn.close()

        session["last_score"] = score
        session["last_total"] = len(questions)
        session["last_quiz_id"] = quiz_id

        return redirect(
            url_for("result")
        )

    return render_template(
        "quiz.html",
        quiz=quiz_data,
        questions=questions
    )


# ---------------- RESULT ----------------

@app.route("/result")
def result():

    score = session.get("last_score", 0)
    total = session.get("last_total", 0)
    quiz_id = session.get("last_quiz_id")

    percentage = 0

    if total:
        percentage = round(
            (score / total) * 100
        )

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        quiz_id=quiz_id
    )


# ---------------- LEADERBOARD ----------------

@app.route("/leaderboard/<int:quiz_id>")
def leaderboard(quiz_id):

    conn = get_db()

    quiz_data = conn.execute(
        "SELECT * FROM quizzes WHERE id = ?",
        (quiz_id,)
    ).fetchone()

    results = conn.execute(
        """
        SELECT *
        FROM results
        WHERE quiz_id = ?
        ORDER BY score DESC
        """,
        (quiz_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "leaderboard.html",
        quiz=quiz_data,
        results=results
    )


# ---------------- ALL QUIZZES ----------------

@app.route("/quizzes")
def quizzes():

    conn = get_db()

    data = conn.execute(
        "SELECT * FROM quizzes ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "leaderboard.html",
        quizzes=data
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ---------------- RUN ----------------

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))