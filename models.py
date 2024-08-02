from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(255), nullable=False)
    carrera = db.Column(db.String(50), nullable=True)
    año_de_ingreso = db.Column(db.Integer, nullable=True)

    @property
    def contraseña(self):
        raise AttributeError('La contraseña no es un atributo legible.')

    @contraseña.setter
    def contraseña(self, contraseña):
        self.contraseña_hash = generate_password_hash(contraseña)

    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña_hash, contraseña)

class Publicacion(db.Model):
    __tablename__ = 'publicaciones'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicaciones.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

class Amigo(db.Model):
    __tablename__ = 'amigos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id_1 = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario_id_2 = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
