# Generated by Django 5.1.4 on 2024-12-27 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0002_coldwater_electricity_gas_hotwater_rent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rent',
            options={'ordering': ('-payment_date',), 'verbose_name': 'Жировка', 'verbose_name_plural': 'Жировки'},
        ),
    ]
