from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'name': fields.String(required=True, description='user name'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        'wallet_balance': fields.String(description='user current wallet balance')
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class ExpenseDto:
    api = Namespace('expense', description="expense related operations")
    expense = api.model('expense', {
        'id': fields.Integer(description="expense identifier"),
        'title': fields.String(required=True, description="title of the expense"),
        'price': fields.Float(required=True, description="cost of the expense"),
        'category': fields.String(required=True, description="category of the expense"),
        'date': fields.Date(required=True, description="date at which the expense was made")
    })