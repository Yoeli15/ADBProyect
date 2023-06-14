from django.urls import path
from address.views import AddressView, ConfigureAddressView

urlpatterns =[
    path('addresses/', AddressView.as_view()),
    path('configure_addresses/', ConfigureAddressView.as_view())
]