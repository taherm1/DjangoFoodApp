# Generated by Django 2.2.7 on 2019-12-03 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FoodApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('ready-to-eat', 'Ready to Eat'), ('ready-to-cook', 'Ready to Cook'), ('ready-to-drink', 'Ready to Drink')], max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
