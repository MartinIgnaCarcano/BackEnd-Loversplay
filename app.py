from flask import Flask
from database import db
from routes.categorias import categorias_bp
from routes.productos import productos_bp
from routes.pedidos import pedidos_bp
from routes.auth import auth_bp
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Configuración de SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = "cambia-esto-por-un-secreto-seguro"  # usa variable de entorno en prod
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

db.init_app(app)
jwt = JWTManager(app)
# Registrar rutas
app.register_blueprint(auth_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(pedidos_bp)

# Crear tablas al iniciar
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


#activar venv
#venv\Scripts\activate