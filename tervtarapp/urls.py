from django.urls import path
from tervtarapp import views

urlpatterns = [
    path('bejelentkezes/', views.signin, name="signin"),
]