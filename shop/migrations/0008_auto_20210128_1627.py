# Generated by Django 3.1.5 on 2021-01-28 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210128_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(default=0, max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(default=0, max_length=10),
        ),
    ]