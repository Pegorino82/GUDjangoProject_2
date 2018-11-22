from django.core.management.base import BaseCommand, CommandError

from products.models import Category


class Command(BaseCommand):
    help = '''delete category by category_id.
    if --all delete all categories'''

    def add_arguments(self, parser):
        parser.add_argument('category_id', nargs='*', type=int)
        parser.add_argument('--all', action='store_true')

    def handle(self, *args, **options):
        if options['all']:
            confirm = input('do you want to delete all products? y/n ')
            if confirm.lower() == 'y':
                Category.objects.all().delete()
        else:
            for category_id in options['category_id']:
                try:
                    Category.objects.get(id=category_id).delete()
                except Exception as err:
                    print(f'Exception: {err}')
