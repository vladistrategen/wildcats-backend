# Generated by Django 4.2.6 on 2023-11-21 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlightData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airline', models.CharField(max_length=100)),
                ('origin', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('flight_number', models.CharField(max_length=100)),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('arrival_date', models.DateField()),
                ('arrival_time', models.TimeField()),
                ('duration', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
