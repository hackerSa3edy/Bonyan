$(document).ready(function() {
    // Authentication functions
    function getAccessToken() {
        return localStorage.getItem('accessToken');
    }

    function getRefreshToken() {
        return localStorage.getItem('refreshToken');
    }

    function clearTokens() {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    }

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
                    clearTokens();
                    window.location.href = '/login';
                }
                throw new Error('Failed to refresh token');
            }
            return response.json();
        })
        .then(data => {
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
        });
    }

    function authenticatedRequest(url, method, data, retryCount = 1) {
        return fetch(url, {
            method: method,
            headers: {
                'Authorization': 'Bearer ' + getAccessToken(),
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: data ? JSON.stringify(data) : undefined
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401 && retryCount > 0) {
                    return refreshAccessToken().then(() => authenticatedRequest(url, method, data, retryCount - 1));
                }
                return response.text().then(text => {
                    const errorMessage = text ? JSON.parse(text).detail : 'Request failed';
                    throw new Error(errorMessage);
                });
            }
            return response.text().then(text => {
                return text ? JSON.parse(text) : {}; // Handle empty response
            });
        });
    }

    // Tab switching
    $('#profile-tab').click(function() {
        $('#profile-form').removeClass('hidden').addClass('block');
        $('#password-form').removeClass('block').addClass('hidden');
        $('#profile-tab').addClass('text-blue-600').removeClass('text-gray-700');
        $('#password-tab').addClass('text-gray-700').removeClass('text-blue-600');
    });

    $('#password-tab').click(function() {
        $('#password-form').removeClass('hidden').addClass('block');
        $('#profile-form').removeClass('block').addClass('hidden');
        $('#password-tab').addClass('text-blue-600').removeClass('text-gray-700');
        $('#profile-tab').addClass('text-gray-700').removeClass('text-blue-600');
    });

    // Function to fetch and set the avatar URL
    function fetchAvatarUrl() {
        return authenticatedRequest('/api/user/avatar/', 'GET')
            .then(data => {
                return data.avatar || null;
            })
            .catch(() => {
                showMessage('Failed to fetch avatar. Please try again.', 'red');
                return null;
            });
    }

    function setAvatarUrl(avatarUrl) {
        if (avatarUrl) {
            $('.profile-pic').attr('src', avatarUrl).removeClass('hidden');
            $('.avatar-initials').addClass('hidden');
        } else {
            $('.profile-pic').addClass('hidden');
            $('.avatar-initials').removeClass('hidden');
        }
    }

    $('#upload-avatar').click(function(e) {
        e.preventDefault();
        $('<input type="file">').click().on('change', function() {
            const file = this.files[0];
            
            const formData = new FormData();
            formData.append('avatar', file);
            
            fetch('/api/user/avatar/', {
                method: 'PUT',
                headers: {
                    'Authorization': 'Bearer ' + getAccessToken(),
                    'Accept': 'application/json',
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) throw new Error('Failed to update avatar');
                showMessage('Avatar updated successfully!', 'green');
                return response.json();
            })
            .then(data => {
                setAvatarUrl(data.avatar);
            })
            .catch(() => {
                showMessage('Failed to update avatar. Please try again.', 'red');
            });
        });
    });

    $('#delete-avatar').click(function(e) {
        e.preventDefault();
        authenticatedRequest('/api/user/avatar/', 'DELETE')
            .then(() => {
                $('.profile-pic').attr('src', '').addClass('hidden');
                $('.avatar-initials').removeClass('hidden');
                showMessage('Avatar deleted successfully!', 'green');
            })
            .catch(() => {
                showMessage('Failed to delete avatar. Please try again.', 'red');
            });
    });

    // Fetch initial profile data
    let initialProfileData = {};
    authenticatedRequest('/api/user/profile/', 'GET')
        .then(data => {
            initialProfileData = data; // Store the initial profile data
            $('#email').val(data.email);
            $('#first_name').val(data.first_name);
            $('#last_name').val(data.last_name);
            $('#bio').val(data.bio);
            $('#role').val(data.role);
            $('#header-username').text(data.first_name + ' ' + data.last_name);
            $('.avatar-initials').text(data.first_name.charAt(0) + data.last_name.charAt(0));
        })
        .catch(() => {
            showMessage('Failed to fetch profile data. Please refresh the page.', 'red');
        });

    // Fetch and set the avatar URL
    fetchAvatarUrl().then(setAvatarUrl);

    // Profile form submission
    $('#profile-settings-form').submit(function(e) {
        e.preventDefault();
        const currentProfileData = {
            email: $('#email').val(),
            first_name: $('#first_name').val(),
            last_name: $('#last_name').val(),
            bio: $('#bio').val()
        };

        const changedFields = {};

        for (const key in currentProfileData) {
            if (currentProfileData[key] !== initialProfileData[key]) {
                changedFields[key] = currentProfileData[key];
            }
        }

        if (Object.keys(changedFields).length === 0) {
            showMessage('No changes detected.', 'blue');
            return;
        }

        authenticatedRequest('/api/user/profile/', 'PUT', changedFields)
            .then(() => {
                showMessage('Profile updated successfully!', 'green');
                $('#header-username').text($('#first_name').val() + ' ' + $('#last_name').val());
                $('.avatar-initials').text($('#first_name').val().charAt(0) + $('#last_name').val().charAt(0));
                // Update initialProfileData with the new values
                Object.assign(initialProfileData, changedFields);
            })
            .catch(() => {
                showMessage('Failed to update profile. Please try again.', 'red');
            });
    });
    // Function to validate password
    function validatePassword(password) {
        return password.length >= 8;
    }

    // Password form submission
    $('#password-settings-form').submit(function(e) {
        e.preventDefault();
        const currentPassword = $('input[name="current_password"]').val();
        const newPassword = $('input[name="new_password"]').val();
        const confirmPassword = $('input[name="confirm_password"]').val();

        if (!validatePassword(newPassword)) {
            showMessage('Password must be at least 8 characters long.', 'red');
            return;
        }

        if (newPassword !== confirmPassword) {
            showMessage('New password and confirm password do not match.', 'red');
            return;
        }

        const formData = {
            current_password: currentPassword,
            new_password: newPassword
        };
        
        authenticatedRequest('/api/user/change-password/', 'PUT', formData)
            .then(() => {
                showMessage('Password changed successfully!', 'green');
                $('#password-settings-form')[0].reset();
            })
            .catch((data) => {
                if (data === 'Request failed') {
                    showMessage('Failed to change password. Please try again.', 'red');
                }
                else {
                    showMessage(data, 'red');
                }
            });
    });

    // Delete account functionality
    $('#profile-settings-form .bg-red-500').click(function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            authenticatedRequest('/api/user/profile/', 'DELETE')
                .then(() => {
                    showMessage('Account deleted successfully!', 'green');
                    // Wait for 3 seconds, then clear tokens and redirect to login page
                    setTimeout(() => {
                        clearTokens(); // Function to clear tokens
                        window.location.href = '/login'; // Redirect to login page
                    }, 3000);
                })
                .catch(() => {
                    showMessage('Failed to delete account. Please try again.', 'red');
                });
        }
    });

    // Logout functionality
    $('a:contains("Log out")').click(function(e) {
        e.preventDefault();
        authenticatedRequest('/api/auth/logout/', 'POST', { refresh: getRefreshToken() })
            .then(() => {
                showMessage('Logged out successfully!', 'green');
                // Wait for 2 seconds, then clear tokens and redirect to login page
                setTimeout(() => {
                    clearTokens(); // Function to clear tokens
                    window.location.href = '/login'; // Redirect to login page
                }, 2000);
            })
            .catch(() => {
                showMessage('Failed to logout. Please try again.', 'red');
            });
    });

    function showMessage(message, color) {
        const popup = $('<div>', {
            class: `bg-${color}-500 text-white p-4 rounded shadow-lg max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl mx-auto`,
            text: message
        });
        $('#error-messages-container').append(popup);
        popup.hide().fadeIn(300);
        setTimeout(() => popup.fadeOut(300, function() { $(this).remove(); }), 5000);
    }

    // Toggle sidebar
    $('#toggle-sidebar').click(function() {
        $('#sidebar').toggleClass('sidebar-open sidebar-closed');
        $('#main-content').toggleClass('lg:ml-0 lg:ml-64');
        
        if ($('#sidebar').hasClass('sidebar-closed')) {
            $('#toggle-sidebar').html('<i class="fas fa-bars"></i>');
        } else {
            $('#toggle-sidebar').html('<i class="fas fa-times"></i>');
        }
    });

    // Initialize sidebar state
    if ($(window).width() >= 1024) {
        $('#sidebar').removeClass('sidebar-closed').addClass('sidebar-open');
        $('#main-content').addClass('lg:ml-64');
        $('#toggle-sidebar').html('<i class="fas fa-times"></i>');
    } else {
        $('#sidebar').removeClass('sidebar-open').addClass('sidebar-closed');
        $('#main-content').removeClass('lg:ml-64');
        $('#toggle-sidebar').html('<i class="fas fa-bars"></i>');
    }
});