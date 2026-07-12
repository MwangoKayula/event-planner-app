from flask import Flask, render_template, request, redirect, url_for, jsonify
from .database import init_db, get_connection

app = Flask(__name__)
init_db()

EVENTS_PER_PAGE = 5


@app.route("/")
def index():
    search = request.args.get("search", "")
    page = int(request.args.get("page", 1))
    offset = (page - 1) * EVENTS_PER_PAGE

    conn = get_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT id, title, date, location FROM events WHERE title LIKE ? LIMIT ? OFFSET ?",
            (f"%{search}%", EVENTS_PER_PAGE, offset)
        )
    else:
        cursor.execute(
            "SELECT id, title, date, location FROM events LIMIT ? OFFSET ?",
            (EVENTS_PER_PAGE, offset)
        )

    events = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]
    total_pages = (total_events // EVENTS_PER_PAGE) + (1 if total_events % EVENTS_PER_PAGE > 0 else 0)

    conn.close()

    return render_template("index.html",
                           events=events,
                           page=page,
                           total_pages=total_pages,
                           search=search)

# -----------------------
# CREATE
# -----------------------
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

# -----------------------
# UPDATE
# -----------------------
@app.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute(
            "UPDATE events SET title=?, date=?, location=? WHERE id=?",
            (request.form["title"], request.form["date"], request.form["location"], event_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    cursor.execute("SELECT id, title, date, location FROM events WHERE id=?", (event_id,))
    event = cursor.fetchone()
    conn.close()

    return render_template("edit_event.html", event=event)

# -----------------------
# DELETE
# -----------------------
@app.route("/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# -----------------------
# API (Clean Separation)
# -----------------------
@app.route("/api/events", methods=["GET"])
def api_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, date, location FROM events")
    rows = cursor.fetchall()
    conn.close()

    events = [
        {"id": r[0], "title": r[1], "date": r[2], "location": r[3]}
        for r in rows
    ]
    return jsonify(events)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
