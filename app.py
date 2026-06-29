from flask import Flask
from database import db
from models import Equipamento, Aluguel, Cliente
from routes.equipamentos import bp as equipamentos_bp
from routes.clientes import bp as clientes_bp
from routes.alugueis import bp as alugueis_bp
from routes.usuario import bp as usuario_bp
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager




load_dotenv()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)

migrate = Migrate(app, db)

jwt = JWTManager(app)


with app.app_context():
    db.create_all()

app.register_blueprint(equipamentos_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(alugueis_bp)
app.register_blueprint(usuario_bp)

if __name__ == "__main__":
    app.run(debug=True)


