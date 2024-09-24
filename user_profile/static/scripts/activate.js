$(document).ready(function() {
    // Get the token from the URL
    var pathname = window.location.pathname.split('/');
    var activateIndex = pathname.indexOf('activate');
    var token = activateIndex !== -1 && pathname.length > activateIndex + 1 ? pathname[activateIndex + 1] : null;

    // Make the API call
    fetch(`/api/user/activate/${token}/`, {
        method: 'GET',
        headers:{
            'Accept': 'application/json',
        }
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
        // Hide all message blocks
        $('#message-container > div').hide();

        // Show the appropriate message block
        switch(status) {
            case 'success':
                $('#activation-title').text('Account Activated Successfully');
                $('#success-message').show();
                break;
            case 'already-activated':
                $('#activation-title').text('Account Already Activated');
                $('#already-activated-message').show();
                break;
            case 'invalid':
                $('#activation-title').text('Invalid Activation Token');
                $('#invalid-message').show();
                break;
            case 'expired':
                $('#activation-title').text('Activation Token Expired');
                $('#expired-message').show();
                break;
            default:
                $('#activation-title').text('Activation Error');
                $('#error-message').show();
        }
    }
});