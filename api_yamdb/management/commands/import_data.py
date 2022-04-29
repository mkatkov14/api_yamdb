import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, genre_title


class Command(BaseCommand):
    def handle(self, *args, **options):
        with(os.join.path(settings.BASE_DIR / 'titles.csv'), 'r') as f:
            csv_reader = csv.reader('titles.csv', delimiter=',')
            for row in csv_reader:
                Title.objects.create(name=row[1], year=row[2], category=row[3])
