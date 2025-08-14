import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

def send_password_reset_email(user_email, user_name, reset_link):
    """Envia email de recuperação de senha"""
    
    # Verificar se as configurações de email estão definidas
    if not current_app.config.get('MAIL_SERVER'):
        print(f"\n=== EMAIL NÃO CONFIGURADO - MODO DESENVOLVIMENTO ===")
        print(f"Usuário: {user_name} ({user_email})")
        print(f"Link: {reset_link}")
        print("=" * 50)
        return True
    
    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = user_email
        msg['Subject'] = "Cotemig Connect - Recuperação de Senha"
        
        # Corpo do email
        body = f"""
Olá {user_name},

Você solicitou a recuperação de senha para sua conta no Cotemig Connect.

Clique no link abaixo para redefinir sua senha:
{reset_link}

Este link expira em 1 hora.

Se você não solicitou esta recuperação, ignore este email.

Atenciosamente,
Equipe Cotemig Connect
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Conectar ao servidor SMTP
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        
        # Enviar email
        text = msg.as_string()
        server.sendmail(current_app.config['MAIL_DEFAULT_SENDER'], user_email, text)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        # Em caso de erro, mostrar no console para desenvolvimento
        print(f"\n=== ERRO NO EMAIL - MODO FALLBACK ===")
        print(f"Usuário: {user_name} ({user_email})")
        print(f"Link: {reset_link}")
        print("=" * 50)
        return False