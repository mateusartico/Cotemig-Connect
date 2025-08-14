from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.base_model import User, PasswordResetToken
from app.models.database import db
from app.views.auth_forms import LoginForm, CadastroForm, RecuperarSenhaForm, RedefinirSenhaForm
from app.utils.email_service import send_password_reset_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(matricula=form.matricula.data).first()
        
        if user and user.check_password(form.senha.data):
            session['user_id'] = user.id
            session['user_nome'] = user.nome
            session['user_email'] = user.email
            session['user_tipo'] = user.tipo_usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Matrícula ou senha incorretos', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        try:
            user = User(
                nome=form.nome.data,
                email=form.email.data,
                senha=form.senha.data
            )
            db.session.add(user)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao realizar cadastro', 'error')
    
    return render_template('auth/cadastro.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    form = RecuperarSenhaForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Criar token de recuperação
            token = PasswordResetToken(user.id)
            db.session.add(token)
            db.session.commit()
            
            # Enviar email de recuperação
            reset_link = url_for('auth.redefinir_senha', token=token.token, _external=True)
            
            if send_password_reset_email(user.email, user.nome, reset_link):
                flash('Link de recuperação enviado para seu email!', 'success')
            else:
                flash('Erro ao enviar email. Verifique o console.', 'error')
        else:
            flash('Email não encontrado', 'error')
    
    return render_template('auth/recuperar_senha.html', form=form)

@auth_bp.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    reset_token = PasswordResetToken.query.filter_by(token=token).first()
    
    if not reset_token or not reset_token.is_valid():
        flash('Token inválido ou expirado', 'error')
        return redirect(url_for('auth.login'))
    
    form = RedefinirSenhaForm()
    if form.validate_on_submit():
        user = reset_token.user
        user.senha = user._hash_password(form.senha.data)
        reset_token.mark_as_used()
        db.session.commit()
        
        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/redefinir_senha.html', form=form, token=token)