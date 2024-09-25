$(document).ready(function() {
    // Function to store tokens in localStorage
    function storeTokens(access, refresh) {
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
    }

    // Function to set cookie
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    // Handle form submission
    $('#login-form').on('submit', function(e) {
        e.preventDefault();
        
        const username = $('#username').val();
        const password = $('#pass').val();
        const rememberMe = $('#remember-me').is(':checked');

        fetch('/api/auth/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ username: username, password: password })
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Invalid username or password. Please try again.');
                } else {
                    throw new Error('An error occurred. Please try again later.');
                }
            }
            return response.json();
        })
        .then(data => {
            storeTokens(data.access, data.refresh);
            
            if (rememberMe) {
                // Set cookie to expire in 7 days
                setCookie('jwtAccess', data.access, 7);
            } else {
                // Set cookie that expires when browser is closed
                setCookie('jwtAccess', data.access);
            }
            
            window.location.href = '/profile';
        })
        .catch(error => {
            showError(error.message);
        });
    });

    function showError(message) {
        $('#flash-message').text(message).show();
        setTimeout(function() {
            $('#flash-message').hide();
        }, 5000);
    }
});