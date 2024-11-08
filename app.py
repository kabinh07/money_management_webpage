from flask import Flask, request, jsonify
from models import db, User, Income, Investment, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_manager.db'
db.init_app(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/add_income', methods=['POST'])
def add_income():
    data = request.json
    new_income = Income(user_id=data['user_id'], amount=data['amount'], date=data['date'])
    db.session.add(new_income)
    db.session.commit()
    return jsonify({'message': 'Income added successfully'})

@app.route('/add_investment', methods=['POST'])
def add_investment():
    data = request.json
    new_investment = Investment(user_id=data['user_id'], name=data['name'], amount=data['amount'], status=data['status'])
    db.session.add(new_investment)
    db.session.commit()
    return jsonify({'message': 'Investment added successfully'})

@app.route('/remaining_balance/<int:user_id>', methods=['GET'])
def get_remaining_balance(user_id):
    # Calculate remaining balance based on incomes and investments
    total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0
    total_investment = db.session.query(db.func.sum(Investment.amount)).filter_by(user_id=user_id).scalar() or 0
    remaining_balance = total_income - total_investment
    return jsonify({'remaining_balance': remaining_balance})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
