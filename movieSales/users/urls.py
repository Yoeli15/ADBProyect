from django.urls import path
from users.views import(ClientSignupView, EmployeeSignupView,
                        UserListView, UserLoginView, 
                        ConfigureUserView, ChangePasswordView)

urlpatterns = [
    path('signup_clients/', ClientSignupView.as_view()),
    path('signup_employees/', EmployeeSignupView.as_view()),
    path('list_users/', UserListView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('configure_users/', ConfigureUserView.as_view()),
    path('change_passwords/', ChangePasswordView.as_view())
]