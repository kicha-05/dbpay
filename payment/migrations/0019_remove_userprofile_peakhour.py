# Generated by Django 3.0 on 2020-01-02 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0018_delete_prevorder2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='peakhour',
        ),
    ]
