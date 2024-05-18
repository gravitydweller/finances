# Generated by Django 4.2.9 on 2024-05-18 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('current_balance', models.FloatField()),
                ('allocated_procentage', models.FloatField()),
                ('allocated_fixed', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PoolTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('destination_pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_to', to='pools.pool')),
                ('source_pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_from', to='pools.pool')),
            ],
        ),
    ]
