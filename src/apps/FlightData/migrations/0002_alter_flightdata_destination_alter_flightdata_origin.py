# Generated by Django 4.2.6 on 2023-11-23 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('City', '0002_alter_city_latitude_alter_city_longitude'),
        ('FlightData', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightdata',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='City.city'),
        ),
        migrations.AlterField(
            model_name='flightdata',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin', to='City.city'),
        ),
    ]
