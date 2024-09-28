$(document).ready(function() {
    /**
     * Displays a popup message.
     * @param {string} message - The message to display.
     * @param {string} color - The color of the popup background.
     */
    function showMessage(message, color) {
        const popup = $('<div>', {
            class: `bg-${color}-500 text-white p-4 rounded shadow-lg max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl mx-auto`,
            text: message
        });
        $('#error-messages-container').append(popup);
        popup.hide().fadeIn(300);
        setTimeout(() => popup.fadeOut(300, function() { $(this).remove(); }), 5000);
    }

    // Toggle sidebar visibility
    $('#toggle-sidebar').click(function() {
        $('#sidebar').toggleClass('-translate-x-full');
        $('#main-content').toggleClass('lg:ml-64');

        if ($('#sidebar').hasClass('-translate-x-full')) {
            $('#toggle-sidebar').html('<i class="fas fa-bars"></i>');
        } else {
            $('#toggle-sidebar').html('<i class="fas fa-times"></i>');
        }
    });

    // Toggle between list and grid view for quizzes
    $('#grid-view-icon').click(function() {
        $('#quizzes-container').removeClass('grid-cols-1 lg:grid-cols-2');
        $('#quizzes-attempts, #quizzes').addClass('grid-quiz-container').removeClass('space-y-4');
        $(this).addClass('text-blue-600');
        $('#list-view-icon').removeClass('text-blue-600');
    });

    $('#list-view-icon').click(function() {
        $('#quizzes-container').addClass('grid-cols-1 lg:grid-cols-2');
        $('#quizzes-attempts, #quizzes').removeClass('grid-quiz-container').addClass('space-y-4');
        $(this).addClass('text-blue-600');
        $('#grid-view-icon').removeClass('text-blue-600');
    });

    // Authentication functions
    /**
     * Retrieves the access token from local storage.
     * @returns {string} The access token.
     */
    function getAccessToken() {
        return localStorage.getItem('accessToken');
    }

    /**
     * Retrieves the refresh token from local storage.
     * @returns {string} The refresh token.
     */
    function getRefreshToken() {
        return localStorage.getItem('refreshToken');
    }

    /**
     * Clears the access and refresh tokens from local storage.
     */
    function clearTokens() {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    }

    /**
     * Refreshes the access token using the refresh token.
     * @returns {Promise} A promise that resolves when the token is refreshed.
     */
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

    /**
     * Makes an authenticated request to the specified URL.
     * @param {string} url - The URL to request.
     * @param {string} method - The HTTP method to use.
     * @param {Object} [data] - The data to send with the request.
     * @param {number} [retryCount=1] - The number of times to retry the request if unauthorized.
     * @returns {Promise} A promise that resolves with the response data.
     */
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

    /**
     * Fetches the user profile and updates the UI.
     */
    function fetchUserProfile() {
        authenticatedRequest('/api/user/profile/', 'GET')
            .then(data => {
                $('#header-username').text(data.first_name + ' ' + data.last_name);

                if (data.avatar) {
                    $('.profile-pic').attr('src', data.avatar).removeClass('hidden');
                    $('.avatar-initials').addClass('hidden');
                } else {
                    $('.avatar-initials').text(data.first_name.charAt(0) + data.last_name.charAt(0)).removeClass('hidden');
                    $('.profile-pic').addClass('hidden');
                }
            })
            .catch(error => {
                console.error('Error fetching user profile:', error);
                showMessage('Failed to fetch user profile. Please try again.', 'red');
            });
    }

    // Initialize sidebar state based on window width
    if ($(window).width() >= 1024) {
        $('#sidebar').removeClass('-translate-x-full');
        $('#main-content').addClass('lg:ml-64');
        $('#toggle-sidebar').html('<i class="fas fa-times"></i>');
    } else {
        $('#sidebar').addClass('-translate-x-full');
        $('#main-content').removeClass('lg:ml-64');
        $('#toggle-sidebar').html('<i class="fas fa-bars"></i>');
    }

    // Logout functionality
    $('#sidebar a:contains("Log out")').click(function(e) {
        e.preventDefault();
        authenticatedRequest('/api/auth/logout/', 'POST', { refresh: getRefreshToken() })
            .then(() => {
                showMessage('Logged out successfully!', 'green');
                setTimeout(() => {
                    clearTokens();
                    window.location.href = '/login';
                }, 2000);
            })
            .catch(() => {
                showMessage('Failed to logout. Please try again.', 'red');
            });
    });

    /**
     * Fetches quizzes and populates the dashboard.
     */
    function fetchQuizzes() {
        authenticatedRequest('/api/quizzes/', 'GET')
            .then(quizzes => {
                $('#quizzes').empty();
                quizzes.results.forEach(quiz => {
                    if (quiz.is_published) {
                        const quizCard = createQuizCard(quiz);
                        $('#quizzes').append(quizCard);
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching quizzes:', error);
                showMessage('Failed to fetch quizzes. Please try again.', 'red');
            });
    }

    /**
     * Fetches quiz attempts and populates the dashboard.
     */
    function fetchQuizAttempts() {
        authenticatedRequest('/api/participation/attempts/', 'GET')
            .then(attempts => {
                $('#quizzes-attempts').empty();
                attempts.results.forEach(attempt => {
                    const attemptCard = createAttemptCard(attempt);
                    $('#quizzes-attempts').append(attemptCard);
                });
            })
            .catch(error => {
                console.error('Error fetching quiz attempts:', error);
                showMessage('Failed to fetch quiz attempts. Please try again.', 'red');
            });
    }

    /**
     * Creates a quiz card element.
     * @param {Object} quiz - The quiz data.
     * @returns {string} The HTML string for the quiz card.
     */
    function createQuizCard(quiz) {
        const startTime = new Date(quiz.start_time);
        const endTime = new Date(quiz.end_time);

        let duration;
        if (endTime && startTime) {
            if (endTime > startTime) {
                duration = (endTime - startTime) / (1000 * 60); // Duration in minutes
                duration = Math.round(duration); // Round to nearest minute
            } else {
                duration = 'N/A'; // Invalid duration
            }
        } else {
            duration = 'N/A'; // Missing start or end time
        }

        return `
            <div class="quiz-card bg-blue-50 rounded-lg p-4 shadow-sm flex flex-col">
                <h3 class="font-semibold text-lg mb-2">${quiz.title}</h3>
                <p class="text-sm text-gray-600 mb-2">${quiz.description}</p>
                <p class="text-sm text-gray-600 mb-1">Created by: ${quiz.creator.name}</p>
                <p class="text-sm text-gray-600 mb-1">Starts: ${startTime ? startTime.toLocaleString() : 'Not set'}</p>
                <p class="text-sm text-gray-600 mb-1">Duration: ${duration} minutes</p>
                <button class="start-quiz-btn w-full bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition duration-300 mt-auto" data-quiz-id="${quiz.id}">
                    Start Quiz
                </button>
            </div>
        `;
    }

    /**
     * Creates a quiz attempt card element.
     * @param {Object} attempt - The quiz attempt data.
     * @returns {string} The HTML string for the quiz attempt card.
     */
    function createAttemptCard(attempt) {
        const startTime = new Date(attempt.start_time);
        const completedAt = attempt.completed_at ? new Date(attempt.completed_at) : null;

        return `
            <div class="quiz-card bg-green-50 rounded-lg p-4 shadow-sm flex flex-col">
                <h3 class="font-semibold text-lg mb-2">${attempt.quiz}</h3>
                <p class="text-sm text-gray-600 mb-1">Started: ${startTime.toLocaleString()}</p>
                <p class="text-sm text-gray-600 mb-1">Completed: ${completedAt ? completedAt.toLocaleString() : 'Not completed'}</p>
                ${attempt.is_completed ? `<p class="text-sm font-semibold mb-2">Score: ${attempt.score}%</p>` : ''}
                <button class="view-results-btn w-full bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md transition duration-300 mt-auto" data-attempt-id="${attempt.id}">
                    ${attempt.is_completed ? 'View Results' : 'Continue Quiz'}
                </button>
            </div>
        `;
    }

    // Initialize the dashboard
    fetchUserProfile();
    fetchQuizzes();
    fetchQuizAttempts();

    // Event delegation for dynamically created buttons
    $(document).on('click', '.start-quiz-btn', function() {
        const quizId = $(this).data('quiz-id');
        // Implement quiz start logic here
        console.log('Starting quiz:', quizId);
    });

    $(document).on('click', '.view-results-btn', function() {
        const attemptId = $(this).data('attempt-id');
        // Implement view/continue quiz logic here
        console.log('Viewing/Continuing attempt:', attemptId);
    });
});