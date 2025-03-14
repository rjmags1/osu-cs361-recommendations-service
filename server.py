from decimal import Decimal
from flask import Flask, jsonify, request, abort
import psycopg2
from faker import Faker

app = Flask(__name__)

# Database connection details
DB_CONFIG = {
    "dbname": "cs361-project",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": 5432
}

def get_posts():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, content, latitude, longitude, createdat, views FROM posts;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": row[0], "title": row[1], "content": row[3], "author": row[2], "latitude": row[4], "longitude": row[5], "createdat": row[6], "views": row[7]} for row in rows]

def get_recommended_posts(lat, long):
    posts = get_posts()
    recommended_order = sorted(posts, key=lambda p: abs(p["latitude"] - lat) + abs(p["longitude"] - long))
    return recommended_order

@app.route("/posts", methods=["GET"])
def posts():
    lat = request.args.get('lat')
    long = request.args.get('long')
    is_coord = lambda s: s.replace(".", "", 1).replace("-", "", 1).isdigit()
    if lat is None or long is None or not is_coord(lat) or not is_coord(long):
        abort(400, description="lat and long query string params invalid or not specified in query string")
    return jsonify(get_recommended_posts(Decimal(lat), Decimal(long)))

if __name__ == "__main__":
    app.run(debug=True, port=4003)
