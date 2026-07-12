import dotenv

from flask import Flask
from flask_smorest import Api

from db import db, database_uri

from services.item import blp as ItemBlueprint
from services.store import blp as StoreBlueprint


def create_app(db_url=None):

    dotenv.load_dotenv()

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri(db_url)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context(): 
        db.create_all()
    
    api = Api(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()    
    app.run()

