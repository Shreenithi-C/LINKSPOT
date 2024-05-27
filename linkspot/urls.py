"""
URL configuration for linkspot project.

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
from supply.views import supply,home,user_page,restaurant_page,accept_request,check_notification,reject_request,navigate
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('supply/', supply, name='supply'),
    path('home/',home,name='home'),
    path('user/', user_page, name='user_page'),
    path('restaurant/', restaurant_page, name='restaurant_page'),
    path('accept/<int:request_id>/', accept_request, name='accept_request'),
    path('reject/<int:request_id>/', reject_request, name='reject_request'),
    path('check_notification/', check_notification, name='check_notification'),
    path('navigate/',navigate,name = 'navigate')
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
