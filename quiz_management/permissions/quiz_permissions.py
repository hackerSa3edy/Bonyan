from django.apps import apps

class QuizPermissionsMixin:
    @classmethod
    def has_create_permission(cls, user):
        return user.has_perm('quiz.create_quiz')

    def has_edit_permission(self, user):
        return user.has_perm('quiz.edit_quiz') and self.creator == user

    def has_delete_permission(self, user):
        return user.has_perm('quiz.delete_quiz') and self.creator == user

    def has_view_permission(self, user):
        return user.has_perm('quiz.view_quiz') or (self.is_published and user.has_perm('quiz.take_quiz'))

    def has_take_permission(self, user):
        QuizAssignment = apps.get_model('quiz_management', 'QuizAssignment')
        return user.has_perm('quiz.take_quiz') and (self.is_published or QuizAssignment.objects.filter(quiz=self, user=user).exists())

class QuizAttemptPermissionsMixin:
    @classmethod
    def has_create_permission(cls, user, quiz):
        return quiz.has_take_permission(user)

    def has_submit_answer_permission(self, user):
        return self.user == user and not self.completed_at

    def has_view_result_permission(self, user):
        return self.user == user and self.completed_at and self.quiz.show_results
