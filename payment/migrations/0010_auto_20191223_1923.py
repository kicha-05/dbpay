# Generated by Django 3.0 on 2019-12-23 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20191223_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ManyToManyField(to='payment.UserProfile'),
        ),
    ]
