# Generated by Django 2.2 on 2020-06-13 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_db', '0002_auto_20200613_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='photo',
            field=models.ImageField(null=True, upload_to=None),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='rating',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
