"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from main.views import *
from django.views.static import serve
from mysite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexHandler),
    path('overhead/overheadAdd/<int:us_id>/', overheadAddHandler),
    path('overhead/', overheadHandler),
    path('overhead/<int:overhead_id>/', overheadInfoHandler, name="overheadInfoHandler"),
    path('login/', loginHandler),
    path('logout/', logoutHandler),
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    })
]
