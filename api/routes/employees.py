from flask import Blueprint, jsonify
from controllers.employee import EmployeeController
from decorators.token import tokenRequired
from config.config import Role
from flask_pydantic import validate
from schemas.employee import EmployeeCreate, EmployeeSearch, EmployeeUpdate
employeeRoute = Blueprint('employee', __name__)

@employeeRoute.route('/employee/<id>', methods=['GET'])
@tokenRequired(Role.ADMIN, Role.USER)
@validate()
def getEmployee(id: int):
    try:
        return EmployeeController().getEmployee(id)
    except Exception:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened'})

@employeeRoute.route('/employees', methods=['GET'])
@tokenRequired(Role.ADMIN, Role.USER)
@validate()
def searchEmployees(body: EmployeeSearch):
    try:
        return EmployeeController().searchEmployees(body)
    except Exception:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened'}), 500

@employeeRoute.route('/employee', methods=['POST'])
@tokenRequired(Role.ADMIN)
@validate()
def createEmployee(body: EmployeeCreate):
    try:
        return EmployeeController().createEmployee(body)
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened', 'error': str(e)}), 500

@employeeRoute.route('/employee/<id>', methods=['PUT'])
@tokenRequired(Role.ADMIN)
@validate()
def updateEmployee(id: int, body: EmployeeUpdate):
    try:
        return EmployeeController().updateEmployee(id, body)
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened', 'test': str(e)}), 500
    
@employeeRoute.route('/employee/<id>', methods=['DELETE'])
@tokenRequired(Role.ADMIN)
@validate()
def deleteEmployee(id: int):
    try:
        return EmployeeController().deleteEmployee(id)
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened'}), 500