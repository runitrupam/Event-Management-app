"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.contrib import admin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

app_name = "eventrr"

urlpatterns = [
  #  path('', include('eventrr.urls')),

    path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('',views.index,name='index'), # shows all the events for a user (to book tickets) , and update , delete option only for superuser
    path('update/<int:id>',views.update,name='update'), # UPDATE an event
    path('delete/<int:id>',views.delete,name='delete'), # delete an event
    
    path('registeredEvents/',views.registeredEvents,name='registeredEvents') , # Registered Tickets 
    path('bookticket/<int:id>',views.book_ticket,name='bookticket'), # book  a ticket
    path('unbookticket/<int:id>',views.unbook_ticket,name='unbookticket'), # book  a ticket

    path('createuser/',views.create_user,name='createuser'),#for internal use
    path('listevents/',views.listevents,name='listevents'),# for internal use
    
    path("register/", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),

]
