from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Budget, Transaction
from .forms import BudgetForm, TransForm, FilterTrans
from datetime import timedelta, datetime

# Create your views here.
def budget_view(request):
    budgets = Budget.objects.all()

    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            newBudget = form.save(commit=False)
            if form.cleaned_data["duration"] == '0':
                newBudget.end = form.cleaned_data["custom"]
            else:
                newBudget.end = newBudget.start + timedelta(seconds=float(form.cleaned_data["duration"]))
            newBudget.save()
            return redirect('budget_view')
    else:
        form = BudgetForm()

    return render(request, 'budget_list.html', {'form': form, 'budgets': budgets})

def edit_budget(request, budget_id):
    return redirect('budget_view')

def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    budget.delete()
    return redirect('budget_view')

def trans_view(request, foreign_id):
    transactions = Transaction.objects.filter(budget_id=foreign_id)

    if request.method == "GET":
        form = TransForm(budget_id=foreign_id)
        filterT = FilterTrans(request.GET)
        if filterT.is_valid():
            tag = filterT.cleaned_data["tag"]
            search = filterT.cleaned_data["search"]
            match filterT.cleaned_data["filter_by"]:
                case "name":
                    transactions = transactions.filter(name__icontains=search)
                case "less":
                    transactions = transactions.filter(amount__lt=float(search))
                case "more":
                    transactions = transactions.filter(amount__gt=float(search))
                case "date":
                    transactions = transactions.filter(timestamp__icontains=search)
                case "tag":
                    transactions = transactions.filter(tag__iexact=tag)
    elif request.method == "POST":
        form = TransForm(request.POST,budget_id=foreign_id)
        filterT = FilterTrans()
        if form.is_valid():
            budget = get_object_or_404(Budget, id=foreign_id)
            budget.updateBalance(add=form.cleaned_data["amount"])
            form.save()
            return redirect('trans_view', foreign_id)
    else:
        form = TransForm(budget_id=foreign_id)
        filterT = FilterTrans()

    total = 0
    for x in transactions:
        total += x.amount
    
    return render(request, 'trans_list.html', {'form': form, 'filterT': filterT, 'transactions': transactions, 'total': total})

# Deprecated function
# def add_trans(request, foreign_id):
#     transactions = Transaction.objects.filter(budget_id=foreign_id)

#     if request.method == "POST":
#         form = TransForm(request.POST,budget_id=foreign_id)
#         if form.is_valid():
#             budget = get_object_or_404(Budget, id=foreign_id)
#             budget.updateBalance(add=form.cleaned_data["amount"])
#             form.save()
#             return redirect('trans_view', foreign_id)
#     else:
#         form = TransForm(budget_id=foreign_id)

#     return render(request, 'trans_add.html', {'form': form, 'transactions': transactions})

def edit_trans(request, trans_id):
    transaction = get_object_or_404(Transaction, id=trans_id)
    foreign_id = transaction.budget_id

    if request.method == "POST":
        oldAmount = transaction.amount
        form = TransForm(request.POST, instance=transaction)
        if form.is_valid():
            if (oldAmount != form.cleaned_data["amount"]):
                budget = get_object_or_404(Budget, id=foreign_id)
                budget.updateBalance(
                    add=form.cleaned_data["amount"],
                    deduct=oldAmount
                )
            form.save()
            return redirect('trans_view', foreign_id)
    else:
        form = TransForm(instance=transaction)
    
    return render(request, 'trans_edit.html', {'form': form, 'transaction': transaction})

def delete_trans(request, trans_id):
    transaction = get_object_or_404(Transaction, id=trans_id)
    foreign_id = transaction.budget_id
    budget = get_object_or_404(Budget, id=foreign_id)
    budget.updateBalance(deduct=transaction.amount)
    transaction.delete()
    return redirect('trans_view', foreign_id)