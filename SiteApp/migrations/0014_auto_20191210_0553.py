# Generated by Django 2.2.3 on 2019-12-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteApp', '0013_auto_20191210_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='consignee',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='frieght_description',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='frieght_quantity',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='frieght_weight',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
