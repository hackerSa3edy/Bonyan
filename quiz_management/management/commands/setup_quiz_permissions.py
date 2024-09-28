from django.core.management.base import BaseCommand
from quiz_management.permissions.utils import create_quiz_permissions

class Command(BaseCommand):
    """
    Django management command to set up quiz permissions and groups.

    This command calls the `create_quiz_permissions` utility function to create
    the necessary permissions and groups for managing quizzes.

    Attributes:
        help (str): The help text for the command.
    """

    help = 'Sets up quiz permissions and groups'

    def handle(self, *args, **options):
        """
        The logic of the command.

        This method is called when the command is run. It calls the
        `create_quiz_permissions` function and outputs a success message.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.
        """
        create_quiz_permissions()
        self.stdout.write(self.style.SUCCESS('Successfully set up quiz permissions and groups'))