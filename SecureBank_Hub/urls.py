from django.urls import path
from SecureBank_Hub import views

urlpatterns = [
    path('api/', views.hello, name="hello"),
    path('api/users/', views.UserListCreate.as_view(), name='user_list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('api/users/count/', views.user_count, name='user_count'),
    path('api/accounts/', views.AccountListCreate.as_view(), name='account_list'),
    path('api/accounts/<int:pk>/', views.AccountDetail.as_view(), name='account_detail'),
    path('api/accounts/user/<int:user_id>/',views.AccountListCreate.as_view(), name='account_by_user'),
    path('api/accounts/number/<str:account_number>/',views.AccountDetail.as_view(), name='account_by_number'),
    path('api/accounts/count/', views.account_count, name='account_count'),
    path('api/transactions/', views.TransactionListCreate.as_view(), name='transaction_list'),
    path('api/transactions/<int:pk>', views.TransactionDetail.as_view(), name='transaction_list'),
    path('api/transactions/account/<int:account_id>', views.TransactionListCreate.as_view(), name='transaction_by_account'),
    path('api/transactions/fraud/<str:fraud_status>', views.TransactionListCreate.as_view(), name='transaction_by_status'),
    path('api/transactions/high-risk/<threshold>', views.HighRiskTransactions, name='transaction_by_risk'),
    path('api/transactions/recent/<int:fk>', views.RecentTransactions, name='transaction_by_account'),
    path('api/transactions/count/', views.transaction_count, name='transaction_count'),
    # path('api/users', views.users_list, name="users_list"),
    # path('api/users/<int:user_id>', views.user_view, name="user")
]