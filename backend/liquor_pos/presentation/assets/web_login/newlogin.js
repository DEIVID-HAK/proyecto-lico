document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const submitBtn = document.getElementById('submitBtn');
    const errorMsg = document.getElementById('errorMessage');

    // Inicializar QWebChannel para hablar con Python
    let backend;
    if (typeof qt !== 'undefined') {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            backend = channel.objects.backend;
        });
    }

    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();

        submitBtn.innerText = 'Verifying...';
        submitBtn.disabled = true;
        errorMsg.style.display = 'none';

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (backend) {
            // Llamar a Python
            backend.authenticate(username, password, function(response) {
                if(response.success) {
                    submitBtn.innerText = 'Success!';
                    // El backend se encargará de cambiar la ventana
                } else {
                    submitBtn.innerText = 'Sign In';
                    submitBtn.disabled = false;
                    errorMsg.innerText = response.error;
                    errorMsg.style.display = 'block';
                    document.getElementById('password').value = '';
                }
            });
        } else {
            // Fallback si se abre en un navegador normal
            setTimeout(() => {
                alert(`Welcome back, ${username}! (No Python backend connected)`);
                submitBtn.innerText = 'Sign In';
                submitBtn.disabled = false;
                loginForm.reset();
            }, 1200);
        }
    });
});
