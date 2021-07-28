from os import name
from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib import admin

from tervtarapp import views

admin.site.site_header = "Tervtár adminisztrációs felület"
admin.site.site_title = "Tervtár adminisztráció"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homePageView, name="home"),
    path('home/', TemplateView.as_view(template_name='homepage.html'), name='home'),
    path('bejelentkezes/', views.signin, name="signin"),
    path('kijelentkezes/', views.logout_req, name="logout"),
    path('mappa/', views.folderlist, name="folder"),
    path('jelszocsere/', views.changepassword, name="pwdch"),
    path('allomas/', views.addallomas, name="addallomas"),
    path('vonal/', views.addvonal, name="addvonal"),
]
