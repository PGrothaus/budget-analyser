# Generated by Django 3.0.5 on 2020-05-26 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0003_auto_20200506_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('valued_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('valued_at', models.DateTimeField()),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchangerate_origin', to='backend.Currency')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchangerate_target', to='backend.Currency')),
            ],
        ),
        migrations.AddConstraint(
            model_name='currency',
            constraint=models.UniqueConstraint(fields=('code',), name='unique_currency_code'),
        ),
        migrations.AddConstraint(
            model_name='currency',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_currency_name'),
        ),
        migrations.AddField(
            model_name='accountvalue',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Account'),
        ),
        migrations.AddField(
            model_name='accountvalue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='exchangerate',
            index=models.Index(fields=['origin', 'target', '-valued_at'], name='backend_exc_origin__c74149_idx'),
        ),
        migrations.AddIndex(
            model_name='accountvalue',
            index=models.Index(fields=['account', '-valued_at'], name='backend_acc_account_b31d9d_idx'),
        ),
    ]
