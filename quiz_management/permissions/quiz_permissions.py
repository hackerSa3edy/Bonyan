from django.apps import apps

class QuizPermissionsMixin:
    """
    Mixin class to handle permissions for quiz-related actions.

    This mixin provides methods to check if a user has permissions to create, edit, delete, view, and take quizzes.
    """

    @classmethod
    def has_create_permission(cls, user):
        """
        Check if the user has permission to create a quiz.

        Args:
            user (User): The user to check permissions for.

        Returns:
            bool: True if the user has the 'quiz.create_quiz' permission, False otherwise.
        """
        return user.has_perm('quiz.create_quiz')

    def has_edit_permission(self, user):
        """
        Check if the user has permission to edit the quiz.

        Args:
            user (User): The user to check permissions for.

        Returns:
            bool: True if the user has the 'quiz.edit_quiz' permission and is the creator of the quiz, False otherwise.
        """
        return user.has_perm('quiz.edit_quiz') and self.creator == user

    def has_delete_permission(self, user):
        """
        Check if the user has permission to delete the quiz.

        Args:
            user (User): The user to check permissions for.

        Returns:
            bool: True if the user has the 'quiz.delete_quiz' permission and is the creator of the quiz, False otherwise.
        """
        return user.has_perm('quiz.delete_quiz') and self.creator == user

    def has_view_permission(self, user):
        """
        Check if the user has permission to view the quiz.

        Args:
            user (User): The user to check permissions for.

        Returns:
            bool: True if the user has the 'quiz.view_quiz' permission or if the quiz is published and the user has the 'quiz.take_quiz' permission, False otherwise.
        """
        return user.has_perm('quiz.view_quiz') or (self.is_published and user.has_perm('quiz.take_quiz'))

    def has_take_permission(self, user):
        """
        Check if the user has permission to take the quiz.

        Args:
            user (User): The user to check permissions for.

        Returns:
            bool: True if the user has the 'quiz.take_quiz' permission and the quiz is published or assigned to the user, False otherwise.
        """
        QuizAssignment = apps.get_model('quiz_management', 'QuizAssignment')
        return user.has_perm('quiz.take_quiz') and (self.is_published or QuizAssignment.objects.filter(quiz=self, user=user).exists())

class QuizAttemptPermissionsMixin:
    """
    Mixin class to handle permissions for quiz attempt-related actions.

    This mixin provides methods to check if a user has permissions to create, submit answers, and view results of quiz attempts.
    """

    @classmethod
    def has_create_permission(cls, user, quiz):
        """
        Check if the user has permission to create a quiz attempt.

        Args:
            user (User): The user to check permissions for.
            quiz (Quiz): The quiz to check permissions for.

        Returns:
            bool: True if the user has permission to take the quiz, False otherwise.
        """
        return quiz.has_take_permission(user)

    def has_submit_answer_permission(self, user):
        """
        Check if the user has permission to submit an answer for the quiz attempt.

        Args:
            user (User): The user to check permissions for.

        Returns:
            bool: True if the user is the owner of the quiz attempt and the attempt is not completed, False otherwise.
        """
        return self.user == user and not self.completed_at

    def has_view_result_permission(self, user):
        """
        Check if the user has permission to view the results of the quiz attempt.

        Args:
            user (User): The user to check permissions for.

        Returns:
            bool: True if the user is the owner of the quiz attempt, the attempt is completed, and the quiz shows results, False otherwise.
        """
        return self.user == user and self.completed_at and self.quiz.show_results
