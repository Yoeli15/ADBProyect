from django.urls import path
from stores.views import StoreView, ConfigureStoreView, ListStoresView

urlpatterns =[
    path('stores/', StoreView.as_view()),
    path('configure_stores/', ConfigureStoreView.as_view()),
    path('list_stores/', ListStoresView.as_view())
]