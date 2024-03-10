from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.pythonvssunday.companies.serializers import CompanySerializer
from api.pythonvssunday.companies.models import Company
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.request import Request
from django.conf import settings


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination


@api_view(http_method_names=["POST"])
def send_company_email(request: Request):
    send_mail(
        subject=request.data.get("subject"),
        message=request.data.get("subject"),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
    )
    return Response({"status": "success", "message": "email sent successfully"})
