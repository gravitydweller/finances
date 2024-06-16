# loans/views.py

from django.shortcuts import render
from django.db.models import Sum
from .models import Loan
from expenses.models import Expense, ExpenseTag

def loans_home(request):
    loans = Loan.objects.all()

    # Calculate progress for each loan
    loan_progress = []
    for loan in loans:
        # Get the associated expense tag
        loan_tag_name = f"Loan: {loan.name}"
        loan_tag = ExpenseTag.objects.filter(name=loan_tag_name).first()
        
        if loan_tag:
            # Aggregate the total paid amount using Django's aggregation function
            total_paid = Expense.objects.filter(tag=loan_tag).aggregate(total=Sum('amount'))['total'] or 0
        else:
            total_paid = 0
        
        remaining_amount = loan.amount - total_paid
        loan_progress.append({
            'loan': loan,
            'total_paid': total_paid,
            'remaining_amount': remaining_amount,
        })

    return render(request, 'loans/loans_home.html', {
        'loans': loans,
        'loan_progress': loan_progress
    })