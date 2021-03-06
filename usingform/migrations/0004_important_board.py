# Generated by Django 3.0.6 on 2020-06-18 08:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usingform', '0003_auto_20200614_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Important_board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('important', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usingform.Defaultform')),
            ],
            options={
                'ordering': ['-important'],
            },
        ),
    ]
