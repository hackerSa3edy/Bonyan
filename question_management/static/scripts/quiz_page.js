$(document).ready(function() {
    // Variables to store quiz state
    let quizId;
    let questions = [];
    let currentQuestionIndex = 0;
    let userAnswers = {};
    let quizDuration;
    let timerInterval;
    let nextPage = 1;
    let hasMoreQuestions = true;
    let attemptId;

    // Extract quiz token from the current URL
    const pathArray = window.location.pathname.split('/');
    const quizToken = pathArray[pathArray.length - 2];

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

    // Start the quiz by creating an attempt
    function startQuiz() {
        authenticatedRequest('/api/participation/attempts/start_quiz/', 'POST', { quiz_id: quizToken })
            .then(response => {
                attemptId = response.id;
                quizId = response.quiz_id;
                fetchQuizDetails();
            })
            .catch(error => {
                console.error('Error starting quiz:', error);
                showMessage('Failed to start quiz. Please try again.', 'red');
            });
    }

    // Calculate the duration of the quiz
    function calculateDuration(startTime, endTime) {
        const start = new Date(startTime);
        const end = new Date(endTime);
        const now = new Date();

        let durationInSeconds;

        if (now < start) {
            durationInSeconds = (end - start) / 1000;
        } else if (now >= start && now <= end) {
            durationInSeconds = (end - now) / 1000;
        } else {
            durationInSeconds = 0;
        }

        return Math.round(durationInSeconds);
    }

    // Fetch quiz details
    function fetchQuizDetails() {
        authenticatedRequest(`/api/quizzes/${quizId}/`, 'GET')
            .then(quizData => {
                $('#quiz-title').text(quizData.title);
                quizDuration = calculateDuration(quizData.start_time, quizData.end_time);
                startTimer();
                fetchQuestions();
            })
            .catch(error => {
                console.error('Error fetching quiz details:', error);
                showMessage('Failed to fetch quiz details. Please try again.', 'red');
            });
    }

    // Fetch questions for the quiz
    function fetchQuestions() {
        if (!hasMoreQuestions) return;
        authenticatedRequest(`/api/quizzes/${quizId}/questions/?page=${nextPage}`, 'GET')
            .then(fetchedQuestions => {
                if (fetchedQuestions.next === null) {
                    hasMoreQuestions = false;
                } else {
                    questions = questions.concat(fetchedQuestions.results);
                    nextPage++;
                }
                displayQuestion(currentQuestionIndex);
            })
            .catch(error => {
                console.error('Error fetching questions:', error);
                showMessage('Failed to fetch questions. Please try again.', 'red');
            });
    }

    // Display a question
    function displayQuestion(index) {
        const question = questions[index];
        $('#question-text').text(question.text);

        const optionsContainer = $('#options-container');
        optionsContainer.empty();

        question.options.forEach((option, optionIndex) => {
            const optionElement = $('<div>', {
                class: 'flex items-center space-x-2'
            }).append(
                $('<input>', {
                    type: 'radio',
                    id: `option-${optionIndex}`,
                    name: 'quiz-option',
                    value: optionIndex,
                    class: 'form-radio'
                }).change(saveCurrentAnswer),
                $('<label>', {
                    for: `option-${optionIndex}`,
                    text: option,
                    class: 'text-gray-700'
                })
            );
            optionsContainer.append(optionElement);
        });

        if (userAnswers[question.id] !== undefined) {
            $(`#option-${userAnswers[question.id]}`).prop('checked', true);
        }

        updateNavigationButtons();

        if (index >= questions.length - 3 && hasMoreQuestions) {
            fetchQuestions();
        }
    }

    // Update navigation buttons
    function updateNavigationButtons() {
        $('#prev-btn').prop('disabled', currentQuestionIndex === 0);
        $('#next-btn').text(currentQuestionIndex === questions.length - 1 ? 'Finish' : 'Next');
    }

    // Handle previous button click
    $('#prev-btn').click(function() {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion(currentQuestionIndex);
        }
    });

    // Handle next button click
    $('#next-btn').click(function() {
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
        } else {
            confirmSubmission();
        }
    });

    // Handle submit button click
    $('#submit-btn').click(confirmSubmission);

    // Save the current answer
    function saveCurrentAnswer() {
        const selectedOption = $('input[name="quiz-option"]:checked').val();
        if (selectedOption !== undefined) {
            const questionId = questions[currentQuestionIndex].id;
            userAnswers[questionId] = parseInt(selectedOption);

            const answerData = {
                attempt_id: attemptId,
                question_id: questionId,
                selected_option: userAnswers[questionId]
            };

            authenticatedRequest(`/api/participation/attempts/${attemptId}/submit_answer/`, 'POST', answerData)
                .then(response => {
                    console.log('Answer submitted successfully:', response);
                })
                .catch(error => {
                    console.error('Error submitting answer:', error);
                    showMessage('Failed to submit answer. Please try again.', 'red');
                });
        }
    }

    // Confirm quiz submission
    function confirmSubmission() {
        if (confirm('Are you sure you want to submit the quiz? You won\'t be able to change your answers after submission.')) {
            submitQuiz();
        }
    }

    // Submit the quiz
    function submitQuiz() {
        clearInterval(timerInterval);

        authenticatedRequest(`/api/participation/attempts/${attemptId}/finish_quiz/`, 'POST')
            .then(response => {
                showMessage('Quiz submitted successfully!', 'green');
                window.location.href = `/api/participation/attempts/${attemptId}/results/`;
            })
            .catch(error => {
                console.error('Error submitting quiz:', error);
                showMessage('Failed to submit quiz. Please try again.', 'red');
            });
    }

    // Start the quiz timer
    function startTimer() {
        let timeLeft = quizDuration;
        updateTimerDisplay(timeLeft);

        timerInterval = setInterval(() => {
            timeLeft--;
            updateTimerDisplay(timeLeft);

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                alert('Time\'s up! The quiz will be submitted automatically.');
                submitQuiz();
            }
        }, 1000);
    }

    // Update the timer display
    function updateTimerDisplay(timeLeft) {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        $('#timer').text(`${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
    }

    // Show a message to the user
    function showMessage(message, color) {
        const popup = $('<div>', {
            class: `bg-${color}-500 text-white p-4 rounded shadow-lg max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl mx-auto`,
            text: message
        });
        $('#error-messages-container').append(popup);
        popup.hide().fadeIn(300);
        setTimeout(() => popup.fadeOut(300, function() { $(this).remove(); }), 5000);
    }

    // Make an authenticated request
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
                return text ? JSON.parse(text) : {};
            });
        });
    }

    // Start the quiz when the page is ready
    startQuiz();
});