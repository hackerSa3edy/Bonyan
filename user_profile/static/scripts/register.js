$(document).ready(function() {
    // // Function to show error messages in a pop-up
    // function showError(message) {
    //     const popup = $('<div>', {
    //         class: 'fixed top-4 right-4 bg-red-500 text-white p-4 rounded shadow-lg z-50',
    //         text: message
    //     }).appendTo('body');
    //     setTimeout(() => popup.remove(), 5000);
    // }

    // Function to show error messages in a pop-up
    function showError(message) {
        const popup = $('<div>', {
            class: 'bg-red-500 text-white p-4 rounded shadow-lg max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl mx-auto',
            text: message
        });
        $('#error-messages-container').append(popup);
        popup.hide().fadeIn(300);
        setTimeout(() => popup.fadeOut(300, function() { $(this).remove(); }), 5000);
    } 

    // Function to validate email
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Function to validate password
    function validatePassword(password) {
        return password.length >= 8;
    }

    // Function to handle form submission
    async function handleSubmit(event) {
        event.preventDefault();
        
        const firstName = $('#first-name').val().trim();
        const secondName = $('#second-name').val().trim();
        const email = $('#email').val().trim();
        const password = $('#password').val();
        const retypePassword = $('#retype-password').val();
        const role = $('#role').val();

        // Validate form data
        if (!firstName || !secondName) {
            showError('Please enter both first and second names.');
            return;
        }

        if (!validateEmail(email)) {
            showError('Please enter a valid email address.');
            return;
        }

        if (!validatePassword(password)) {
            showError('Password must be at least 8 characters long.');
            return;
        }

        if (password !== retypePassword) {
            showError('Passwords do not match.');
            return;
        }

        if (!role) {
            showError('Please select a role.');
            return;
        }

        // Prepare data for API request
        const data = {
            first_name: firstName,
            last_name: secondName,
            email: email,
            password: password,
            role: role
        };

        try {
            const response = await $.ajax({
                url: '/api/user/register/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json'
                },
            });

            if (response.ok) {
                // Redirect to activate route
                window.location.href = '/activation';
            } else {
                showError(response.error || 'Registration failed. Please try again.');
            }
        } catch (error) {
            if (error.responseJSON && error.status === 400) {
                const errorData = error.responseJSON;
                for (const key in errorData) {
                    showError(`${key}: ${errorData[key]}`);
                }
            } else {
                showError('An error occurred. Please try again later.');
            }
        }
    }

    // Function to handle next step
    function nextStep(currentStep) {
        if (currentStep === 1) {
            const firstName = $('#first-name').val().trim();
            const secondName = $('#second-name').val().trim();
            const email = $('#email').val().trim();

            if (!firstName || !secondName) {
                showError('Please enter both first and second names.');
                return;
            }

            if (!validateEmail(email)) {
                showError('Please enter a valid email address.');
                return;
            }
        }

        $(`#step${currentStep}`).removeClass('active');
        $(`#step${currentStep + 1}`).addClass('active');
    }

    // Function to handle previous step
    function prevStep(currentStep) {
        $(`#step${currentStep}`).removeClass('active');
        $(`#step${currentStep - 1}`).addClass('active');
    }

    // Function to handle Enter key press
    function handleEnterKey(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const activeStep = $('.form-step.active');
            if (activeStep.attr('id') === 'step1') {
                nextStep(1);
            } else if (activeStep.attr('id') === 'step2') {
                handleSubmit(event);
            }
        }
    }

    // Add event listeners
    $('#registrationForm').on('submit', handleSubmit);

    // Add event listener for Enter key on the entire form
    $('#registrationForm').on('keydown', handleEnterKey);

    // Expose nextStep and prevStep functions globally
    window.nextStep = nextStep;
    window.prevStep = prevStep;
});