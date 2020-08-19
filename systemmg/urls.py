"""systemmg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from sysmg import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('index/', views.index),
    path('register/', views.register),
    path('logout/', views.logout),
    path('machlist/', views.machlist),
    path('machadd/', views.machadd),
    path('useradd/', views.useradd),
    path('userlist/', views.userlist),
    path('useredit/<int:user_id>/', views.useredit, name='useredit'),
    path('userdel/<int:user_id>/', views.userdel, name='userdel'),
    # path('captcha/', include('captcha.urls')),
    path('machdetail/<int:mach_id>/', views.machdetail, name='machdetail'),
    path('machedit/<int:mach_id>/', views.machedit, name='machedit'),
    path('machdel/<int:mach_id>/', views.machdel, name='machdel'),
    path('operationlog/', views.operationlog),
    path('excelin/', views.excelin),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
