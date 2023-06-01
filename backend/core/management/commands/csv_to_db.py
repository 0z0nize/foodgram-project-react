import csv
import os.path

from colorama import Fore
from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Переносит данные из файла CSV в базу данных."""

    help = "Loads data from csv files"

    def handle(self, *args, **options) -> None:
        """Создает объекты Tag."""
        self.stdout.write(Fore.BLUE + 'Trying to load ingredients data')
        file_path = os.path.join(settings.DATA_ROOT, 'ingredients.csv')
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for name, unit in reader:
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit
                )
            self.stdout.write(
                Fore.GREEN + 'Ingredients data successfully uploaded'
            )
