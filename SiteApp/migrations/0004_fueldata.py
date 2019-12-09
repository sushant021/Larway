# Generated by Django 2.2.3 on 2019-12-08 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteApp', '0003_auto_20191208_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surcharge_percentage', models.FloatField(blank=True, default=0.0)),
                ('surcharge_dollar', models.FloatField(blank=True, default=0.0)),
                ('miles', models.FloatField(blank=True, default=0.0)),
                ('rate_per_mile', models.FloatField(blank=True, default=0.0)),
                ('surcharge_amount', models.FloatField(blank=True, default=0.0)),
                ('linehaul_amount', models.FloatField(blank=True, default=0.0)),
                ('total_amount', models.FloatField(blank=True, default=0.0)),
            ],
        ),
    ]