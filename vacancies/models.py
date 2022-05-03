from tabnanny import verbose

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from dopomoga2.models import TimestampedModel
from localflavor.nl.models import NLZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


class Company(TimestampedModel):
    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Companies"


class CompanyLocation(TimestampedModel):
    company = models.ForeignKey("vacancies.Company", blank=False, null=False, on_delete=models.CASCADE)

    zipcode = NLZipCodeField()
    street_number = models.CharField(max_length=10)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = CountryField(default="NL")

    class Meta:
        verbose_name_plural = "Company Locations"

    def __str__(self) -> str:
        return f"{self.company.name} - {self.city} ({self.street})"


class Vacancy(TimestampedModel):
    title = models.CharField(max_length=200, blank=False, null=False)
    spots_available = models.PositiveSmallIntegerField(default=1)
    spots_filled = models.PositiveSmallIntegerField(default=0)

    location = models.ForeignKey("vacancies.CompanyLocation", blank=False, null=False, on_delete=models.CASCADE)

    responsibilities = models.TextField()
    working_hours = models.CharField(max_length=200, blank=False, null=False)
    working_days = models.CharField(max_length=200, blank=False, null=False)
    hours_per_week = models.PositiveSmallIntegerField(default=40)
    salary_per_hour = MoneyField(max_digits=6, decimal_places=2, default_currency="EUR")
    start_date = models.DateField(help_text="Empty start date means ASAP.", blank=True, null=True)
    transport = models.CharField(max_length=200, blank=False, null=False)

    contact_name = models.CharField(max_length=200, blank=False, null=False)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField()

    cao = models.CharField(max_length=200, blank=False, null=False)
    factor = models.CharField(max_length=200, blank=False, null=False)
    comments = models.TextField()

    class Meta:
        verbose_name_plural = "Vacancies"

    @property
    def company(self):
        return self.location.company
