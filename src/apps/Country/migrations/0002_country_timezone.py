# Generated by Django 4.2.6 on 2024-01-17 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Country', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='timezone',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
