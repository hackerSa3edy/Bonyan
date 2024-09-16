from django.core.management.base import BaseCommand
from quiz_management.permissions.utils import create_quiz_permissions

class Command(BaseCommand):
    help = 'Sets up quiz permissions and groups'

    def handle(self, *args, **options):
        create_quiz_permissions()
        self.stdout.write(self.style.SUCCESS('Successfully set up quiz permissions and groups'))