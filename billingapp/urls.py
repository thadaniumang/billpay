from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('create/', login_required(views.BillCreateView.as_view()), name='site-create'),
    path('bill/<int:pk>/update', login_required(views.BillUpdateView.as_view()), name='site-update'),
    path('bill/<int:pk>/delete', login_required(views.BillDeleteView.as_view()), name='site-delete'),
    path('customers/<str:customer_name>', login_required(views.CustomerBillListView.as_view()), name='site-invoice'),
    path('customers/', login_required(views.CustomerListView.as_view()), name='site-customers'),
    path('about/', views.about, name='site-about'),
    path('', login_required(views.BillListView.as_view()), name='site-home')
]
