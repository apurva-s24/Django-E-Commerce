# Generated by Django 3.1.5 on 2021-01-28 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='zip_code',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
