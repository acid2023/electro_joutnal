"""
URL configuration for s_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from network.views import login_view, logout_view, register, home, profile_view, users_view, edit_profile, login_is_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('login_required/', login_is_required, name='login_required'),
    path('register/', register, name='register'),
    path('', home, name='home'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('users/', users_view, name='users'),
    path('edit_profile/', edit_profile, name='edit_profile'),


]
