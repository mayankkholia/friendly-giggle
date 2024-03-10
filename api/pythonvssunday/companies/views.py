from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.pythonvssunday.companies.serializers import CompanySerializer
from api.pythonvssunday.companies.models import Company
from rest_framework.pagination import PageNumberPagination


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination
