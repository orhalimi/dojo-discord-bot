# Generated by Django 4.0.3 on 2022-09-08 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_create_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscribed',
            field=models.BooleanField(default=True),
        ),
    ]