
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'My custom command description'

    def handle(self, *args, **options):
        # Your custom command logic goes here
        self.stdout.write(self.style.SUCCESS('Custom command executed successfully'))
# https://t3rcio.com.br/en/playing-with-notify-command-postgresql-vol-1/