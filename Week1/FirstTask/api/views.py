from django.shortcuts import render
from rest_framework import generics
from .serializers import CompanyModelSerializer, ReviewModelSerializer, UserModelSerializer
from .models import Company, Review
from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


class ReviewSubmissions(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    permission_classes = (IsAdminUser, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_queryset(self):
        return Review.objects.all()


class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer

    def get_queryset(self):
        return Company.objects.all()


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Review.objects.reviews_by_user(self.request.user)

    def perform_create(self, serializer):
        try:
            company = Company.objects.get(id=self.request.data.get('company'))
        except Company.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        return serializer.save(reviewer=self.request.user,
                               company=company,
                               ip_address=self.request.META['REMOTE_ADDR'])
