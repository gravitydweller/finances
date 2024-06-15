# Generated by Django 4.2.9 on 2024-06-15 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('amount', models.FloatField()),
                ('duration_months', models.IntegerField()),
                ('start_date', models.DateTimeField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='loans/images/')),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoanExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_expenses', to='expenses.expense')),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='loans.loan')),
            ],
        ),
    ]
