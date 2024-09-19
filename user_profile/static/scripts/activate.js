$(document).ready(function() {
    // Get the token from the URL
    var token = window.location.pathname.split('/').pop();

    // Make the API call
    fetch('/api/user/activate/' + token, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 400) {
                updateContent('invalid');
            } else if (response.status === 409) {
                updateContent('already-activated');
            } else if (response.status === 410) {
                updateContent('expired');
            } else {
                updateContent('error');
            }
            throw new Error('Request failed with status ' + response.status);
        }
        return response.json();
    })
    .then(response => {
        updateContent('success');
    })
    .catch(error => {
        console.error('Error:', error);
    });

    function updateContent(status) {
        var content = '';
        var title = '';
        switch(status) {
            case 'success':
                title = 'Account Activated Successfully';
                content = `
                    <div class="mb-6">
                        <img src="{% static 'assets/acc_activated.png' %}" alt="User icon with a checkmark" class="mx-auto w-20 h-20 sm:w-24 sm:h-24" />
                    </div>
                    <p class="text-gray-600 mb-6 text-sm sm:text-base">
                        Congratulations! Your account is now active and ready to go. Welcome to our community!
                    </p>
                    <a href="{% url 'authentication-web:login' %}" class="bg-blue-500 hover:bg-blue-600 transition-colors duration-300 text-white py-2 px-4 rounded-full font-bold inline-block">
                        LOGIN TO YOUR ACCOUNT
                    </a>
                `;
                break;
            case 'already-activated':
                title = 'Account Already Activated';
                content = `
                    <div class="mb-6">
                        <img src="{% static 'assets/acc_activated.png' %}" alt="User icon with a checkmark" class="mx-auto w-20 h-20 sm:w-24 sm:h-24" />
                    </div>
                    <p class="text-gray-600 mb-6 text-sm sm:text-base">
                        Good news! Your account is already active. No further action is needed.
                    </p>
                    <a href="{% url 'authentication-web:login' %}" class="bg-blue-500 hover:bg-blue-600 transition-colors duration-300 text-white py-2 px-4 rounded-full font-bold inline-block">
                        LOGIN TO YOUR ACCOUNT
                    </a>
                `;
                break;
            case 'invalid':
                title = 'Invalid Activation Token';
                content = `
                    <div class="mb-6">
                        <i class="fas fa-exclamation-triangle fa-3x text-yellow-500"></i>
                    </div>
                    <p class="text-gray-600 mb-6 text-sm sm:text-base">
                        Oops! The activation token appears to be invalid. Please check your email for the correct link or contact support.
                    </p>
                `;
                break;
            case 'expired':
                title = 'Activation Token Expired';
                content = `
                    <div class="mb-6">
                        <i class="fas fa-clock fa-3x text-red-500"></i>
                    </div>
                    <p class="text-gray-600 mb-6 text-sm sm:text-base">
                        Sorry, your activation token has expired. Please register again to receive a new activation link.
                    </p>
                    <a href="{% url 'authentication-web:register' %}" class="bg-blue-500 hover:bg-blue-600 transition-colors duration-300 text-white py-2 px-4 rounded-full font-bold inline-block">
                        REGISTER AGAIN
                    </a>
                `;
                break;
            default:
                title = 'Activation Error';
                content = `
                    <div class="mb-6">
                        <i class="fas fa-exclamation-circle fa-3x text-red-500"></i>
                    </div>
                    <p class="text-gray-600 mb-6 text-sm sm:text-base">
                        An unexpected error occurred during account activation. Please try again later or contact support.
                    </p>
                `;
        }
        $('h1').text(title);
        $('#message-container').html(content);
    }
});