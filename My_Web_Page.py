from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"

# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="flaskdb",
    user="postgres",
    password="postgres"
)

# Home Route
@app.route('/')
def home():
    return redirect('/login')


# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        cur = conn.cursor()

        try:
            cur.execute(
                """
                INSERT INTO users(username,email,password)
                VALUES(%s,%s,%s)
                """,
                (username, email, hashed_password)
            )

            conn.commit()
            flash("Signup successful. Please Login.")
            return redirect('/login')

        except Exception as e:
            conn.rollback()
            flash("User already exists")

        finally:
            cur.close()

    return render_template('signup2.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = conn.cursor()

        cur.execute(
            "SELECT password FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[0], password):
            flash("Login Successful")
            return "Welcome User"

        flash("Invalid Email or Password")

    return render_template('login2.html')


if __name__ == '__main__':
    app.run(debug=True)