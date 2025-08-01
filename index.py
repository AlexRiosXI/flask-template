from app import  app
from sierra_madre_core.models.abstract_models import db
from flask_migrate import Migrate

import os

from dotenv import load_dotenv
load_dotenv()



migrate = Migrate(app, db)


db.init_app(app)


with app.app_context():
    db.create_all()





if __name__ == "__main__":
    host = os.getenv('HOST')
    if host is None:
        host = '127.0.0.1'

    app.run(
        host="0.0.0.0",
        port=5001,
        ssl_context=("certs/localhost.pem", "certs/localhost-key.pem"),
        debug=True
    )
