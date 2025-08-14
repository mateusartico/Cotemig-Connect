from app.models.database import db
from datetime import datetime, timedelta
import bcrypt
import re
import secrets

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(8), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # aluno, professor, monitor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.matricula = self._extrair_matricula_usuario(email)
        self.senha = self._hash_password(senha)
        self.tipo_usuario = self._determinar_tipo_usuario(email)
    
    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.senha.encode('utf-8'))
    
    def _extrair_matricula_usuario(self, email):
        if email.endswith('@aluno.cotemig.com.br'):
            return email.split('@')[0]  # Matrícula do aluno
        elif email.endswith('@cotemig.com.br'):
            return email.split('@')[0]  # Usuário do funcionário
        return email.split('@')[0]
    
    def _determinar_tipo_usuario(self, email):
        if email.endswith('@aluno.cotemig.com.br'):
            return 'aluno'
        elif email.endswith('@cotemig.com.br'):
            if 'professor' in email.lower():
                return 'professor'
            elif 'monitor' in email.lower():
                return 'monitor'
        return 'aluno'
    
    @staticmethod
    def validar_email_aluno(email):
        if not email.endswith('@aluno.cotemig.com.br'):
            return False
        matricula = email.split('@')[0]
        return len(matricula) == 8 and matricula.isdigit()
    
    @staticmethod
    def validar_email_funcionario(email):
        return email.endswith('@cotemig.com.br') and ('professor' in email.lower() or 'monitor' in email.lower())
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'matricula': self.matricula,
            'email': self.email,
            'tipo_usuario': self.tipo_usuario
        }

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='reset_tokens')
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.token = secrets.token_urlsafe(32)
        self.expires_at = datetime.utcnow() + timedelta(hours=1)  # Expira em 1 hora
    
    def is_valid(self):
        return not self.used and datetime.utcnow() < self.expires_at
    
    def mark_as_used(self):
        self.used = True