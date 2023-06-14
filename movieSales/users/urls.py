from django.urls import path
from users.views import(ClientSignupView, EmployeeSignupView,
                        UserListView, UserLoginView, 
                        ConfigureUserView, ChangePasswordView)

urlpatterns = [
    path('signup_client/', ClientSignupView.as_view()),
    path('signup_employee/', EmployeeSignupView.as_view()),
    path('list_users/', UserListView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('configure_users/', ConfigureUserView.as_view()),
    path('change_password/', ChangePasswordView.as_view())
]