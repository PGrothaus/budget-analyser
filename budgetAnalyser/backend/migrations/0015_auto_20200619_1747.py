# Generated by Django 3.0.5 on 2020-06-19 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_auto_20200616_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networth',
            name='type',
            field=models.CharField(default='networth', max_length=40),
        ),
    ]
