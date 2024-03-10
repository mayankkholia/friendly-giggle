from django.db import models
from django.utils.timezone import now


# Create your models here.
class Company(models.Model):
    class CompanyStatus(models.TextChoices):
        HIRING = "HIRING"
        HIRING_FREEZE = "HIRING_FREEZE"
        LAYOFFS = "LAYOFFS"

    name = models.CharField(max_length=30, unique=True)
    company_status = models.CharField(
        choices=CompanyStatus, max_length=30, default=CompanyStatus.HIRING_FREEZE
    )
    last_update = models.DateTimeField(default=now, editable=True)
    application_link = models.URLField(blank=True)
    notes = models.TextField(max_length=100, blank=True)
