from flask import jsonify, request, current_app
from authlib.integrations.requests_client import OAuth2Session
from config.config import CLIENT_ID, CLIENT_SECRET, CLIENT_SCOPE, AUTHORIZE_URL, ACCESS_TOKEN_URL, REDIRECT_URI, USERINFO_URL, JWT_SECRET, DEFAULT_ADMIN_EMAIL, DEFAULT_ROLE, Role, JWT_DURATION
from exceptions.oauth import AuthorizationHeaderNotFound
import jwt
from models.user import User
from extensions import db
from datetime import datetime, timedelta, timezone
from uuid import uuid4

class OAuthController:
    def __init__(self, redirectUri=None):
        self.clientId = CLIENT_ID
        self.clientSecret = CLIENT_SECRET
        self.authorizationEndpoint = AUTHORIZE_URL
        self.tokenEndpoint = ACCESS_TOKEN_URL
        self.scope = CLIENT_SCOPE
        self.redirectUri = REDIRECT_URI
        if self.redirectUri is not None:
            self.redirectUri = redirectUri
            self.client = OAuth2Session(
                client_id=self.clientId,
                client_secret=self.clientSecret,
                authorization_endpoint=self.authorizationEndpoint,
                token_endpoint=self.tokenEndpoint,
                scope=self.scope,
                redirect_uri=self.redirectUri,
            )

    def login(self):
        eventId = str(uuid4())
        uri = self.client.create_authorization_url(self.authorizationEndpoint)
        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
            "client.ip": request.remote_addr,
            "http.request.method": request.method,
            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
            "event.action": "LOGIN_START",
            "event.outcome": "success",
            "event.id": eventId
        })
        return jsonify({"redirect_url": uri})
    
    def callback(self):
        eventId = str(uuid4())
        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
            "client.ip": request.remote_addr,
            "http.request.method": request.method,
            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
            "event.action": "CALLBACK_START",
            "event.outcome": "success",
            "event.id": eventId
        })

        token = self.client.fetch_token(
            url=self.tokenEndpoint,
            authorization_response=request.url,
            redirect_uri=self.redirectUri
        )

        client = OAuth2Session(token={"access_token": token['access_token'], "token_type": "Bearer"})
        userinfoData = client.get(USERINFO_URL).json()

        username=userinfoData.get('email')
        user = User.query.filter_by(username=username).first()

        if user is None:
            role = (Role.ADMIN if DEFAULT_ADMIN_EMAIL == username else DEFAULT_ROLE).name
            user = User(
                username=username,
                role=role
            )
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
        else:
            role = user.role.name

        current_app.logger.info(f"{request.method} {request.path} from {request.remote_addr}.", extra={
            "client.ip": request.remote_addr,
            "http.request.method": request.method,
            "http.request.body.content": f"{request.method} {request.path} from {request.remote_addr}.",
            "event.action": "CALLBACK_END",
            "event.outcome": "success",
            "event.id": eventId,
            "user.name": username,
            "user.roles": [role]
        })

        expirationDatetime = datetime.now(timezone.utc) + timedelta(seconds=JWT_DURATION)
        expirationEpoch = int(expirationDatetime.timestamp())

        accessToken = {
            'oauth': userinfoData,
            'username': username,
            'role': role,
            'exp': expirationEpoch
        }

        encodedAccessToken = jwt.encode(accessToken, JWT_SECRET, algorithm='HS256')
        return jsonify({"jwt": encodedAccessToken, 'accessToken': accessToken})