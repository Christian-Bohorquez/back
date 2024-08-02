from flask import request, jsonify
from app import app, db
from models import Usuario, Publicacion, Comentario, Amigo
from auth import create_token, jwt_required
from flask_jwt_extended import get_jwt_identity

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        carrera=data.get('carrera'),
        año_de_ingreso=data.get('año_de_ingreso')
    )
    nuevo_usuario.contraseña = data['contraseña']
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario registrado con éxito'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if usuario and usuario.verificar_contraseña(data['contraseña']):
        token = create_token(usuario.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Credenciales inválidas'}), 401

@app.route('/api/posts', methods=['GET'])
@jwt_required()
def get_posts():
    current_user_id = get_jwt_identity()
    posts = Publicacion.query.all()
    result = [{'id': post.id, 'usuario_id': post.usuario_id, 'contenido': post.contenido, 'fecha': post.fecha} for post in posts]
    return jsonify(result), 200

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    nueva_publicacion = Publicacion(
        usuario_id=current_user_id,
        contenido=data['contenido']
    )
    db.session.add(nueva_publicacion)
    db.session.commit()
    return jsonify({'message': 'Publicación creada con éxito'}), 201

@app.route('/api/comments', methods=['POST'])
@jwt_required()
def create_comment():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    nuevo_comentario = Comentario(
        publicacion_id=data['publicacion_id'],
        usuario_id=current_user_id,
        contenido=data['contenido']
    )
    db.session.add(nuevo_comentario)
    db.session.commit()
    return jsonify({'message': 'Comentario creado con éxito'}), 201

@app.route('/api/friends', methods=['GET'])
@jwt_required()
def get_friends():
    current_user_id = get_jwt_identity()
    amigos = Amigo.query.filter((Amigo.usuario_id_1 == current_user_id) | (Amigo.usuario_id_2 == current_user_id)).all()
    result = [{'usuario_id_1': amigo.usuario_id_1, 'usuario_id_2': amigo.usuario_id_2, 'fecha': amigo.fecha} for amigo in amigos]
    return jsonify(result), 200

@app.route('/api/friends', methods=['POST'])
@jwt_required()
def add_friend():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    nuevo_amigo = Amigo(
        usuario_id_1=current_user_id,
        usuario_id_2=data['usuario_id_2']
    )
    db.session.add(nuevo_amigo)
    db.session.commit()
    return jsonify({'message': 'Amigo agregado con éxito'}), 201
