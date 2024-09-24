$(document).ready(function() {
    // Function to store tokens in localStorage
    function storeTokens(access, refresh) {
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
    }

    // // Function to get the access token
    // function getAccessToken() {
    //     return localStorage.getItem('accessToken');
    // }

    // // Function to get the refresh token
    // function getRefreshToken() {
    //     return localStorage.getItem('refreshToken');
    // }

    // // Function to clear tokens (for logout)
    // function clearTokens() {
    //     localStorage.removeItem('accessToken');
    //     localStorage.removeItem('refreshToken');
    // }

    // // Function to refresh the access token
    // function refreshAccessToken() {
    //     return $.ajax({
    //         url: '/api/auth/token/refresh/',
    //         method: 'POST',
    //         data: JSON.stringify({ refresh: getRefreshToken() }),
    //         contentType: 'application/json',
    //         dataType: 'json'
    //     }).done(function(data) {
    //         storeTokens(data.access, data.refresh);
    //     }).fail(function(jqXHR) {
    //         if (jqXHR.status === 401) {
    //             // Refresh token is invalid, logout the user
    //             clearTokens();
    //             window.location.href = '/login';  // Redirect to login page
    //         }
    //     });
    // }

    // // Function to make authenticated requests
    // function authenticatedRequest(url, method, data) {
    //     return $.ajax({
    //         url: url,
    //         method: method,
    //         headers: {
    //             'Authorization': 'Bearer ' + getAccessToken()
    //         },
    //         data: JSON.stringify(data),
    //         contentType: 'application/json',
    //         dataType: 'json'
    //     }).fail(function(jqXHR) {
    //         if (jqXHR.status === 401) {
    //             // Access token might be expired, try to refresh
    //             return refreshAccessToken().then(function() {
    //                 // Retry the original request with the new token
    //                 return authenticatedRequest(url, method, data);
    //             });
    //         }
    //         // If it's not a 401 error, reject the promise
    //         return $.Deferred().reject(jqXHR);
    //     });
    // }

    // Handle form submission
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
            return response.json()
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

    function showError(message) {
        $('#error-message').text(message);
        $('#error-popup').addClass('show');
        setTimeout(function() {
            $('#error-popup').removeClass('show');
        }, 5000);
    }

    // // Example of how to use the authenticatedRequest function
    // // This could be placed in another script file that handles dashboard functionality
    // function fetchDashboardData() {
    //     authenticatedRequest('/api/dashboard/', 'GET')
    //         .done(function(data) {
    //             // Handle successful dashboard data fetch
    //             console.log('Dashboard data:', data);
    //         })
    //         .fail(function(jqXHR) {
    //             // Handle error
    //             console.error('Failed to fetch dashboard data:', jqXHR);
    //         });
    // }

    // // Logout functionality
    // $('#logout-button').on('click', function(e) {
    //     e.preventDefault();
    //     clearTokens();
    //     window.location.href = '/login';
    // });
});