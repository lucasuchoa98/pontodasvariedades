# Generated by Django 2.2 on 2020-06-02 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200602_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='adress',
            new_name='address',
        ),
    ]