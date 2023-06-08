from django.urls import path
from users.views import(UserSignupView, UserListView,
                        VerifyEmail, UserLoginView, 
                        RefreshTokenView, ConfigureUserView,
                        ChangePasswordView)

urlpatterns = [
    path('signup/', UserSignupView.as_view()),
    path('list_users/', UserListView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('configure_users/', ConfigureUserView.as_view()),
    path('change_password/', ChangePasswordView.as_view())
]