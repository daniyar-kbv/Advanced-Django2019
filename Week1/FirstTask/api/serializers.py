from rest_framework import serializers
from .models import Review, Company
from django.contrib.auth.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CompanyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ReviewModelSerializer(serializers.ModelSerializer):
    company = CompanyModelSerializer
    reviewer = UserModelSerializer

    class Meta:
        model = Review
        fields = '__all__'
