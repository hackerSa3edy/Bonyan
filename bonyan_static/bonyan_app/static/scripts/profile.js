$(document).ready(function () {
  const fields = [
    'username', 'email', 'city', 'level', 'first_name', 'second_name', 'third_name', 'fourth_name',
    'gender', 'birth_date', 'address', 'phone_number', 'department', 'specialization'
  ];
  const originalData = {};

  const populateUserProfile = (data) => {
    $('#username').val(data.username);
    $('#profile-name').text(data.username);
    $('#email').val(data.email);
    $('#city').val(data.city);
    if ('level' in data) {
      $('#h-level').text('Level ' + data.level);
      $('#level').val(data.level);
    } else {
      $('#level').parent().hide();
      $('#h-level').hide();
    }
    $('#first_name').val(data.first_name);
    $('#second_name').val(data.second_name);
    $('#third_name').val(data.third_name);
    $('#fourth_name').val(data.fourth_name);
    $('#gender').val(data.gender);
    $('#birth_date').val(data.birth_date);
    $('#address').val(data.address);
    $('#phone_number').val(data.phone);
    if ('department' in data) {
      $('#department').val(data.department.title);
    } else {
      $('#department').hide();
    }
    if ('specialization' in data) {
      $('#specialization').val(data.courses[0].title);
    } else {
      $('#specialization').hide();
    }
    $('#joined_at').text('Joined at: ' + new Date(data.date_joined).toLocaleDateString());

    fields.forEach(field => {
      originalData[field] = $(`#${field}`).val();
    });
  };

  const handleAjaxError = (jqXHR, textStatus) => {
    const errorMessage = jqXHR?.responseJSON?.detail ||
      jqXHR?.responseJSON?.username ||
      jqXHR?.responseJSON?.email ||
      textStatus;
    $('#flash-message').text(errorMessage).removeClass('hidden');
    setTimeout(() => {
      $('#flash-message').addClass('hidden');
    }, 5000);
  };

  const getUserProfile = (userId, token, url) => {
    $.ajax({
      url: url + userId + '/',
      type: 'GET',
      headers: {
        Authorization: 'Bearer ' + token
      },
      success: populateUserProfile,
      error: handleAjaxError
    });
  };

  const getURL = (userRole) => {
    const baseURL = '/api/accounts/';
    let url;
    switch (userRole) {
      case 'admin':
        url = baseURL + 'admins/';
        break;
      case 'instructor':
        url = baseURL + 'instructors/';
        break;
      case 'student':
        url = baseURL + 'students/';
        break;
      default:
        url = baseURL;
    }
    return url;
  };

  const token = document.cookie.replace(/(?:(?:^|.*;\s*)jwtAccess\s*=\s*([^;]*).*$)|^.*$/, '$1');
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace('-', '+').replace('_', '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  const userId = JSON.parse(jsonPayload).user_id;
  const userRole = JSON.parse(jsonPayload).user_role;
  const url = getURL(userRole);
  getUserProfile(userId, token, url);

  let isEditing = false;

  $('#update').click(function () {
    if (isEditing) {
      // Cancel update
      $('input, select').not('#username, #email').each(function () {
        $(this).prop('readonly', true).prop('disabled', true);
      });
      $(this).removeClass('bg-white text-blue-500 border border-blue-500').addClass('bg-blue-500 text-white').text('Update');
      $('#save').hide();
      isEditing = false;
    } else {
      // Enable update
      $('input, select').not('#username, #email').each(function () {
        $(this).prop('readonly', false).prop('disabled', false);
      });
      $(this).addClass('bg-white text-blue-500 border border-blue-500').removeClass('bg-blue-500 text-white').text('Cancel');
      $('#save').show();
      isEditing = true;
    }
  });

  $('#save').hide(); // Initially hide the save button

  $('#save').click(function () {
    const userData = {};
    fields.forEach(field => {
      const currentValue = $(`#${field}`).val();
      if (currentValue !== originalData[field] && !$(`#${field}`).is(':hidden')) {
        userData[field] = currentValue;
      }
      $('#save').hide(); // Initially hide the save button
    });

    $.ajax({
      url: url + userId + '/',
      type: 'PUT',
      headers: {
        Authorization: 'Bearer ' + token
      },
      contentType: 'application/json',
      data: JSON.stringify(userData),
      success: (data) => {
        populateUserProfile(data);
        $('input, select').each(function () {
          $(this).prop('readonly', true).prop('disabled', true);
        });
        $('#update').removeClass('bg-white text-blue-500 border border-blue-500').addClass('bg-blue-500 text-white');
        $('#flash-message').text('Profile updated successfully').removeClass('hidden bg-red-100 border-red-400 text-red-700').addClass('bg-green-100 border-green-400 text-green-700');
        setTimeout(() => {
          $('#flash-message').addClass('hidden');
        }, 5000);
      },
      error: handleAjaxError
    });
  });
});