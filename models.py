from datetime import datetime
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    
    pedidos = db.relationship("Pedido", backref="usuario", lazy=True)
    resenas = db.relationship("Resena", backref="usuario", lazy=True)

    # Guardar password en hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verificar password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    url_imagen = db.Column(db.String(200))
    slug = db.Column(db.String(150), nullable=True) # Nuevo atributo para 'slug'

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)  # Corresponde a 'name'
    slug = db.Column(db.String(150), unique=True, nullable=False) # Nuevo atributo para 'slug'
    precio = db.Column(db.Float, nullable=False) # Corresponde a 'price'
    cantidad_resenas = db.Column(db.Integer, default=0) # Nuevo atributo para 'reviewsCount'
    descripcion_corta = db.Column(db.String(255)) # Nuevo atributo para 'shortDesc'
    descripcion_larga = db.Column(db.Text) # Corresponde a 'description'
    stock = db.Column(db.Integer, default=0) # Mantenido, corresponde a 'stock'
    peso = db.Column(db.Float, default=0.4)  # en kg
    url_imagen_principal = db.Column(db.String(200)) # Podría usarse para la imagen principal de 'images'
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"))

    vistas = db.Column(db.Integer, default=0) # Nuevo atributo para 'views'
    valoracion_promedio = db.Column(db.Float, default=0.0) # Nuevo atributo para 'rating'
    
    imagenes = db.relationship("ImagenProducto", backref="producto", lazy=True)
    resenas = db.relationship("Resena", backref="producto", lazy=True)
    detalles_pedido = db.relationship("PedidoDetalle", backref="producto", lazy=True)

    
class ImagenProducto(db.Model):
    __tablename__ = "imagenes_productos"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    url_imagen = db.Column(db.String(200), nullable=False)

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default="pendiente")
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    total = db.Column(db.Float, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
     
    detalles = db.relationship("PedidoDetalle", backref="pedido", lazy=True)
    
class PedidoDetalle(db.Model):
    __tablename__ = "pedido_detalle"
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
class Resena(db.Model):
    __tablename__ = "resenas"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)    


