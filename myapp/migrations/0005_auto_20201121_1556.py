# Generated by Django 3.1.3 on 2020-11-21 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20201019_1631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Student',
            new_name='student',
        ),
        migrations.AddField(
            model_name='course',
            name='num_reviews',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
