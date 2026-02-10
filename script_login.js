document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    // Toggle password visibility
    togglePassword.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);

        // Toggle icon
        togglePassword.classList.toggle('fa-eye');
        togglePassword.classList.toggle('fa-eye-slash');
    });

    // Form submission
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const submitButton = loginForm.querySelector('.login-button');
        const buttonText = submitButton.querySelector('.button-text');
        const icon = submitButton.querySelector('i');

        // Loading state mockup
        submitButton.disabled = true;
        buttonText.textContent = 'Connexion...';
        icon.className = 'fas fa-circle-notch fa-spin';

        setTimeout(() => {
            console.log('Login attempt for:', username);
            // In a real app, this is where the API call happens

            // Animation success mockup
            submitButton.style.background = '#2ecc71';
            buttonText.textContent = 'Succès !';
            icon.className = 'fas fa-check';

            // Simulation redirect
            setTimeout(() => {
                alert('Connexion réussie ! Redirection vers le tableau de bord...');
                // window.location.href = 'dashboard.html';

                // Reset button for demo purposes
                submitButton.disabled = false;
                submitButton.style.background = '';
                buttonText.textContent = 'Se connecter';
                icon.className = 'fas fa-arrow-right';
            }, 1000);
        }, 1500);
    });
});
