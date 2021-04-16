from django.db import models
from django.contrib.auth.models import User


class Bills(models.Model):
    customer_name = models.CharField(max_length=50)
    product = models.CharField(max_length=50)
    amount_due = models.FloatField()
    bill_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Customer: {}, Product: {}, Amount: {}".format(self.customer_name, self.product, self.amount_due)
