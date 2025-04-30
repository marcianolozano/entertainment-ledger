from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

# Correct database path for Render compatibility
db_path = os.path.join(os.getcwd(), 'ledger.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.id} - {self.description}>'

@app.route('/')
def index():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    starting_balance = 600
    total = starting_balance - sum(t.amount for t in transactions)
    return render_template('index.html', transactions=transactions, total=total)

@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    amount = float(request.form['amount'])
    new_transaction = Transaction(description=description, amount=amount)
    db.session.add(new_transaction)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
