import os
import re
import logging
from flask import Flask, render_template, request, g, redirect, url_for, flash
from flask_mail import Mail, Message
import sqlite3
import secrets

# Generate a random secret key
secret_key = secrets.token_hex(16)  # 16 bytes (128 bits) is a common choice
print(secret_key)

app = Flask(__name__)
app.secret_key = secret_key
# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sphesihlekheswa44@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mnguni44@'
app.config['MAIL_DEFAULT_SENDER'] = 'sphesihlekheswa44@gmail.com'

mail = Mail(app)
# Set up logging


# Define the path to the SQLite database
DATABASE = os.path.join(app.root_path, 'data', 'kanye.db')

# Function to get the SQLite database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Teardown function to close the database connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route to display the home page
@app.route('/', methods=['GET'])
def show_home():
    return render_template('index.html')

# Route to process the contact form submission
# Route to process the contact form submission
@app.route('/quote', methods=['POST'])
def process_contact_form():
    try:
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        service = request.form['service']
        details = request.form['details']

        # Get database connection
        db = get_db()
        c = db.cursor()

        # Insert form data into the contacts table
        c.execute("INSERT INTO contacts (name, email, phone, service, details) VALUES (?, ?, ?, ?, ?)",
                  (name, email, phone, service, details))

        # Commit changes
        db.commit()

        # Render the thank_you.html template
        return render_template('thank_you.html', service=service)

    except Exception as e:
        logging.exception("Error occurred while processing contact form submission:")
        flash("An error occurred. Please try again later.")
        return redirect(url_for('show_home'))

# Route to handle contact form submission
@app.route('/contact', methods=['POST'])
def handle_contact():
    try:
        # Get form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Get database connection
        db = get_db()
        c = db.cursor()

        # Insert form data into the messages table
        c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                  (name, email, message))

        # Commit changes
        db.commit()

        # Close the database connection
        db.close()

        # Redirect to a thank you page
        return render_template('thank_you.html')

    except Exception as e:
        logging.exception("Error occurred while processing contact form submission:")
        flash("An error occurred. Please try again later.")
        return redirect(url_for('show_home'))

# Route to display the pricing page
@app.route('/pricing', methods=['POST'])
def show_pricing():
    return render_template('pricing.html')

# Route to display the payment page
@app.route('/pric', methods=['GET'])
def show_payment():
    return render_template('payment.html')

# Route to process the payment form submission
@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        id_number = request.form['idNumber']
        card_number = request.form['cardNumber']
        expiration_month = request.form['expirationMonth']
        expiration_year = request.form['expirationYear']
        cvv = request.form['cvv']

        # Validate form data
        errors = []
        if not re.match(r"^\d{13}$", id_number):
            errors.append("ID Number must be 13 digits.")
        if not re.match(r"^\d{16}$", card_number.replace(" ", "")):
            errors.append("Card Number must be 16 digits.")
        if not (1 <= int(expiration_month) <= 12):
            errors.append("Invalid Expiration Month.")
        if int(expiration_year) < 2024:
            errors.append("Invalid Expiration Year.")
        if not re.match(r"^\d{3}$", cvv):
            errors.append("CVV must be 3 digits.")

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('show_payment'))

        # Get database connection
        db = get_db()
        c = db.cursor()

        # Insert payment data into the payments table
        c.execute("INSERT INTO payments (id_number, card_number, expiration_month, expiration_year, cvv) VALUES (?, ?, ?, ?, ?)",
                  (id_number, card_number, expiration_month, expiration_year, cvv))
        db.commit()

        # Close the database connection
        db.close()

        # Redirect to a thank you page
        return redirect(url_for('thank_you'))

    except Exception as e:
        logging.exception("Error occurred while processing payment form submission:")
        flash("An error occurred while processing your payment. Please try again.")
        return redirect(url_for('show_payment'))

# Route to display a thank you page
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
