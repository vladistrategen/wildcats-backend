from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = 'Runs a health check to ensure that Django can run'

    def handle(self, *args, **options):
        try:
            # Check database connections
            for connection in connections.all():
                connection.cursor()
            self.stdout.write(self.style.SUCCESS('Django is ready.'))
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f'Django is not ready: {str(e)}'))
            exit(1)
