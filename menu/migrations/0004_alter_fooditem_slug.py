# Generated by Django 4.1 on 2022-09-14 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_category_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]
