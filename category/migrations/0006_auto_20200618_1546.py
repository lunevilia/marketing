# Generated by Django 3.0.6 on 2020-06-18 06:46

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_auto_20200618_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default='', max_length=18),
        ),
    ]
