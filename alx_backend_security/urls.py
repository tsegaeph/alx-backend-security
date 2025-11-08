from django.contrib import admin
from django.urls import path
from ip_tracking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
]
