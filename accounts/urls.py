from django.urls import path


from . import views



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_acc, name='logout'),
    path('token/',views.token, name='token'),
    path('error/', views.error_page, name='error'),
    path('success/', views.success_page, name='success'),
    path('verify/<id>/', views.verify, name='verify'),
    path('forgot/', views.forget, name="forgot"),
    path('reset/<token>/', views.reset, name='reset_password'),
]
