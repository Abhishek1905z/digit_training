from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configure PostgreSQL connection
conn = psycopg2.connect(
    host='localhost',
    dbname='your_db_name',
    user='your_db_user',
    password='your_db_password'
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials against the database
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        dbuser = cursor.fetchone()

        if dbuser:
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            dbpass = cursor.fetchone()[0]

            if dbpass == password:
                return "Login successful!"
            else:
                return "Incorrect password."
        else:
            return "Username not found."

    return render_template('login.html')  # Create an HTML template for login form

if __name__ == '__main__':
    app.run(debug=True)
