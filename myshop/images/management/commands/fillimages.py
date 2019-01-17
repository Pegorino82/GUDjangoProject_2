from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
from shutil import copy2
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

        path = os.path.join(settings.BASE_DIR, imgs_dir)
        file_list = os.listdir(path)

        if options['del']:
            confirm = input('do you want to delete all images, including in media directory? y/n ')
            if confirm.lower() == 'y':
                Image.objects.all().delete()
                medai_path = os.path.join(settings.BASE_DIR, 'media')
                media_file_list = os.listdir(medai_path)
                for f in media_file_list:
                    if os.path.isfile(os.path.join(medai_path, f)):
                        os.remove(medai_path, f)

        for d in file_list:
            for f in os.listdir(os.path.join(path, d)):
                if f.endswith(img_formats):
                    image = Image(
                        name=d + '_' + f,
                        img=f
                    )
                    image.save()
                    copy2(os.path.join(path, d, f), os.path.join(settings.BASE_DIR, 'media'))
