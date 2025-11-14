from django.db import models
from django.utils import timezone

USER_ROLES = {
    "CUSTOMER": "CUSTOMER",
    "ADMIN": "ADMIN",
    "BANKER": "BANKER",
}
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField()
    password = models.CharField()
    firstname = models.CharField()
    lastname = models.CharField()
    phone = models.CharField()
    dateOfBirth = models.DateField()
    role = models.CharField(choices=USER_ROLES)
    isActive = models.BooleanField(default=True)
    createdBy = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

ACCOUNT_TYPES = {
    "CHECKING": "CHECKING",
    "SAVINGS": "SAVINGS",
    "BUSINESS": "BUSINESS",
}

class Account(models.Model):
    account_number = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=19,decimal_places=2)
    isActive = models.BooleanField(default=True)
    createdBy = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

FRAUD_STATUS = {
    "PENDING": "PENDING",
    "APPROVED": "APPROVED",
    "FLAGGED": "FLAGGED",
    "BLOCKED": "BLOCKED",
    "UNDER_REVIEW": "UNDER_REVIEW",
}

TRANSACTION_TYPE = {
    "DEPOSIT": "DEPOSIT",
    "WITHDRAWAL": "WITHDRAWAL",
    "TRANSFER_OUT": "TRANSFER_OUT",
    "TRANSFER_IN": "TRANSFER_IN",
    "PURCHASE": "PURCHASE",
    "REFUND": "REFUND",
    "FEE": "FEE",
}

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=19,decimal_places=2)
    description = models.CharField(blank=True, null=True)
    merchant_name = models.CharField(blank=True, null=True)
    merchant_category = models.CharField(blank=True, null=True)
    location = models.CharField(blank=True, null=True)
    ipAddress = models.CharField(blank=True, null=True)
    deviceFingerprint = models.CharField(blank=True, null=True)
    fraud_status = models.CharField(choices=FRAUD_STATUS, default="PENDING")
    fraud_score = models.FloatField(blank=True, null=True)
    fraud_reason = models.CharField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)