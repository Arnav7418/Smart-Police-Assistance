from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    port="3300",  # Specify the port here
    user="root",
    password="1234",
    database="name"
)

# Define a route to render the help page with editable status
@app.route('/')
def index():
    try:
        # Query the database to fetch data
        cursor = db_connection.cursor()
        query = "SELECT * FROM distress_signals"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        # Render the template and pass the fetched data
        return render_template('help.html', data=data)

    except Exception as e:
        return str(e)


# Route to update the status in the database
@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        # Get the form data
        case_id = request.form['case_id']
        new_status = request.form['new_status']

        # Update the status in the database
        cursor = db_connection.cursor()
        query = "UPDATE distress_signals SET status = %s WHERE id = %s"
        cursor.execute(query, (new_status, case_id))
        db_connection.commit()
        cursor.close()

        # Redirect to the index page after updating the status
        return redirect('/')

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
