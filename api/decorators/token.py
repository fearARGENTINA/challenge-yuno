from flask import request, jsonify, g, current_app
from config.config import JWT_SECRET
from functools import wraps
import jwt
from uuid import uuid4
import json

def tokenRequired(*neededRoles):
    def decTokenRequired(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            eventId = str(uuid4())
            token = None
            try:
                if 'Authorization' in request.headers:
                    token = request.headers['Authorization'].split(" ")[1]
                if not token:
                    current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                        "client.ip": request.remote_addr,
                        "http.request.method": request.method,
                        "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                        "event.action": "TOKEN_CHECK",
                        "event.outcome": "failure",
                        "event.reason": "Token not found in headers",
                        "event.id": eventId
                    })
                    return jsonify({"status": "error", "reason":"Unauthenticated"}), 401

                try:
                    claims = jwt.decode(token, JWT_SECRET, algorithms='HS256')

                    role = claims.get('role')

                    g.user = claims

                    allowedRoles = list(map(lambda r: r.name, neededRoles))
                    if len(allowedRoles) and not role in allowedRoles:
                        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                            "client.ip": request.remote_addr,
                            "http.request.method": request.method,
                            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                            "event.action": "TOKEN_CHECK",
                            "event.outcome": "failure",
                            "event.reason": "Role not allowed to perform",
                            "event.id": eventId,
                            "user.name": g.user.get("username"),
                            "user.roles": [g.user.get("role")]
                        })
                        return jsonify({"status": "error", "reason":"Not sufficient roles"}), 401

                except jwt.ExpiredSignatureError:
                    current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                        "client.ip": request.remote_addr,
                        "http.request.method": request.method,
                        "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                        "event.action": "TOKEN_CHECK",
                        "event.outcome": "failure",
                        "event.reason": "Expired JWT",
                        "event.id": eventId
                    })
                    return jsonify({"status": "error", "reason":"Access token expired"}), 401
                except Exception as e:
                    current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                        "client.ip": request.remote_addr,
                        "http.request.method": request.method,
                        "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                        "event.action": "TOKEN_CHECK",
                        "event.outcome": "failure",
                        "event.reason": "Invalid token",
                        "event.id": eventId
                    })
                    return jsonify({"status": "error", "reason":"Access token invalid", 'error': str(e)}), 401
                
                current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
                    "client.ip": request.remote_addr,
                    "http.request.method": request.method,
                    "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
                    "event.action": "TOKEN_CHECK",
                    "event.outcome": "success",
                    "event.id": eventId,
                    "user.name": g.user.get("username"),
                    "user.roles": [g.user.get("role")]
                })
                ret = f(*args, **kwargs)
                return ret
            except Exception:
                return jsonify({"status": "error", "reason":"Something unexpected happened"}), 500
        return decorator
    return decTokenRequired