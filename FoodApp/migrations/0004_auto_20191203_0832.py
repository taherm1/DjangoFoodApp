# Generated by Django 2.2.7 on 2019-12-03 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodApp', '0003_auto_20191203_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='image',
            field=models.FileField(default=None, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
    ]
