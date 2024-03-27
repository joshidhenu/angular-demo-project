from django.urls import path
from account.views import UserRegistrationView, VerifyEmailView, UserLoginView, UserDataView, AllUserDataView, UserUpdateDetailsView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordRestView,  UserDeleteView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify/<str:uidb64>/<str:token>/',
         VerifyEmailView.as_view(), name='verify_email'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('dataview/', UserDataView.as_view(),
         name='UserDataViewSerializer'),
    path('alluserdataview/', AllUserDataView.as_view()),
    path('userupdatedetails/', UserUpdateDetailsView.as_view(),
         name='UserUpdateDetailsView'),
    path('changepassword/', UserChangePasswordView.as_view(),
         name='UserChangePasswordView'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(),
         name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordRestView.as_view()),
    path('userdelete/', UserDeleteView.as_view(), name='UserDeleteView'),
]
