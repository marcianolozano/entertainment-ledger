from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Make sure the instance folder exists
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

# SQLite database file stored in the instance folder (Render compatible)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/ledger.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    balance = sum(t.amount for t in transactions)
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    amount = float(request.form['amount'])
    date = request.form['date']
    new_transaction = Transaction(description=description, amount=amount, date=date)
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
