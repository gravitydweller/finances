# Generated by Django 4.2.9 on 2024-05-30 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='color',
            field=models.CharField(default='#FFFFFF', max_length=50),
        ),
    ]
