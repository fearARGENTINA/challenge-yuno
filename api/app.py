from flask import Flask
from extensions import db
from flask_cors import CORS
from config.config import SQLALCHEMY_DATABASE_URL, FILEBEAT_HOST, FILEBEAT_PORT
import logging
import ecs_logging
from helpers.logHandlers import PlainTextTcpHandler

def createApp():
    app = Flask(__name__)
    CORS(app)


    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
    db.init_app(app)

    socket_handler = PlainTextTcpHandler(FILEBEAT_HOST, FILEBEAT_PORT)
    socket_handler.setLevel(logging.INFO)
    socket_handler.setFormatter(ecs_logging.StdlibFormatter())
    app.logger.addHandler(socket_handler)
    app.logger.setLevel(logging.INFO)

    from routes.main import mainRoute
    from routes.employees import employeeRoute
    from routes.users import userRoute
    from routes.oauth import oauthRoute
    app.register_blueprint(mainRoute)
    app.register_blueprint(employeeRoute)
    app.register_blueprint(userRoute)
    app.register_blueprint(oauthRoute)

    return app

if __name__ == '__main__':
    app = createApp()
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=8080, debug=True)