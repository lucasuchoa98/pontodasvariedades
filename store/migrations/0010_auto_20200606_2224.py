# Generated by Django 2.2 on 2020-06-07 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20200605_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Bo', 'Bolsas'), ('Ci', 'Cintos'), ('Ca', 'Carteiras'), ('Av', 'Escolar'), ('Ar', 'Armarinho'), ('Br', 'Briquedos')], max_length=2),
        ),
    ]