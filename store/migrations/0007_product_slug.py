# Generated by Django 2.2 on 2020-06-03 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20200602_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]