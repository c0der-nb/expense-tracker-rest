import uuid
import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            name=data['name'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(user_id):
    return User.query.filter_by(id=user_id).first()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def add_wallet_balance(data, auth_token):
    try:
        auth_token = auth_token.split(" ")[1]
        user_subject = User.decode_auth_token(auth_token)
        user = User.query.filter_by(id=user_subject).first()
        if user:
            user.wallet_balance += data['wallet_balance']
            db.session.commit()
            response_obj = {
                'status': 'success',
                'message': 'wallet balance successfully updated'
            }
            return response_obj, 201
        response_obj = {
            'status': 'fail',
            'message': 'user not found'
        }
        return response_obj, 404
    except Exception as ex:
        response_obj = {
            'status': 'fail',
            'message': 'Something went wrong. Try again later',
            'error': str(ex)
        }
        return response_obj, 500


def save_changes(data):
    db.session.add(data)
    db.session.commit()