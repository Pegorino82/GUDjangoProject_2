from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
from images.models import Image


class Command(BaseCommand):
    help = '''add images from directory (in BASE_DIR) to DB
    --del to delete all images before upload'''

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)
        parser.add_argument('--del', action='store_true')

    def handle(self, *args, **options):
        img_formats = ('.jpg', '.jpeg', '.png')
        imgs_dir = options['directory']

        # path = os.path.join(settings.MEDIA_ROOT, imgs_dir)
        path = os.path.join(settings.BASE_DIR, imgs_dir)
        file_list = os.listdir(path)

        if options['del']:
            Image.objects.all().delete()

        for f in file_list:
            if f.endswith(img_formats):
                image = Image(
                    name=f,
                    img=f
                )
                image.save()
