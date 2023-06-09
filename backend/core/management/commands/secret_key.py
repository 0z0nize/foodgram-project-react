from colorama import Fore
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    """Утилита для создания секретного ключа."""

    help = 'Generates new SECRET_KEY'

    def handle(self, *args, **options) -> None:
        self.stdout.write(
            Fore.GREEN
            + '\nSECRET_KEY: \n'
            + Fore.MAGENTA
            + get_random_secret_key()
            + '\n\n'
        )
