from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Sum
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from bootstrap_datepicker_plus import DatePickerInput
from .models import Bills


# Displaying All Bills on the Home Page
class BillListView(ListView):
    model = Bills
    context_object_name = 'bills'
    template_name = 'billingapp/home.html'
    paginate_by = 12

    def get_queryset(self):
        return (
            Bills
            .objects
            .filter(owner=self.request.user)
            .order_by('due_date')
        )

    def get_context_data(self, *args, **kwargs):
        data = super(BillListView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Home'
        return data


# Form to create a Bill
class BillCreateView(CreateView):
    model = Bills
    template_name = 'billingapp/create_bill.html'
    fields = ['customer_name', 'product', 'amount_due', 'due_date']
    success_url = reverse_lazy('site-home')

    def get_form(self, **kwargs):
        form = super().get_form()
        form.fields['due_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        data = super(BillCreateView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Create A Bill'
        return data


# Display Names of all customers in the Customers page
class CustomerListView(ListView):
    model = Bills
    context_object_name = 'bills'
    template_name = 'billingapp/customers.html'
    paginate_by = 12

    def get_queryset(self):
        return (
            Bills
            .objects
            .filter(owner=self.request.user)
            .order_by('customer_name')
            .values('customer_name')
            .distinct()
        )

    def get_context_data(self, *args, **kwargs):
        data = super(CustomerListView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Customers'
        return data


# Display entire bill of a Customer when clicked on Customers Page
class CustomerBillListView(ListView):
    model = Bills
    context_object_name = 'bills'
    template_name = 'billingapp/customer_bill.html'

    def get_queryset(self):
        return ({
            'bills': Bills
            .objects
            .filter(customer_name=self.kwargs.get('customer_name'))
            .filter(owner=self.request.user)
            .order_by('due_date'),
            'sum': Bills
            .objects
            .filter(customer_name=self.kwargs.get('customer_name'))
            .filter(owner=self.request.user)
            .aggregate(Sum('amount_due'))
        })

    def get_context_data(self, *args, **kwargs):
        data = super(CustomerBillListView, self).get_context_data(*args, **kwargs)
        data['title'] = self.kwargs.get('customer_name')
        return data


# A view developed to edit the Bills which are already created
class BillUpdateView(UserPassesTestMixin, UpdateView):
    model = Bills
    template_name = 'billingapp/create_bill.html'
    fields = ['customer_name', 'product', 'amount_due', 'due_date']
    success_url = reverse_lazy('site-home')

    def get_form(self, **kwargs):
        form = super().get_form()
        form.fields['due_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bill = self.get_object()
        return bill.owner == self.request.user

    def get_context_data(self, *args, **kwargs):
        data = super(BillUpdateView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Update Bill'
        return data


# A view created to Delete the Bill
class BillDeleteView(UserPassesTestMixin, DeleteView):
    model = Bills
    context_object_name = 'bill'
    template_name = 'billingapp/delete.html'
    success_url = '/'

    def test_func(self):
        bill = self.get_object()
        return bill.owner == self.request.user


# About Page View
def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'billingapp/about.html', context)
