# loans/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Loan
from .forms import LoanForm
from expenses.models import Expense, ExpenseTag

def loans_home(request):
    loans = Loan.objects.all()

    # Calculate progress for each loan
    loan_progress = []
    for loan in loans:
        # Get the associated expense tag
        loan_tag_name = f"{loan.name} loan"
        loan_tag = ExpenseTag.objects.filter(name=loan_tag_name).first()

        start_date = loan.start_date
        end_date = loan.end_date
        
        if loan_tag:
            # Aggregate the total paid amount using Django's aggregation function
            total_paid = Expense.objects.filter(tag=loan_tag).aggregate(total=Sum('amount'))['total'] or 0
        else:
            total_paid = 0
        
        remaining_amount = loan.amount - total_paid
        procent_remaining_amount = (remaining_amount * 100) / loan.amount
        procent_total_paid = (total_paid * 100) / loan.amount

        # Calculate percentage paid
        if loan.amount > 0:
            percentage_paid = (1 - (remaining_amount / loan.amount)) * 100
        else:
            percentage_paid = 0
        
        loan_progress.append({
            'loan': loan,
            'amount': loan.amount,
            'total_paid': total_paid,
            'procent_total_paid': procent_total_paid,
            'remaining_amount': remaining_amount,
            'procent_remaining_amount':procent_remaining_amount,
            'percentage_paid': percentage_paid,
        })

    return render(request, 'loans/loans_home.html', {
        'loans': loans,
        'loan_progress': loan_progress
    })

def create_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('loans/loans_home.html')
    else:
        form = LoanForm()
    
    context = {
        'form': form,
    }
    return render(request, 'loans/loans_form.html', context)

def update_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        form = LoanForm(request.POST, request.FILES, instance=loan)
        if form.is_valid():
            form.save()
            return redirect('loans/loans_home.html')
    else:
        form = LoanForm(instance=loan)
    
    context = {
        'form': form,
        'loan': loan,
    }
    return render(request, 'loans/loans_form.html', context)