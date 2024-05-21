# income/models.py

from django.db import models
from decimal import Decimal

INCOME_TAG_CHOICES =[
    ('Salary', 'Salary'),
    ('Regres', 'Regres'),
    ('Freelance work', 'Freelance work'),
    ('Loan', 'Loan'),
    ('Gift', 'Gift'),
]

class Employer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Income(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.SET_NULL, blank=True, null=True)
    tag = models.CharField(max_length=50, choices=INCOME_TAG_CHOICES,blank=True, null=True)
    amount = models.FloatField()
    description = models.CharField(max_length=200, default='', blank=True, null=True)
    date = models.DateField()
    attachment = models.FileField(upload_to='incomes/attachments/', blank=True, null=True)
    allocated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} from {self.employer}"
    
    