from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models.base_model import User

class LoginForm(FlaskForm):
    matricula = StringField('Matrícula/Usuário', validators=[
        DataRequired(message='Matrícula ou usuário é obrigatório')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=2, max=100, message='Nome deve ter entre 2 e 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter pelo menos 6 caracteres')
    ])
    submit = SubmitField('Cadastrar')
    
    def validate_email(self, email):
        if not (User.validar_email_aluno(email.data) or User.validar_email_funcionario(email.data)):
            if email.data.endswith('@aluno.cotemig.com.br'):
                raise ValidationError('Para alunos, use sua matrícula de 8 dígitos antes do @')
            else:
                raise ValidationError('Email deve ser @aluno.cotemig.com.br ou @cotemig.com.br (professor/monitor)')
        
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já cadastrado')

class RecuperarSenhaForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    submit = SubmitField('Enviar Link de Recuperação')

class RedefinirSenhaForm(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[
        DataRequired(message='Nova senha é obrigatória'),
        Length(min=6, message='Senha deve ter pelo menos 6 caracteres')
    ])
    submit = SubmitField('Redefinir Senha')