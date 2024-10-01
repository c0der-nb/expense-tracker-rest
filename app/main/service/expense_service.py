from app.main import db
from app.main.model.expense import Expense
from app.main.model.user import User

def create_new_expense(auth_token, data):
    try:
        auth_token = auth_token.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            new_expense = Expense(
                user_id = resp,
                title = data['title'],
                price = data['price'],
                category = data['category'],
                date = data['date']
            )
            new_wallet_balance = user.wallet_balance - data['price']
            if new_wallet_balance < 0:
                new_wallet_balance = 0
            user.wallet_balance = new_wallet_balance
            db.session.add(new_expense)
            db.session.commit()
            response_object = {
                'id': new_expense.id,
                'title': new_expense.title,
                'price': new_expense.price,
                'category': new_expense.category,
                'date': str(new_expense.date)
            }
            return response_object, 201
        response_object = {
            'status': 'fail',
            'message': resp
        }
        return response_object, 401
    except Exception as ex:
        response_object = {
            'status': 'fail',
            'message': 'Something went wrong. Please try again later.',
            'error': str(ex)
        }
        return response_object, 500

def get_all_expenses(auth_token):
    try:
        auth_token = auth_token.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        return Expense.query.filter_by(user_id=resp).all()
    except Exception as ex:
        response_object = {
            'status': 'fail',
            'message': 'Something went wrong. Please try again later.',
            'error': str(ex)
        }
        return response_object, 500
    
def get_expense_by_id(expense_id, auth_token):
    try:
        auth_token = auth_token.split(" ")[1]
        user_subject = User.decode_auth_token(auth_token)
        expense = Expense.query.filter_by(id=expense_id, user_id=user_subject).first()
        return expense
    except Exception as ex:
        response_object = {
            'status': 'fail',
            'message': 'Something went wrong. Please try again later.',
            'error': str(ex)
        }
        return response_object, 500
    
def update_expense(expense_id, data, auth_token):
    try:
        expense = get_expense_by_id(expense_id, auth_token)
        auth_token = auth_token.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if expense:
            user = User.query.filter_by(id=resp).first()
            expense.title = data['title']
            expense.price = data['price']
            expense.category = data['category']
            expense.date = data['date']
            new_wallet_balance = user.wallet_balance - data['price']
            if new_wallet_balance < 0:
                new_wallet_balance = 0
            user.wallet_balance = new_wallet_balance
            db.session.commit()
            response_obj = {
                'status': 'success',
                'message': 'Expense successfully updated.'
            }
            return response_obj, 200
        response_obj = {
            'status': 'fail',
            'message': "Expense doesn't exists."
        }
        return response_obj, 404

    except Exception as ex:
        response_obj = {
            'status': 'fail',
            'message': 'Something went wrong. please try again later',
            'error': str(ex)
        }
        return response_obj, 500
    
def delete_expense(expense_id, auth_token):
    try:
        expense = get_expense_by_id(expense_id, auth_token)
        if expense:
            db.session.delete(expense)
            db.session.commit()
            response_obj = {
                'status': 'success',
                'message': 'Expense successfully deleted'
            }
            return response_obj, 200
        response_obj = {
            'status': 'fail',
            'message': 'Expense not found'
        }
        return response_obj, 404
        
    except Exception as ex:
        response_obj = {
            'status': 'fail',
            'message': 'Something went wrong. please try again later',
            'error': str(ex)
        }
        return response_obj, 500