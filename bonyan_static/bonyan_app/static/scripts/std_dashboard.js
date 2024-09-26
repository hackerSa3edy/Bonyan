$(document).ready(function () {
  const token = document.cookie.replace(/(?:(?:^|.*;\s*)jwtAccess\s*=\s*([^;]*).*$)|^.*$/, '$1');
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace('-', '+').replace('_', '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

  const userId = JSON.parse(jsonPayload).user_id;

  const handleAjaxError = (jqXHR, textStatus) => {
    $('#flash-message').text(
      jqXHR?.responseJSON?.detail ||
      jqXHR?.responseJSON?.username ||
      jqXHR?.responseJSON?.email ||
      textStatus);
    $('#flash-message').show();
  };

  const populateUserProfile = (data) => {
    const courses = data.courses;
    const coursesContainer = $('.courses');

    coursesContainer.empty();
    courses.forEach(course => {
      coursesContainer.append(`
        <div class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
          <h3 class="text-lg font-semibold mb-2">${course.title}</h3>
          <p class="text-sm text-gray-600">Course Code: ${course.code || 'N/A'}</p>
        </div>
      `);
    });
  };

  const getUserProfile = (userId, token) => {
    return $.ajax({
      url: '/api/accounts/students/' + userId + '/',
      type: 'GET',
      headers: {
        Authorization: 'Bearer ' + token
      },
      success: populateUserProfile,
      error: handleAjaxError
    });
  };

  const populateExams = (data) => {
      const exams = data.results;
      const examsContainer = $('.nonFinishedExams .exams');
  
      examsContainer.empty();
      exams.forEach(exam => {
          const currentDate = new Date();
          const startDate = new Date(exam.start_date);
          const endDate = new Date(exam.end_date);
          const isExamActive = currentDate >= startDate && currentDate <= endDate;
  
          const examDiv = `
              <div class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow" exam_id="${exam.id}">
                  <div class="flex justify-between items-start mb-4">
                      <div>
                          <h3 class="text-lg font-semibold">${exam.title}</h3>
                          <p class="text-sm text-gray-600">Course: ${exam.course.title}</p>
                          <p class="text-xs text-gray-500">ID: ${exam.id}</p>
                      </div>
                      <div class="text-right">
                          <p class="text-sm font-semibold">Exam Score: ${exam.exam_score}</p>
                          <p class="text-xs text-gray-600">Start: ${startDate.toLocaleString()}</p>
                          <p class="text-xs text-gray-600">End: ${endDate.toLocaleString()}</p>
                      </div>
                  </div>
                  <p class="text-sm text-gray-600 mb-4">Instructor: ${exam.instructor.first_name} ${exam.instructor.second_name}</p>
                  <button type="button" class="start-exam w-full bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors ${isExamActive ? '' : 'opacity-50 cursor-not-allowed'}" exam_id="${exam.id}" ${isExamActive ? '' : 'disabled'}>
                      ${isExamActive ? 'Start Exam' : 'Exam is not active'}
                  </button>
              </div>
          `;
      examsContainer.append(examDiv);

      setTimeout(() => {
        // Disable the start button if the current date is less than the start date
        const startDate = new Date(exam.start_date);
        const endDate = new Date(exam.end_date);
        const now = new Date();
        if (now > startDate && now < endDate) {
          $(`button.start-exam[exam_id="${exam.id}"]`).prop('disabled', false);
        } else {
          $(`button.start-exam[exam_id="${exam.id}"]`).prop('disabled', true).text('Exam is over');
        }
      }, 0);

      // Add a click event listener to the start-exam button
      $(`button.start-exam[exam_id="${exam.id}"]`).click(function () {
        // Check if the button is not disabled
        if (!$(this).prop('disabled')) {
          // Navigate to the exam page
          window.location.href = `/exams?exam_id=${exam.id}&exam_title=${exam.title}`;
        }
      });
    });
  };

  const getExams = (token) => {
    $.ajax({
      url: '/api/exams/',
      type: 'GET',
      headers: {
        Authorization: 'Bearer ' + token
      },
      success: populateExams,
      error: handleAjaxError
    });
  };

  const populateFinishedExams = (data) => {
    const results = data.results;
    const examsContainer = $('.finishedExams .exams');

    examsContainer.empty();
    results.forEach(result => {
      const resultDiv = `
        <div class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-lg font-semibold">${result.exam.title}</h3>
              <p class="text-sm text-gray-600">Course: ${result.exam.course_title}</p>
              <p class="text-xs text-gray-500">ID: ${result.exam.id}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold">Exam Score: ${result.exam.exam_score}</p>
              <p class="text-sm font-semibold text-green-600">Your Score: ${result.score}</p>
              <p class="text-xs text-gray-600">Start: ${new Date(result.exam.start_date).toLocaleString()}</p>
              <p class="text-xs text-gray-600">End: ${new Date(result.exam.end_date).toLocaleString()}</p>
            </div>
          </div>
          <p class="text-sm text-gray-600">Instructor: ${result.instructor.first_name} ${result.instructor.second_name}</p>
        </div>`;
      examsContainer.append(resultDiv);
    });
  };

  const getFinishedExams = (username, token) => {
    $.ajax({
      url: `/api/exams/results/?student_name=${username}`,
      type: 'GET',
      headers: {
        Authorization: 'Bearer ' + token
      },
      success: populateFinishedExams,
      error: handleAjaxError
    });
  };

  // Call getFinishedExams after getUserProfile
  getUserProfile(userId, token).done((data) => {
    getFinishedExams(data.username, token);
  });
  getExams(token);
});
