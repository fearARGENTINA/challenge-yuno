from models.user import User
from extensions import db
from flask import jsonify, current_app, request, g
import json

class UserController:
    def getUser(self, id):
        user = User.query.filter_by(id=id).first()

        if user is None:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        return jsonify({'status': 'success', 'user': user.serialize()})

    def searchUsers(self, query):
        q = User.query

        if query.username is None:
            return jsonify({'status': 'error', 'message': 'Must provide username field for searching'}), 400

        q = q.filter(User.username.ilike(f"%{query.username}%"))

        return jsonify({'status': 'success', 'total': q.count(), 'users': list(map(lambda u: u.serialize(), q.all()))})

    def createUser(self, body):
        eventId = str(uuid4())

        if not User.query.filter_by(username=body.username).first() is None:
            current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                "client.ip": request.remote_addr,
                "http.request.method": request.method,
                "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                "event.action": "CREATE_USER",
                "event.outcome": "failure",
                "event.reason": "User already exists",
                "event.id": eventId,
                "event.original": json.dumps(body),
                "user.name": g.user.get('username'),
                "user.roles": [g.user.get('role')]
            })
            return jsonify({'status': 'error', 'message': 'User already exists'}), 400

        user = User(
            username=body.username,
            role=body.role
        )            

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
            "client.ip": request.remote_addr,
            "http.request.method": request.method,
            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
            "event.action": "CREATE_USER",
            "event.outcome": "success",
            "event.id": eventId,
            "event.original": json.dumps(body),
            "user.name": g.user.get('username'),
            "user.roles": [g.user.get('role')]
        })
        return jsonify({'status': 'success', 'message': 'User created', 'user': user.serialize()}), 201

    def updateUser(self, id, body):
        eventId = str(uuid4())
        
        user = User.query.filter_by(id=id).first()
        if user is None:
            current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                "client.ip": request.remote_addr,
                "http.request.method": request.method,
                "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                "event.action": "UPDATE_USER",
                "event.outcome": "failure",
                "event.reason": "User not found",
                "event.id": eventId,
                "event.original": json.dumps(body.dict()),
                "user.name": g.user.get('username'),
                "user.roles": [g.user.get('role')],
                "client.user.id": id
            })
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        user.role=body.username,

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
            "client.ip": request.remote_addr,
            "http.request.method": request.method,
            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
            "event.action": "UPDATE_USER",
            "event.outcome": "success",
            "event.id": eventId,
            "event.original": json.dumps(body.dict()),
            "user.name": g.user.get('username'),
            "user.roles": [g.user.get('role')],
            "client.user.id": id
        })
        return jsonify({'status': 'success', 'message': 'User updated', 'user': user.serialize()}), 200