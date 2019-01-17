from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import json
from main.models import Author


class Command(BaseCommand):
    help = '''add authors from json file in directory (in BASE_DIR) to DB'''

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, *args, **options):
        authors_dir = options['directory']
        path = os.path.join(settings.BASE_DIR, authors_dir, 'authors.json')

        with open(path, 'r') as f:
            authors = json.load(f)

            for item in authors:
                author = Author(
                    name=item['name'],
                    lastname=item['lastname']
                )
                author.save()
