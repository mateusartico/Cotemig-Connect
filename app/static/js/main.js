// Função principal que executa quando o DOM está carregado
document.addEventListener('DOMContentLoaded', function() {
    console.log('Web App carregado com sucesso!');
    
    // Inicializar funcionalidades
    initMobileMenu();
    initScrollEffects();
});

// Função para mostrar mensagem (exemplo de interatividade)
function showMessage() {
    alert('Olá! Este é seu web app mobile-first funcionando!');
}

// Inicializar menu mobile (para futuras implementações)
function initMobileMenu() {
    // Placeholder para funcionalidade de menu mobile
    console.log('Menu mobile inicializado');
}

// Efeitos de scroll
function initScrollEffects() {
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        } else {
            navbar.style.backgroundColor = '#fff';
        }
    });
}

// Utilitários
const Utils = {
    // Função para fazer requisições AJAX
    async fetchData(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Erro na requisição:', error);
            throw error;
        }
    },
    
    // Função para detectar dispositivo móvel
    isMobile() {
        return window.innerWidth <= 768;
    }
};