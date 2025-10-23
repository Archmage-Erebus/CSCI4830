from django.db import models
from django.utils import timezone

# Create your models here.
class Budget(models.Model):
    goal = models.DecimalField(max_digits=9,decimal_places=2)
    balance = models.DecimalField(max_digits=9,decimal_places=2,default=0)
    start = models.DateField(default=timezone.now, help_text = "Use the format <em>YYYY-MM-DD</em> for dates")
    end = models.DateField()

    # Updates balance for budget
    def updateBalance(self, add=0, deduct=0):
        self.balance += add
        self.balance -= deduct
        self.save()

class Transaction(models.Model):
    name = models.CharField(max_length=100, help_text = "Provide a short descriptor")
    amount = models.DecimalField(max_digits=9, decimal_places=2, help_text = "Enter in profit or expense")
    timestamp = models.DateTimeField(default=timezone.now, help_text = "Use the format <em>YYYY-MM-DD</em> for dates")
    tag = models.CharField(max_length=20, blank=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self): 
        return self.name