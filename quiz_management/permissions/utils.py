from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ..models import Quiz, QuizAssignment
from question_management.models import Question
from quiz_participation.models import QuizAttempt, UserAnswer

def create_quiz_permissions():
    # Create groups
    creator_group, _ = Group.objects.get_or_create(name='Quiz Creator')
    resolver_group, _ = Group.objects.get_or_create(name='Quiz Resolver')

    # Define permissions for Quiz Creator
    quiz_content_type = ContentType.objects.get_for_model(Quiz)
    question_content_type = ContentType.objects.get_for_model(Question)
    quiz_assignment_content_type = ContentType.objects.get_for_model(QuizAssignment)

    creator_permissions = [
        Permission.objects.get_or_create(codename='create_quiz', name='Can create quiz', content_type=quiz_content_type)[0],
        Permission.objects.get_or_create(codename='edit_quiz', name='Can edit quiz', content_type=quiz_content_type)[0],
        Permission.objects.get_or_create(codename='delete_quiz', name='Can delete quiz', content_type=quiz_content_type)[0],
        Permission.objects.get_or_create(codename='view_quiz', name='Can view quiz', content_type=quiz_content_type)[0],
        Permission.objects.get_or_create(codename='create_question', name='Can create question', content_type=question_content_type)[0],
        Permission.objects.get_or_create(codename='edit_question', name='Can edit question', content_type=question_content_type)[0],
        Permission.objects.get_or_create(codename='delete_question', name='Can delete question', content_type=question_content_type)[0],
        Permission.objects.get_or_create(codename='assign_quiz', name='Can assign quiz', content_type=quiz_assignment_content_type)[0],
    ]

    # Define permissions for Quiz Resolver
    quiz_attempt_content_type = ContentType.objects.get_for_model(QuizAttempt)
    user_answer_content_type = ContentType.objects.get_for_model(UserAnswer)

    resolver_permissions = [
        Permission.objects.get_or_create(codename='take_quiz', name='Can take quiz', content_type=quiz_content_type)[0],
        Permission.objects.get_or_create(codename='view_quiz', name='Can view quiz', content_type=quiz_content_type)[0],
        Permission.objects.get_or_create(codename='create_quiz_attempt', name='Can create quiz attempt', content_type=quiz_attempt_content_type)[0],
        Permission.objects.get_or_create(codename='submit_answer', name='Can submit answer', content_type=user_answer_content_type)[0],
    ]

    # Assign permissions to groups
    creator_group.permissions.set(creator_permissions)
    resolver_group.permissions.set(resolver_permissions)