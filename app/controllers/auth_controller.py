from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.base_model import User
from app.models.database import db
from app.views.auth_forms import LoginForm, CadastroForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(matricula=form.matricula.data).first()
        
        if user and user.check_password(form.senha.data):
            session['user_id'] = user.id
            session['user_nome'] = user.nome
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