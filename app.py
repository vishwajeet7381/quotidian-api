import sqlite3

from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__)


# Function to create a connection to the SQLite database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("quotes.db")
    return g.db


# Close the database connection at the end of the request
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "db"):
        g.db.close()


# Database schema setup
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY,
                author TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        db.commit()


# Initialize the database schema
init_db()


# Get a random quote of the day
@app.route("/quote-of-the-day", methods=["GET"])
def get_quote_of_the_day():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
    quote = cursor.fetchone()
    if quote:
        return jsonify({"id": quote[0], "author": quote[1], "content": quote[2]})
    else:
        return jsonify({"message": "No quotes available"})


# Serve the HTML form for adding a quote
@app.route("/add-quote", methods=["GET"])
def add_quote_form():
    return render_template("add_quote.html")


# Get all quotes or add a new quote
@app.route("/quotes", methods=["GET", "POST"])
def manage_quotes():
    if request.method == "GET":
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM quotes")
        quotes = cursor.fetchall()
        quotes_list = [
            {"id": row[0], "author": row[1], "content": row[2]} for row in quotes
        ]
        return jsonify(quotes_list)
    elif request.method == "POST":
        data = request.get_json()
        if "author" in data and "content" in data:
            author = data["author"]
            content = data["content"]
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO quotes (author, content) VALUES (?, ?)", (author, content)
            )
            db.commit()
            return jsonify({"message": "Quote added successfully"})
        else:
            return jsonify({"error": "Author and content are required fields"}, 400)


# Update or delete a specific quote
@app.route("/quotes/<int:quote_id>", methods=["GET", "PUT", "DELETE"])
def update_or_delete_quote(quote_id):
    if request.method == "GET":
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
        quote = cursor.fetchone()
        if quote:
            return jsonify({"id": quote[0], "author": quote[1], "content": quote[2]})
        else:
            return jsonify({"message": "Quote not found"}, 404)
    elif request.method == "PUT":
        data = request.get_json()
        if "author" in data and "content" in data:
            author = data["author"]
            content = data["content"]
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE quotes SET author = ?, content = ? WHERE id = ?",
                (author, content, quote_id),
            )
            db.commit()
            return jsonify({"message": "Quote updated successfully"})
        else:
            return jsonify({"error": "Author and content are required fields"}, 400)
    elif request.method == "DELETE":
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
        db.commit()
        return jsonify({"message": "Quote deleted successfully"})


# Search quotes by author
@app.route("/quotes/search", methods=["GET"])
def search_quotes_by_author():
    author_name = request.args.get("author")
    if author_name:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM quotes WHERE author = ?", (author_name,))
        quotes = cursor.fetchall()
        if quotes:
            quotes_list = [
                {"id": row[0], "author": row[1], "content": row[2]} for row in quotes
            ]
            return jsonify(quotes_list)
        else:
            return jsonify({"message": "No quotes found for the author"})
    else:
        return jsonify({"error": "Author parameter is required"}, 400)


if __name__ == "__main__":
    app.run(debug=True)
