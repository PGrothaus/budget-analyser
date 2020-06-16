# Generated by Django 3.0.5 on 2020-06-16 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20200615_0226'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='networth',
            name='backend_net_user_id_8236c0_idx',
        ),
        migrations.AddField(
            model_name='networth',
            name='type',
            field=models.CharField(default='networth', max_length=20),
        ),
        migrations.AddIndex(
            model_name='networth',
            index=models.Index(fields=['user_id', 'type', '-valued_at'], name='backend_net_user_id_3600d8_idx'),
        ),
    ]
