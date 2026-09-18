from flask import Flask, render_template, request, redirect, jsonify
from database import get_connection, initialize_database

app = Flask(__name__)

initialize_database()


@app.route("/")
def home():
    connection = get_connection()

    restaurants = connection.execute(
        "SELECT * FROM restaurants"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        restaurants=restaurants
    )


@app.route("/restaurant/<int:restaurant_id>")
def restaurant_menu(restaurant_id):
    connection = get_connection()

    restaurant = connection.execute(
        "SELECT * FROM restaurants WHERE id = ?",
        (restaurant_id,)
    ).fetchone()

    menu_items = connection.execute(
        """
        SELECT * FROM menu_items
        WHERE restaurant_id = ?
        """,
        (restaurant_id,)
    ).fetchall()

    connection.close()

    return render_template(
        "menu.html",
        restaurant=restaurant,
        menu_items=menu_items
    )


@app.route("/api/restaurants")
def restaurants_api():
    connection = get_connection()

    restaurants = connection.execute(
        "SELECT * FROM restaurants"
    ).fetchall()

    connection.close()

    return jsonify([
        dict(restaurant)
        for restaurant in restaurants
    ])


@app.route("/admin/restaurant", methods=["POST"])
def add_restaurant():

    name = request.form["name"]
    location = request.form["location"]

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO restaurants (name, location)
        VALUES (?, ?)
        """,
        (name, location)
    )

    connection.commit()
    connection.close()

    return redirect("/")


@app.route("/admin/menu", methods=["POST"])
def add_menu_item():

    restaurant_id = request.form["restaurant_id"]
    name = request.form["name"]
    price = request.form["price"]

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO menu_items
        (restaurant_id, name, price)
        VALUES (?, ?, ?)
        """,
        (restaurant_id, name, price)
    )

    connection.commit()
    connection.close()

    return redirect(
        f"/restaurant/{restaurant_id}"
    )


if __name__ == "__main__":
    app.run(debug=True)
