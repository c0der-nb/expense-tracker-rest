from flask import request
from flask_restx import Resource

from ..util.dto import ExpenseDto
from ..service.expense_service import create_new_expense, get_all_expenses, get_expense_by_id, update_expense, delete_expense
from app.main.util.decorator import token_required

api = ExpenseDto.api
_expense = ExpenseDto.expense

@api.route('/')
class ExpenseList(Resource):
    @api.doc('list all expenses')
    @token_required
    @api.marshal_list_with(_expense, envelope='data')
    def get(self):
        """List all expenses"""
        token = request.headers.get("Authorization")
        return get_all_expenses(token)
    
    @api.response(201, 'Expense successfully created.')
    @api.doc('create a new expense')
    @token_required
    @api.expect(_expense, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        token = request.headers.get("Authorization")
        return create_new_expense(auth_token=token,data=data)

@api.route('/<id>')
@api.param('id', 'The expense identifier')
@api.response(404, 'Expense not found')
class ExpenseRetrieveUpdateDelete(Resource):
    @api.doc('get expense by id')
    @token_required
    @api.marshal_with(_expense)
    def get(self, id):
        """Retrieves an expense by id"""
        token = request.headers.get("Authorization")
        return get_expense_by_id(id, token)

    @api.doc('update expense')
    @token_required
    @api.response('204', 'Expense successfully updated.')
    @api.expect(_expense, validate=True)
    def put(self, id):
        """Updates an expense"""
        token = request.headers.get("Authorization")
        data = request.json
        return update_expense(id, data, token)

    @api.doc('delete expense')
    @token_required
    @api.response('204', 'Expense successfully deleted.')
    def delete(self, id):
        """Deletes an expense"""
        token = request.headers.get("Authorization")
        return delete_expense(id, token)
