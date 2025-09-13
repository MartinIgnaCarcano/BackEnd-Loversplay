from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from models import Usuario
from database import db

auth_bp = Blueprint("auth", __name__,url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y password son requeridos"}), 400

    user = Usuario.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token
    }), 200

@auth_bp.route("/register", methods=["POST"])
def crear_usuario():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email y password son requeridos"}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    nuevo_usuario = Usuario(
        nombre=data.get("nombre"),
        email=data["email"],
        fecha_registro=db.func.now()   
    )
    nuevo_usuario.set_password(data["password"])

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuario creado con éxito"}), 201

@auth_bp.route("/", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {
            "id": u.id,
            "nombre": u.nombre,
            "email": u.email,
            "fecha_registro": u.fecha_registro.isoformat()
        }
        for u in usuarios
    ])


@auth_bp.route("/", methods=["PATCH"])
@jwt_required()
def actualizar_usuario():
    current = get_jwt_identity()  # dict con {id, email, rol}
    user = Usuario.query.get(current)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json() or {}

    # Solo actualizamos los campos permitidos si vienen en la request
    if "nombre" in data:
        user.nombre = data["nombre"]

    if "direccion" in data:
        user.direccion = data["direccion"]

    if "telefono" in data:
        user.telefono = data["telefono"]

    if "password" in data:
        user.set_password(data["password"])

    db.session.commit()

    return jsonify({
        "message": "Usuario actualizado",
        "user": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "direccion": user.direccion,
            "telefono": user.telefono,
            "rol": user.rol
        }
    }), 200
    
