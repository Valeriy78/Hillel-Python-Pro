# Generated by Django 3.2.14 on 2022-10-06 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0008_remove_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderreturn',
            name='customer',
        ),
    ]
