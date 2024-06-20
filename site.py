from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
@app.route('/')
def get_ip_geo():
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    webhook_url = 'https://discord.com/api/webhooks/1253309748820971570/ZHyckJA2tMno7aP6r4sn9HP-vjr5H4r4wnAsQdPixbkdXkSE61eLrhFYik33AMzL7y4j'
    
    
    message = f'Visitor IP: {visitor_ip}'

    
    payload = {'content': message}
    response = requests.post(webhook_url, json=payload)
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with app.app_context():
            user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password', 401

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with app.app_context():
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return 'Username already exists', 400

            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    # Add authentication logic here to restrict access to admin page
    return render_template('dashboard.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)