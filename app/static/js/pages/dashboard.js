// Dashboard Cotemig Connect - Funcionalidades

document.addEventListener('DOMContentLoaded', function() {
    initDashboard();
});

// Inicializar dashboard
function initDashboard() {
    console.log('Cotemig Connect Dashboard carregado!');
    
    // Configurar navegação
    setupNavigation();
    
    // Configurar animações
    setupAnimations();
    
    // Carregar dados do usuário
    loadUserData();
}

// Configurar sistema de navegação
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const section = this.dataset.section;
            switchSection(section);
            
            // Atualizar navegação ativa
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Trocar seção ativa
function switchSection(sectionName) {
    // Esconder todas as seções
    const sections = document.querySelectorAll('.dashboard-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Mostrar seção selecionada
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Atualizar navegação se não foi clicada diretamente
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(nav => {
        nav.classList.remove('active');
        if (nav.dataset.section === sectionName) {
            nav.classList.add('active');
        }
    });
}

// Configurar animações
function setupAnimations() {
    // Animação de entrada dos cards
    const cards = document.querySelectorAll('.stat-card, .action-btn');
    
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Função de logout
function logout() {
    if (confirm('Tem certeza que deseja sair?')) {
        window.location.href = '/auth/logout';
    }
}

// Carregar dados do usuário
async function loadUserData() {
    try {
        const response = await fetch('/api/user-data');
        const data = await response.json();
        
        if (data.error) {
            console.error('Erro ao carregar dados:', data.error);
            return;
        }
        
        // Atualizar elementos da tela
        document.getElementById('profile-name').textContent = data.nome;
        document.getElementById('profile-email').textContent = data.email;
        document.getElementById('profile-matricula').textContent = `Matrícula: ${data.matricula}`;
        document.getElementById('profile-avatar-text').textContent = data.nome[0].toUpperCase();
        
    } catch (error) {
        console.error('Erro ao carregar dados do usuário:', error);
    }
}

// Mostrar formulário de edição
function showEditForm() {
    // Carregar dados atuais no formulário
    const nome = document.getElementById('profile-name').textContent;
    const email = document.getElementById('profile-email').textContent;
    
    document.getElementById('edit-nome').value = nome;
    document.getElementById('edit-email').value = email;
    document.getElementById('edit-senha').value = '';
    
    // Trocar visualização
    document.getElementById('profile-view').style.display = 'none';
    document.getElementById('profile-edit').style.display = 'block';
}

// Cancelar edição
function cancelEdit() {
    document.getElementById('profile-view').style.display = 'block';
    document.getElementById('profile-edit').style.display = 'none';
}

// Salvar perfil
async function saveProfile() {
    const nome = document.getElementById('edit-nome').value.trim();
    const senha = document.getElementById('edit-senha').value.trim();
    
    if (!nome) {
        alert('Nome é obrigatório!');
        return;
    }
    
    // Mostrar loading
    document.getElementById('profile-edit').style.display = 'none';
    document.getElementById('profile-loading').style.display = 'block';
    
    try {
        const response = await fetch('/api/update-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nome: nome,
                senha: senha || undefined
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Atualizar dados na tela
            document.getElementById('profile-name').textContent = nome;
            document.getElementById('profile-avatar-text').textContent = nome[0].toUpperCase();
            
            // Atualizar header também
            const headerName = document.querySelector('.user-details h2');
            if (headerName) {
                headerName.textContent = `Olá, ${nome.split(' ')[0]}!`;
            }
            
            alert('Perfil atualizado com sucesso!');
            cancelEdit();
        } else {
            alert('Erro ao atualizar perfil: ' + (result.error || 'Erro desconhecido'));
        }
        
    } catch (error) {
        console.error('Erro ao salvar perfil:', error);
        alert('Erro ao salvar perfil. Tente novamente.');
    } finally {
        document.getElementById('profile-loading').style.display = 'none';
        document.getElementById('profile-view').style.display = 'block';
    }
}

// Utilitários
const Dashboard = {
    // Mostrar notificação
    showNotification(message, type = 'info') {
        // Implementação futura para notificações
        console.log(`${type.toUpperCase()}: ${message}`);
    },
    
    // Atualizar estatísticas
    updateStats(connections = 0, activities = 0, messages = 0) {
        const statNumbers = document.querySelectorAll('.stat-number');
        if (statNumbers.length >= 3) {
            statNumbers[0].textContent = connections;
            statNumbers[1].textContent = activities;
            statNumbers[2].textContent = messages;
        }
    }
};