# Generated by Django 3.0.5 on 2020-05-30 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0006_account_currency"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccountType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name="currency", name="code", field=models.CharField(max_length=10),
        ),
    ]
