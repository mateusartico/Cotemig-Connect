from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from app.models.base_model import User
from app.models.database import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@main_bp.route('/api/user-data')
def get_user_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Não autorizado'}), 401
    
    user = User.query.get(session['user_id'])
    if user:
        return jsonify({
            'nome': user.nome,
            'email': user.email,
            'matricula': user.matricula,
            'tipo_usuario': user.tipo_usuario
        })
    return jsonify({'error': 'Usuário não encontrado'}), 404

@main_bp.route('/api/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Não autorizado'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    try:
        # Atualizar nome se fornecido
        if 'nome' in data and data['nome'].strip():
            user.nome = data['nome'].strip()
            session['user_nome'] = user.nome
        
        # Atualizar senha se fornecida
        if 'senha' in data and data['senha'].strip():
            user.senha = user._hash_password(data['senha'])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Perfil atualizado com sucesso!'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar perfil'}), 500