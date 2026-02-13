from flask import Flask, render_template, request, redirect, url_for
from .database import init_db, get_connection

app = Flask(__name__)
init_db()

# --------------------
# READ (Home Page)
# --------------------
@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, date, location FROM events")
    events = cursor.fetchall()
    conn.close()
    return render_template("index.html", events=events)

# --------------------
# CREATE
# --------------------
@app.route("/add", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        location = request.form["location"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (title, date, location) VALUES (?, ?, ?)",
            (title, date, location)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add_event.html")

# --------------------
# UPDATE
# --------------------
@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        location = request.form["location"]

        cursor.execute(
            "UPDATE events SET title=?, date=?, location=? WHERE id=?",
            (title, date, location, event_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    cursor.execute("SELECT id, title, date, location FROM events WHERE id=?", (event_id,))
    event = cursor.fetchone()
    conn.close()

    return render_template("edit_event.html", event=event)

# --------------------
# DELETE
# --------------------
@app.route("/delete/<int:event_id>")
def delete_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
