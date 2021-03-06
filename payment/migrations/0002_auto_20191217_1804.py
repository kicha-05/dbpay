# Generated by Django 3.0 on 2019-12-17 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='payment.UserProfile')),
                ('item', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='CartModel',
        ),
    ]
