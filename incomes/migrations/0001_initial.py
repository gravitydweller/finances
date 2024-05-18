# Generated by Django 4.2.9 on 2024-05-18 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(blank=True, choices=[('Salary', 'Salary'), ('Regres', 'Regres'), ('Freelance work', 'Freelance work'), ('Loan', 'Loan'), ('Gift', 'Gift')], max_length=50, null=True)),
                ('amount', models.FloatField()),
                ('description', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('date', models.DateField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='incomes/attachments/')),
                ('allocated', models.BooleanField(default=False)),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='incomes.employer')),
            ],
        ),
    ]
