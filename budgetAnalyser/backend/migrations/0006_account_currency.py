# Generated by Django 3.0.5 on 2020-05-26 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20200526_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backend.Currency'),
        ),
    ]
