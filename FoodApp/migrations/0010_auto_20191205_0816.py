# Generated by Django 2.2.7 on 2019-12-05 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodApp', '0009_auto_20191205_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.CharField(max_length=255),
        ),
    ]
