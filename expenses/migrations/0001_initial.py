# Generated by Django 4.2.9 on 2024-05-18 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseChategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('source_pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.pool')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('bill_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('amount', models.FloatField()),
                ('description', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='expenses/attachments/')),
                ('chategory', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='expenses.expensechategory')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.expensetag')),
            ],
        ),
    ]