from django.urls import path
from .import views
urlpatterns = [
    path('',views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path("resend-otp/", views.resend_otp, name="resend_otp"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('resend-reset-otp/', views.resend_reset_otp, name='resend_reset_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset-success/', views.reset_success, name='reset_success'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('features/', views.features, name='features'),
    path('about/', views.about, name='about'),
    path('loan/<int:id>/', views.loan_detail, name='loan_detail'),
    path('check-eligibility/', views.check_eligibility, name='check_eligibility'),
    path("logout/", views.logout_view, name="logout"),
]
