$(document).ready(function() {
    /**
     * Stores the access and refresh tokens in localStorage.
     * @param {string} access - The access token.
     * @param {string} refresh - The refresh token.
     */
    function storeTokens(access, refresh) {
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
    }

    /**
     * Handles the form submission for login.
     * Prevents the default form submission behavior, retrieves the email and password values,
     * and sends a POST request to the authentication API endpoint.
     */
    document.getElementById('login-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
    
        fetch('/api/auth/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Invalid email or password. Please try again.');
                } else {
                    throw new Error('An error occurred. Please try again later.');
                }
            }
            return response.json();
        })
        .then(data => {
            storeTokens(data.access, data.refresh);
            window.location.href = '/dashboard';
            // console.log('Login successful:', data);
        })
        .catch(error => {
            showError(error.message);
        });
    });

    /**
     * Displays an error message in a popup.
     * @param {string} message - The error message to display.
     */
    function showError(message) {
        $('#error-message').text(message);
        $('#error-popup').addClass('show');
        setTimeout(function() {
            $('#error-popup').removeClass('show');
        }, 5000);
    }
});