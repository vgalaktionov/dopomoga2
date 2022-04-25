from tabnanny import verbose

from django.conf.global_settings import LANGUAGES
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from localflavor.generic.models import BICField, IBANField
from localflavor.nl.models import NLZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Candidate(models.Model):
    class Title(models.TextChoices):
        MR = "MR", _("Mr.")
        MS = "MS", _("Ms.")

    class MaritalStatus(models.TextChoices):
        UNMARRIED = "UNMARRIED", _("Unmarried")
        MARRIED = "MARRIED", _("Married")
        COHABITANT = "COHABITANT", _("Cohabitant")
        DIVORCED = "DIVORCED", _("Divorced")
        WIDOWED = "WIDOWED", _("Widowed")
        UNKNOWN = "UNKNOWN", _("Unknown")

    class DocumentType(models.TextChoices):
        PASSPORT = "UNMARRIED", _("Unmarried")
        MARRIED = "MARRIED", _("Married")
        COHABITANT = "COHABITANT", _("Cohabitant")
        DIVORCED = "DIVORCED", _("Divorced")
        WIDOWED = "WIDOWED", _("Widowed")
        UNKNOWN = "UNKNOWN", _("Unknown")

    title = models.CharField(max_length=10, choices=Title.choices, default=Title.MS, verbose_name=_("Title"))
    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    preposition = models.CharField(max_length=20)
    last_name = models.CharField(max_length=100, verbose_name=_("Last name"))
    initials = models.CharField(max_length=20)

    zipcode = NLZipCodeField(verbose_name=_("Zipcode"))
    street_number = models.CharField(max_length=10, verbose_name=_("Street number"))
    street = models.CharField(max_length=200, verbose_name=_("Street"))
    city = models.CharField(max_length=200, verbose_name=_("City"))
    country = CountryField(default="NL", verbose_name=_("Country"))

    email = models.EmailField(max_length=200, verbose_name=_("Email"))
    phone_number = PhoneNumberField(verbose_name=_("Phone number"))
    mobile_phone_number = PhoneNumberField()

    drivers_licenses = models.CharField(max_length=100)
    max_travel_one_way_minutes = models.PositiveSmallIntegerField(default=30)
    has_own_bicycle = models.BooleanField(default=False)
    has_own_car = models.BooleanField(default=False)
    work_experience = models.TextField()
    work_willing_to_consider = models.TextField()
    cv = models.FileField(upload_to="candidates.CVFile/bytes/filename/mimetype", blank=True, null=True)

    date_of_birth = models.DateField(verbose_name=_("Date of birth"))
    place_of_birth = models.CharField(max_length=100)
    country_of_birth = CountryField()

    bsn = models.CharField(max_length=9, validators=[RegexValidator(r"^\d*$")])
    bsn_proof_file = models.FileField(upload_to="candidates.BSNProofFile/bytes/filename/mimetype", blank=True, null=True)
    marital_status = models.CharField(max_length=15, choices=MaritalStatus.choices, default=MaritalStatus.UNMARRIED, verbose_name=_("Marital status"))

    iban = IBANField()
    bic = BICField()

    passport_number = models.CharField(max_length=20, blank=False, null=False)
    passport_valid_to = models.DateField(blank=False, null=False)
    passport_file = models.FileField(upload_to="candidates.PassportFile/bytes/filename/mimetype", blank=True, null=True)
    nationality = CountryField()


class DiplomaCertificate(models.Model):
    candidate = models.ForeignKey("candidates.Candidate", blank=False, null=False, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    diploma_certificate_file = models.FileField(upload_to="candidates.DiplomaCertificateFile/bytes/filename/mimetype", blank=True, null=True)


class Language(models.Model):
    class LanguageLevel(models.TextChoices):
        BEGINNER = "BEGINNER", _("Beginner")
        CONVERSATIONAL = "CONVERSATIONAL", _("Conversational")
        PROFESSIONAL = "PROFESSIONAL", _("Professional")
        FLUENT = "FLUENT", _("Fluent")
        NATIVE = "NATIVE", _("Native")

    candidate = models.ForeignKey("candidates.Candidate", blank=False, null=False, on_delete=models.CASCADE)
    language = models.CharField(max_length=7, choices=LANGUAGES)
    level = models.CharField(max_length=20, choices=LanguageLevel.choices)


class PassportFile(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class BSNProofFile(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class DiplomaCertificateFile(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class CVFile(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)
