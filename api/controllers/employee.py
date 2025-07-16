from models.employee import Employee
from extensions import db
from flask import jsonify, current_app, request, g
from uuid import uuid4
import json

class EmployeeController:
    def getEmployee(self, id):
        employee = Employee.query.filter_by(id=id).first()

        if employee is None:
            return jsonify({'status': 'error', 'message': 'Employee not found'}), 404
        
        return jsonify({'status': 'success', 'employee': employee.serialize()})

    def searchEmployees(self, query):
        q = Employee.query

        if query.firstName is not None:
            q = q.filter(Employee.firstName.ilike(f"%{query.firstName}%"))

        if query.lastName is not None:
            q = q.filter(Employee.lastName.ilike(f"%{query.lastName}%"))

        if query.address is not None:
            q = q.filter(Employee.address.ilike(f"%{query.address}%"))

        if query.phone is not None:
            q = q.filter(Employee.phone.ilike(f"%{query.phone}%"))

        if query.minAge is not None:
            q = q.filter(Employee.age >= query.minAge)

        if query.maxAge is not None:
            q = q.filter(Employee.age <= query.maxAge)

        return jsonify({'status': 'success', 'total': q.count(), 'employees': list(map(lambda e: e.serialize(), q.all()))})

    def createEmployee(self, body):
        eventId = str(uuid4())

        employee = Employee(
            body.firstName,
            body.lastName,
            body.address,
            body.phone,
            body.age,
            body.hireDate,
            body.terminationDate
        )            

        db.session.add(employee)
        db.session.commit()
        db.session.refresh(employee)

        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
            "client.ip": request.remote_addr,
            "http.request.method": request.method,
            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
            "event.action": "CREATE_EMPLOYEE",
            "event.outcome": "success",
            "event.id": eventId,
            "event.original": json.dumps(body),
            "user.name": g.user.get('username'),
            "user.roles": [g.user.get('role')]
        })

        return jsonify({'status': 'success', 'message': 'Employee created', 'employee': employee.serialize()}), 201

    def updateEmployee(self, id, body):
        eventId = str(uuid4())
        employee = Employee.query.filter_by(id=id).first()

        if employee is None:
            current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                "client.ip": request.remote_addr,
                "http.request.method": request.method,
                "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                "event.action": "UPDATE_EMPLOYEE",
                "event.outcome": "failure",
                "event.reason": "Employee not found",
                "event.id": eventId,
                "event.original": json.dumps(body.serialize()),
                "user.name": g.user.get('username'),
                "user.roles": [g.user.get('role')],
                "client.user.id": id
            })
            return jsonify({'status': 'error', 'message': 'Employee not found'}), 404
        
        if body.firstName is not None:
            employee.firstName = body.firstName

        if body.lastName is not None:
            employee.lastName = body.lastName

        if body.address is not None:
            employee.address = body.address

        if body.phone is not None:
            employee.phone = body.phone

        if body.age is not None:
            employee.age = body.age

        if body.hireDate is not None:
            employee.hireDate = body.hireDate

        if body.terminationDate is not None:
            employee.terminationDate = body.terminationDate

        db.session.add(employee)
        db.session.commit()
        db.session.refresh(employee)

        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
            "client.ip": request.remote_addr,
            "http.request.method": request.method,
            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
            "event.action": "UPDATE_EMPLOYEE",
            "event.outcome": "success",
            "event.id": eventId,
            "event.original": json.dumps(body.serialize()),
            "user.name": g.user.get('username'),
            "user.roles": [g.user.get('role')],
            "client.user.id": id
        })
        return jsonify({'status': 'success', 'message': 'Employee updated', 'employee': employee.serialize()}), 200

    def deleteEmployee(self, id):
        eventId = str(uuid4())
        employee = Employee.query.filter_by(id=id).first()

        if employee is None:
            current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                "client.ip": request.remote_addr,
                "http.request.method": request.method,
                "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                "event.action": "DELETE_EMPLOYEE",
                "event.outcome": "failure",
                "event.reason": "Employee not found",
                "event.id": eventId,
                "user.name": g.user.get('username'),
                "user.roles": [g.user.get('role')],
                "client.user.id": id
            })
            return jsonify({'status': 'error', 'message': 'Employee not found'}), 404
        
        employeeDeleted = employee.serialize()

        db.session.delete(employee)
        db.session.commit()

        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
            "client.ip": request.remote_addr,
            "http.request.method": request.method,
            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
            "event.action": "DELETE_EMPLOYEE",
            "event.outcome": "success",
            "event.id": eventId,
            "user.name": g.user.get('username'),
            "user.roles": [g.user.get('role')],
            "client.user.id": id
        })

        return jsonify({'status': 'success', 'message': 'Employee deleted', 'employee': employeeDeleted}), 204