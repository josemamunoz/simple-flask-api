from flask import Flask, request, jsonify
import pymysql
from pymysql import cursors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host='mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com',
            database='bsale_test', 
            user='bsale_test', 
            password='bsale_test')
    except pymysql.Error as e:
        print(e)
    return conn


@app.route('/')
def home():
    return "flask heroku app"

@app.route("/products", methods=["GET", "POST"])
def products():
    conn = db_connection()
    cursor = conn.cursor()
    productList = []
    print("function products")
    cursor.execute("SELECT * FROM product")
    products = [
        dict(
            id=row[0], 
            name=row[1],
            url_image =row[2],
            price =row[3],
            discount =row[4],
            category =row[5])
            for row in cursor.fetchall()
            ]
    
    for product in products:
        productList.append(product)

    return jsonify({"Products": productList})



@app.route("/categories", methods=["GET", "POST"])
def categories():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM category")
        categories = [
            dict(
                id=row[0], 
                name=row[1])
                for row in cursor.fetchall()
                ]
        if categories is not None:
            return jsonify({"categories ": categories})


if __name__ == "__main__":
    app.run()