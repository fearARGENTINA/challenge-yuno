from flask import Blueprint, jsonify, url_for, request
from controllers.oauth import OAuthController

oauthRoute = Blueprint('oauth', __name__)

@oauthRoute.route('/oauth/login')
def login():
    try:
        redirectUri = url_for('oauth.callback', _external=True)
        return OAuthController(redirectUri).login()
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened', 'error': str(e)})
    
@oauthRoute.route('/oauth/callback')
def callback():
    try:
        redirectUri = url_for('oauth.callback', _external=True)
        return OAuthController(redirectUri).callback()
    except Exception as e:
        return jsonify({'status': 'error', 'reason': 'something unexpected happened', 'error': str(e)})