# Generated by Django 3.0.5 on 2020-05-26 16:54

from django.db import migrations


CURRENCIES = [('CLP', 'Chilean Peso'),
              ('UF', 'Unidad de Fomento'),
              ('EUR', 'Euro'),
              ('GBP', 'Pound Sterling'),
              ('USD', 'US Dollar'),
              ('PLV_A', 'Planvital Multifondo A'),
              ('PLV_B', 'Planvital Multifondo B'),
              ('PLV_C', 'Planvital Multifondo C'),
              ('PLV_D', 'Planvital Multifondo D'),
              ('PLV_E', 'Planvital Multifondo E'),
              ]


def add_currencies(apps, schema_editor):
    Currency = apps.get_model('backend', 'Currency')
    for elem in CURRENCIES:
        print(elem)
        Currency.objects.get_or_create(code=elem[0], name=elem[1])


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20200526_1653'),
    ]

    operations = [
        migrations.RunPython(add_currencies),
    ]
