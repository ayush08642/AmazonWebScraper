# Generated by Django 3.2.5 on 2021-08-01 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serve', '0007_alter_scraped_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fastscraped',
            name='categories',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='fastscraped',
            name='names',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
