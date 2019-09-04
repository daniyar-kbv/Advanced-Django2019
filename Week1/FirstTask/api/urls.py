from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from .views import ReviewListCreate, CompanyList, ReviewSubmissions

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('review/', ReviewListCreate.as_view()),
    path('company/', CompanyList.as_view()),
    path('review_submissions/', ReviewSubmissions.as_view())
]
