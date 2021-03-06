# Generated by Django 2.1.1 on 2018-10-06 12:46

from django.db import migrations

import os
import datetime
from myshop.settings import BASE_DIR


def add_author(apps, schema_editor):
    author = apps.get_model('main', 'Author')
    author.objects.create(name='Jack', lastname='Black')
    author.objects.create(name='Mary', lastname='Contrary')


def add_main_content(apps, schema_editor):
    authors = apps.get_model('main', 'Author')
    mpcontent = apps.get_model('main', 'MainPageContent')
    url = os.path.join(BASE_DIR, 'tempDB')
    txt_files = [f for f in os.listdir(url) if f.endswith('.txt')]

    for txt_file in txt_files:
        with open(os.path.join(BASE_DIR, 'tempDB', txt_file), 'r') as file:
            f = list(map(lambda x: x.strip(), file.readlines()))

            if f[0] == '<main>':
                name = f[1].split()[0]
                lastname = f[1].split()[1]
                dt = f[2].split()[0].split('.') + f[2].split()[1].split(':')
                date = datetime.datetime(year=int(dt[2]),
                                         month=int(dt[1]),
                                         day=int(dt[0]),
                                         hour=int(dt[3], ),
                                         minute=int(dt[4])
                                         )
                chapter = f[3]
                content = f[4]
                mpcontent.objects.create(
                    chapter=chapter,
                    content=content,
                    date=date,
                    author=authors.objects.filter(name=name, lastname=lastname)[0]
                )

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_author,
            lambda x, y: (x, y)
        ),
        migrations.RunPython(
            add_main_content,
            lambda x, y: (x, y)
        )
    ]

