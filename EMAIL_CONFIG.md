# Configuração de Email - Cotemig Connect

## Para Gmail (Recomendado para desenvolvimento)

1. **Ativar verificação em 2 etapas** na sua conta Google
2. **Gerar senha de app**:
   - Acesse: https://myaccount.google.com/apppasswords
   - Selecione "Email" e "Outro (nome personalizado)"
   - Digite "Cotemig Connect"
   - Copie a senha gerada (16 caracteres)

3. **Configurar .env**:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=senha-de-app-de-16-caracteres
MAIL_DEFAULT_SENDER=seu-email@gmail.com
```

## Para Outlook/Hotmail

```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@outlook.com
MAIL_PASSWORD=sua-senha
MAIL_DEFAULT_SENDER=seu-email@outlook.com
```

## Para outros provedores

- **Yahoo**: smtp.mail.yahoo.com:587
- **UOL**: smtps.uol.com.br:587

## Modo Desenvolvimento

Se não configurar email, o sistema mostra o link no console:
```
=== EMAIL NÃO CONFIGURADO - MODO DESENVOLVIMENTO ===
Usuário: João Silva (joao@email.com)
Link: http://localhost:5000/auth/redefinir-senha/token123
==================================================
```

## Testando

1. Configure o .env com suas credenciais
2. Reinicie a aplicação
3. Teste a recuperação de senha
4. Verifique se o email chegou na caixa de entrada