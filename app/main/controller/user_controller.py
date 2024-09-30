from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, add_wallet_balance, get_wallet_balance
from app.main.util.decorator import token_required

api = UserDto.api
_user = UserDto.user


@api.route('')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @token_required
    @api.marshal_with(_user)
    def get(self, id):
        """get a user given its identifier"""
        user = get_a_user(id)
        if not user:
            api.abort(404)
        else:
            return user

@api.route('/wallet_balance')
@api.response(201, "Wallet balance successfully updated")
class UserWalletBalance(Resource):
    @api.doc('get user wallet balance')
    @token_required
    def get(self):
        token = request.headers.get("Authorization")
        return get_wallet_balance(token)

    @api.doc('add wallet balance')
    @token_required
    @api.response(201, "wallet balance added successfully")
    def post(self):
        """Add user's wallet balance"""
        token = request.headers.get("Authorization")
        data = request.json
        return add_wallet_balance(data, token)