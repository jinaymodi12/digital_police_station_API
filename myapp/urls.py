from django.contrib import admin
from django.urls import path,include
from .views import*

urlpatterns = [
    path('registration/',registrationViews.as_view()),
    path('login/',loginViews.as_view()),
    path('create-complain/',createcomplainViews.as_view()),
    path('list-complain/',listcomplainViews.as_view()),
    path('view-complain/',viewcomplainViews.as_view()),
    path('add-police/<int:pk>',AddpoliceViews.as_view()),
    path('add-station/',AddstationViews.as_view()),
    path('assign-complain/<int:pk>',AssigncomplainViews.as_view()),
    path('add-criminal/<int:pk>',addcrimialViews.as_view()),
    path('search/',searchViews.as_view()),




]