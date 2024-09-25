$(document).ready(function () {
  const token = document.cookie.replace(/(?:(?:^|.*;\s*)jwtAccess\s*=\s*([^;]*).*$)|^.*$/, '$1');
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace('-', '+').replace('_', '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

  const userId = JSON.parse(jsonPayload).user_id;

  let editMode = false;
  let currentExamId = null;
  let currentQuestionId = null;

  $('#exams-list').empty();
  function fetchCourses(instructorId) {
    $('#course-name').empty().append('<option value="">Select a course</option>');
    $.ajax({
      url: `/api/levels/courses/?instructor=${instructorId}`,
      method: 'GET',
      headers: { Authorization: 'Bearer ' + token },
      success: function (data) {
        data.results.forEach(function (course) {
          const option = $('<option>').val(course.id).text(course.title);
          $('#course-name').append(option);
        });
      },
      error: function (error) {
        console.error('Error fetching courses:', error);
        $('#exams-list').append('<p class="no-exams">No exams have been created yet.</p>'); // Update this line to add a class for styling
      }
    });
  }

  function fetchExams(userId) {
    $('#exams-list').empty();
    $.ajax({
      url: `/api/exams/?instructor_id=${userId}`,
      method: 'GET',
      headers: { Authorization: 'Bearer ' + token },
      success: function (data) {
        if (data.results.length === 0) {
          $('#exams-list').append('<p>No exams have been created yet.</p>');
        } else {
          data.results.forEach(function (exam) {
            appendExamToList(exam);
          });
        }
      },
      error: function (error) {
        console.error('Error fetching exams:', error);
        $('#exams-list').append(`<p class="text-red-500">Error: ${error.status} ${error.statusText}<br>Message: ${error.responseText}</p>`);
      }
    });
  }

  function appendExamToList(exam) {
    const examDiv = `
      <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow" data-exam-id="${exam.id}">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-lg font-semibold">${exam.title}</h3>
            <p class="text-sm text-gray-600">${exam.course.title}</p>
          </div>
          <div class="text-right">
            <p class="text-sm font-semibold">Exam Score: ${exam.exam_score}</p>
            <p class="text-xs text-gray-600">Start: ${formatDate(exam.start_date)}</p>
            <p class="text-xs text-gray-600">End: ${formatDate(exam.end_date)}</p>
          </div>
        </div>
        <p class="text-sm text-gray-600 mt-2">Instructor: ${exam.instructor.first_name} ${exam.instructor.second_name}</p>
        <div class="mt-4 space-x-2">
          <button class="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600 transition-colors edit_exam">Edit</button>
          <button class="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600 transition-colors delete_exam">Delete</button>
          <button class="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600 transition-colors manage_questions">Manage Questions</button>
        </div>
      </div>`;
    $('#exams-list').append(examDiv);
  }

  function formatDate(dateString) {
    return new Date(dateString).toLocaleString('en-US', { 
      timeZone: 'Africa/Cairo',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  function populateExamForm(exam) {
    $('#exam-title').val(exam.title);
    $('#course-name').val(exam.course.id);
    $('#start-date').val(formatDateTimeLocal(exam.start_date));
    $('#end-date').val(formatDateTimeLocal(exam.end_date));
    $('#exam-score').val(exam.exam_score);
  }

  function formatDateTimeLocal(dateString) {
    const date = new Date(dateString);
    return date.toISOString().slice(0, 16);
  }

  function clearExamForm() {
    $('#exam-form')[0].reset();
    editMode = false;
    currentExamId = null;
  }

  function showQuestionModal() {
    $('#question-modal').removeClass('hidden').addClass('flex');
  }

  function hideQuestionModal() {
    $('#question-modal').removeClass('flex').addClass('hidden');
    clearQuestionForm();
    currentQuestionPage = 1;
  }

  function clearQuestionForm() {
    $('#question-form')[0].reset();
    currentQuestionId = null;
    $('#submit-question').text('Add Question');
  }

  function populateQuestionForm(question) {
      clearQuestionForm();
      $('#question').val(question.text);
      currentQuestionId = question.id;
      question.choices.forEach((choice, index) => {
          const choiceInput = $(`#choice-${index + 1}`);
          choiceInput.val(choice.text);
          choiceInput.prop('checked', choice.is_correct);
          choiceInput.attr('data-choice-id', choice.id); // Append data-choice-id attribute
      });
      $('#submit-question').text('Update Question');
  }

  function fetchQuestions(examId) {
    $.ajax({
      url: `/api/exams/questions/?exam_id=${examId}`,
      method: 'GET',
      headers: { Authorization: 'Bearer ' + token },
      success: function(data) {
        displayQuestions(data);
      },
      error: function(error) {
        console.error('Error fetching questions:', error);
      }
    });
  }

  let currentQuestionPage = 1;
  const questionsPerPage = 2;

  function displayQuestions(questions) {
      const questionList = $('#question-list');
      questionList.empty();
      const start = (currentQuestionPage - 1) * questionsPerPage;
      const end = start + questionsPerPage;
      const paginatedQuestions = questions.results.slice(start, end);

      paginatedQuestions.forEach(function(question) {
          const questionItem = `
              <div class="border border-gray-200 rounded p-4 flex justify-between items-center" data-question-id="${question.id}">
                  <p class="flex-1">${question.text}</p>
                  <div>
                      <button class="text-blue-500 hover:text-blue-700 mr-2 edit-question">
                          <i class="fas fa-edit"></i> Edit
                      </button>
                      <button class="text-red-500 hover:text-red-700 delete-question">
                          <i class="fas fa-trash-alt"></i> Delete
                      </button>
                  </div>
              </div>
          `;
          questionList.append(questionItem);
      });

      $('#prev-question-page').prop('disabled', currentQuestionPage === 1);
      $('#next-question-page').prop('disabled', end >= questions.results.length);
      // Update question page info
      $('#question-page-info').text(`Page ${currentQuestionPage} of ${Math.ceil(questions.results.length / questionsPerPage)}`);
  }

  $('#prev-question-page').click(function() {
      if (currentQuestionPage > 1) {
          currentQuestionPage--;
          fetchQuestions(currentExamId);
      }
  });

  $('#next-question-page').click(function() {
      currentQuestionPage++;
      fetchQuestions(currentExamId);
  });

  function saveQuestion() {
      const questionData = {
          exam: currentExamId,
          text: $('#question').val(),
      };

      const choicesData = [1, 2, 3, 4]
          .map(i => ({
              id: $(`#choice-${i}`).attr('data-choice-id'), // Get the data-choice-id attribute value
              question: currentQuestionId,
              text: $(`#choice-${i}`).val(),
              is_correct: $(`#correct-${i}`).is(':checked')
          }))
          .filter(choice => choice.text.trim() !== '');

      const questionUrl = currentQuestionId ? `/api/exams/questions/${currentQuestionId}/` : '/api/exams/questions/';
      const questionMethod = currentQuestionId ? 'PUT' : 'POST';

      $.ajax({
          url: questionUrl,
          method: questionMethod,
          headers: { Authorization: 'Bearer ' + token },
          data: JSON.stringify(questionData),
          contentType: 'application/json',
          success: function(response) {
              const questionId = response.id || currentQuestionId;
              saveChoices(questionId, choicesData);
          },
          error: function(error) {
              console.error('Error saving question:', error);
          }
      });
  }
  
  function saveChoices(questionId, choicesData) {
      choicesData.forEach(choice => {
          const choiceUrl = choice.id ? `/api/exams/choices/${choice.id}/` : '/api/exams/choices/';
          const choiceMethod = choice.id ? 'PUT' : 'POST';
          choice.question = questionId;
  
          $.ajax({
              url: choiceUrl,
              method: choiceMethod,
              headers: { Authorization: 'Bearer ' + token },
              data: JSON.stringify(choice),
              contentType: 'application/json',
              success: function(response) {
                  fetchQuestions(currentExamId);
                  clearQuestionForm();
              },
              error: function(error) {
                  console.error('Error saving choice:', error);
              }
          });
      });
  }

  function deleteQuestion(questionId) {
    if (confirm('Are you sure you want to delete this question?')) {
      $.ajax({
        url: `/api/exams/questions/${questionId}/`,
        method: 'DELETE',
        headers: { Authorization: 'Bearer ' + token },
        success: function() {
          fetchQuestions(currentExamId);
        },
        error: function(error) {
          console.error('Error deleting question:', error);
        }
      });
    }
  }

  // Event Listeners
  $('#exams-list').on('click', '.manage_questions', function() {
    currentExamId = $(this).closest('[data-exam-id]').data('exam-id');
    fetchQuestions(currentExamId);
    showQuestionModal();
  });

  $('#question-list').on('click', '.edit-question', function() {
    const questionId = $(this).closest('[data-question-id]').data('question-id');
    $.ajax({
      url: `/api/exams/questions/${questionId}/`,
      method: 'GET',
      headers: { Authorization: 'Bearer ' + token },
      success: function(question) {
        populateQuestionForm(question);
      },
      error: function(error) {
        console.error('Error fetching question details:', error);
      }
    });
  });

  $('#question-list').on('click', '.delete-question', function() {
    const questionId = $(this).closest('[data-question-id]').data('question-id');
    deleteQuestion(questionId);
  });

  $('#submit-question').click(function(e) {
    e.preventDefault();
    saveQuestion();
  });

  $('#next-question').click(function(e) {
    e.preventDefault();
    saveQuestion();
    clearQuestionForm();
  });

  $('#close-question-form').click(hideQuestionModal);

  fetchExams(userId);
  fetchCourses(userId);

  const today = new Date().toISOString().slice(0, 16);
  $('#start-date, #end-date').attr('min', today);

  $('#submit-exam').click(function (e) {
    e.preventDefault();
    const examData = {
      title: $('#exam-title').val(),
      instructor: userId,
      start_date: $('#start-date').val(),
      end_date: $('#end-date').val(),
      course: $('#course-name').val(),
      exam_score: $('#exam-score').val()
    };

    const url = editMode ? `/api/exams/${currentExamId}/` : '/api/exams/';
    const method = editMode ? 'PUT' : 'POST';

    $.ajax({
      url: url,
      method: method,
      headers: { Authorization: 'Bearer ' + token },
      data: JSON.stringify(examData),
      contentType: 'application/json',
      success: function (response) {
        fetchExams(userId);
        clearExamForm();
      },
      error: function (error) {
        console.error('Error saving exam:', error);
      }
    });
  });

  $('#exams-list').on('click', '.edit_exam', function () {
    const examId = $(this).closest('[data-exam-id]').data('exam-id');
    currentExamId = examId;
    editMode = true;

    $.ajax({
      url: `/api/exams/${examId}/`,
      method: 'GET',
      headers: { Authorization: 'Bearer ' + token },
      success: function (exam) {
        populateExamForm(exam);
      },
      error: function (error) {
        console.error('Error fetching exam details:', error);
      }
    });
  });

  $('#exams-list').on('click', '.delete_exam', function () {
    const examId = $(this).closest('[data-exam-id]').data('exam-id');
    if (confirm('Are you sure you want to delete this exam?')) {
      $.ajax({
        url: `/api/exams/${examId}/`,
        method: 'DELETE',
        headers: { Authorization: 'Bearer ' + token },
        success: function () {
          fetchExams(userId);
        },
        error: function (error) {
          console.error('Error deleting exam:', error);
        }
      });
    }
  });
});