from django.urls import path
from django.contrib.auth import views as auth_views
from  .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.signup,name="signup"),
    path('login',views.signin,name="signin"),
    path('logout',views.handle_logout,name="logout"),
    path('bank_account',views.bank_account,name="bank_account"),
    path('credit_card_generator',views.credit_card_generator,name="credit_card_generator"),
    path('card_details',views.card_details,name="card_details"),
    path('otp_validation',views.otp_validation,name="otp_validation"),
    path('biometric_validation',views.biometric_validation,name="biometric_validation"),
    path('ml_card_transaction',views.ml_card_transaction,name="ml_card"),
    path('qr_transaction',views.qr_transaction,name="qr_code"),
    path('qr_activate',views.qr_activate,name="activate"),
    path('transaction_permission', views.yesno, name="permission"),
    path('transaction_permission_ok',views.yes,name="permission_ok"),
    path('transaction_permission_denied',views.no,name="permission_no"),




   ]