from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project.apis import blueprint as api
import os

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api/v1')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)


class VMInstanse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    cloud_id = db.Column(db.String(100), nullable=True)
    cloud_port_id = db.Column(db.String(100), nullable=True)
    is_preemptible = db.Column(db.Boolean, default=False, nullable=True)

    def __repr__(self):
        return f"<vm_instanse {self.cloud_id}>"


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run(host="0.0.0.0", port=5005, debug=True)
