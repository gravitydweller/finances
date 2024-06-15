# loans/views.py

from django.shortcuts import render
from .models import Loan
from expenses.models import Expense, ExpenseTag

def loans_home(request):
    loans = Loan.objects.all()

    # Calculate progress for each loan
    loan_progress = []
    for loan in loans:
        # Query all expenses associated with the loan's expense tag
        loan_tag = ExpenseTag.objects.filter(name=f"Loan: {loan.name}").first()
        if loan_tag:
            loan_expenses = Expense.objects.filter(tag=loan_tag)
            total_paid = sum(expense.amount for expense in loan_expenses)
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