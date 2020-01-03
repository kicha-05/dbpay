# Generated by Django 3.0 on 2020-01-03 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0021_userprofile_hot_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
