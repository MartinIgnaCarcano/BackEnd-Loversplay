from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Pedido, PedidoDetalle, Producto, Usuario
from database import db

pedidos_bp = Blueprint("pedidos", __name__,url_prefix="/api/pedidos")

# Listar pedidos del usuario logueado
@pedidos_bp.route("/<int:usuario_id>", methods=["GET"])
def listar_pedidos(usuario_id):
    pedidos = Pedido.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([
        {
            "id": p.id,
            "estado": p.estado,
            "total": p.total,
            "detalles": [
                {
                    "producto": i.producto.nombre,
                    "cantidad": i.cantidad,
                    "precio_unitario": i.precio_unitario
                } for i in p.detalles
            ]
        } for p in pedidos
    ])

# Crear un pedido manual (sin carrito)
@pedidos_bp.route("/", methods=["POST"])
def crear_pedido():
    #current_id = get_jwt_identity()
    data = request.get_json()
    #El id que por ahora me lo manden en la request
    current_id = data.get("usuario_id")
    direccion = data.get("direccion", "")
    if not data.get("detalles") or not isinstance(data["detalles"], list):
        return jsonify({"error": "Se requiere lista de detalles"}), 400

    total = 0
    detalles_pedido = []

    for item in data["detalles"]:
        producto = Producto.query.get(item["producto_id"])
        if not producto:
            return jsonify({"error": f"Producto id {item['producto_id']} no encontrado"}), 404
        cantidad = item.get("cantidad", 1)
        subtotal = producto.precio * cantidad
        detalles_pedido.append(
            PedidoDetalle(
                producto_id=producto.id,
                cantidad=cantidad,
                subtotal=subtotal
            )
        )

    pedido = Pedido(usuario_id=current_id, total=total, estado="PENDIENTE", detalles=detalles_pedido)
    db.session.add(pedido)
    db.session.commit()

    return jsonify({"message": "Pedido creado", "pedido_id": pedido.id}), 201

# Ver detalle de un pedido
@pedidos_bp.route("/unico/<int:id>", methods=["GET"])
def detalle_pedido(id):
    pedido = Pedido.query.get(id)
    if not pedido:
        return jsonify({"error": "Pedido no encontrado"}), 404

    return jsonify({
        "id": pedido.id,
        "estado": pedido.estado,
        "total": pedido.total,
        "fecha_creacion": pedido.fecha_creacion.isoformat(),
        "detalles": [
            {
                "producto": i.producto.nombre,
                "cantidad": i.cantidad,
                "precio_unitario": i.precio_unitario,
                "subtotal": i.subtotal
            } for i in pedido.detalles
        ]
    })

# Actualizar estado del pedido (solo admin para cambiar a ENVIADO o ENTREGADO)
@pedidos_bp.route("/<int:id>", methods=["PATCH"])
def actualizar_pedido(id):
    current = get_jwt_identity()
    data = request.get_json() or {}
    pedido = Pedido.query.get_or_404(id)

    # Solo admin puede cambiar estado
    if "estado" in data:
        if current.get("rol") != "ADMIN":
            return jsonify({"error": "Acceso denegado"}), 403
        pedido.estado = data["estado"]

    db.session.commit()
    return jsonify({"message": "Pedido actualizado", "estado": pedido.estado})


