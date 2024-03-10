from api.pythonvssunday.companies.models import Company
from rest_framework import serializers

print("CompanySerializer Initalized")


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "company_status",
            "application_link",
            "last_update",
            "notes",
        ]
