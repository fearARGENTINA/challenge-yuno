from flask import Blueprint, jsonify

mainRoute = Blueprint('main', __name__)

@mainRoute.route('/')
def main():
    return jsonify({"version": 1.0})
