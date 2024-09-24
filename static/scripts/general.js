$(document).ready(function() {
    // Function to store tokens in localStorage
    function storeTokens(access, refresh) {
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
    }

    // Function to get the access token
    function getAccessToken() {
        return localStorage.getItem('accessToken');
    }

    // Function to get the refresh token
    function getRefreshToken() {
        return localStorage.getItem('refreshToken');
    }

    // Function to clear tokens (for logout)
    function clearTokens() {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    }

    // Function to refresh the access token
    function refreshAccessToken() {
        return fetch('/api/auth/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ refresh: getRefreshToken() })
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    // Refresh token is invalid, logout the user
                    clearTokens();
                    window.location.href = '/login';  // Redirect to login page
                }
                return Promise.reject(response);
            }
            return response.json();
        })
        .then(data => {
            storeTokens(data.access, data.refresh);
        });
    }

    // Function to make authenticated requests
    function authenticatedRequest(url, method, data, retryCount = 1) {
        return fetch(url, {
            method: method,
            headers: {
                'Authorization': 'Bearer ' + getAccessToken(),
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401 && retryCount > 0) {
                    // Access token might be expired, try to refresh
                    return refreshAccessToken().then(() => {
                        // Retry the original request with the new token
                        return authenticatedRequest(url, method, data, retryCount - 1);
                    });
                }
                return Promise.reject(response);
            }
            return response.json();
        });
    }
});