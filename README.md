# Web App Mobile First

Uma aplicação web mobile-first desenvolvida com Flask (backend) e HTML/CSS/JS puro (frontend), seguindo arquitetura MVC tradicional.

## Estrutura do Projeto

```
cotemig_connect/
├── app/
│   ├── controllers/          # Controladores (rotas e lógica de controle)
│   ├── models/              # Modelos de dados
│   ├── views/               # Lógica de apresentação
│   ├── static/              # Arquivos estáticos
│   │   ├── css/            # Estilos CSS
│   │   ├── js/             # Scripts JavaScript
│   │   └── images/         # Imagens
│   ├── templates/           # Templates HTML
│   └── __init__.py         # Factory da aplicação
├── config/                  # Configurações
├── tests/                   # Testes
├── venv/                    # Ambiente virtual
├── requirements.txt         # Dependências
├── .env                     # Variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
└── run.py                  # Arquivo principal
```

## Instalação

1. Clone o repositório
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução

```bash
python run.py
```

A aplicação estará disponível em `http://localhost:5000`

## Características

- **Mobile First**: Design responsivo otimizado para dispositivos móveis
- **Arquitetura MVC**: Código organizado e escalável
- **Flask Backend**: API robusta com Python
- **Frontend Puro**: HTML5, CSS3 e JavaScript ES6+
- **Boas Práticas**: Estrutura profissional e manutenível