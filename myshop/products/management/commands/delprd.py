from django.core.management.base import BaseCommand, CommandError

from products.models import Product


class Command(BaseCommand):
    help = '''delete product by product_id.
    if --all delete all products'''

    def add_arguments(self, parser):
        parser.add_argument('product_id', nargs='*', type=int)
        parser.add_argument('--all', action='store_true')

    def handle(self, *args, **options):
        if options['all']:
            confirm = input('do you want to delete all products? y/n ')
            if confirm.lower() == 'y':
                Product.objects.all().delete()
        else:
            for product_id in options['product_id']:
                try:
                    Product.objects.get(id=product_id).delete()
                except Exception as err:
                    print(f'Exception: {err}')
