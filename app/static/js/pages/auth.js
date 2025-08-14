// Funcionalidades de autenticação

// Toggle senha
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    const icon = document.getElementById(fieldId + '-toggle-icon');
    
    if (field.type === 'password') {
        field.type = 'text';
        icon.textContent = 'Ocultar';
    } else {
        field.type = 'password';
        icon.textContent = 'Mostrar';
    }
}

// Indicador de força da senha
function initPasswordStrength() {
    const senhaField = document.getElementById('senha');
    if (!senhaField) return;
    
    senhaField.addEventListener('input', function(e) {
        const password = e.target.value;
        const strengthContainer = document.getElementById('passwordStrength');
        const strengthText = document.getElementById('passwordStrengthText');
        
        if (password.length === 0) {
            strengthContainer.className = 'password-strength';
            strengthText.textContent = '';
            return;
        }
        
        let strength = 0;
        let criteria = [];
        
        if (password.length >= 6) {
            strength++;
            criteria.push('comprimento');
        }
        if (password.match(/[a-z]/)) {
            strength++;
            criteria.push('minúscula');
        }
        if (password.match(/[A-Z]/)) {
            strength++;
            criteria.push('maiúscula');
        }
        if (password.match(/[0-9]/)) {
            strength++;
            criteria.push('número');
        }
        if (password.match(/[^a-zA-Z0-9]/)) {
            strength++;
            criteria.push('símbolo');
        }
        
        strengthContainer.className = 'password-strength';
        
        if (strength <= 2) {
            strengthContainer.classList.add('password-strength-weak');
            strengthText.textContent = 'Senha fraca';
        } else if (strength <= 3) {
            strengthContainer.classList.add('password-strength-medium');
            strengthText.textContent = 'Senha média';
        } else {
            strengthContainer.classList.add('password-strength-strong');
            strengthText.textContent = 'Senha forte';
        }
    });
}

// Inicializar quando DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    initPasswordStrength();
});