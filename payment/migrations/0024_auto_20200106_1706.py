# Generated by Django 3.0 on 2020-01-06 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0023_dummy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dummy',
            old_name='name',
            new_name='label',
        ),
    ]
