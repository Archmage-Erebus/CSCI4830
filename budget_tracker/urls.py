from django.urls import path
from budget_tracker import views

urlpatterns = [
    path('budgets', views.budget_view, name='budget_view'),
    path('budgets/edit/<int:budget_id>', views.edit_budget, name='edit_budget'),
    path('budgets/delete/<int:budget_id>', views.delete_budget, name='delete_budget'),
    path('transactions/<int:foreign_id>', views.trans_view, name='trans_view'),
    # path('transactions/add/<int:foreign_id>', views.add_trans, name='add_trans'),
    path('transactions/edit/<int:trans_id>', views.edit_trans, name='edit_trans'), 
    path('transactions/delete/<int:trans_id>', views.delete_trans, name='delete_trans'),
]