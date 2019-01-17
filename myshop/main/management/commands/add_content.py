from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import json
import random
from main.models import MainPageContent, Author


class Command(BaseCommand):
    help = '''add authors from json file in directory (in BASE_DIR) to DB'''

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, *args, **options):
        content_dir = options['directory']
        path = os.path.join(settings.BASE_DIR, content_dir, 'content.json')

        authors = Author.objects.all()

        with open(path, 'r') as f:
            content = json.load(f)

            for item in content:
                author = random.choice(authors)
                article = MainPageContent(
                    chapter=item['chapter'],
                    content=item['content'],
                    author=author
                )
                article.save()
