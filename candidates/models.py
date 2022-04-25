from django.conf.global_settings import LANGUAGES
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_jsonform.models.fields import JSONField
from localflavor.generic.models import BICField, IBANField
from localflavor.nl.models import NLZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


def default_languages():
    return [{"language": "uk", "level": 4}]


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

    class LanguageLevel(models.IntegerChoices):
        BEGINNER = 0, _("Beginner")
        CONVERSATIONAL = 1, _("Conversational")
        PROFESSIONAL = 2, _("Professional")
        FLUENT = 3, _("Fluent")
        NATIVE = 4, _("Native")

        __empty__ = _("(Unknown)")

    LANGUAGES_SCHEMA = {
        "type": "array",  # a list which will contain the items
        "items": {
            "type": "object",
            "keys": {
                "language": {"type": "string", "title": _("Language"), "choices": [{"label": _(name), "value": code} for code, name in LANGUAGES]},
                "level": {"type": "number", "title": _("Level"), "choices": [{"label": _(name), "value": value} for value, name in LanguageLevel.choices]},
            },
        },
    }

    class DriversLicenseType(models.TextChoices):
        A = "A", "A"
        AM = "AM", "AM"
        B = "B", "B"
        BE = "BE", "BE"
        C = "C", "C"
        CE = "CE", "CE"
        D = "D", "D"

    title = models.CharField(max_length=10, choices=Title.choices, default=Title.MS, verbose_name=_("Title"))
    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    preposition = models.CharField(max_length=20)
    last_name = models.CharField(max_length=100, verbose_name=_("Last name"))
    initials = models.CharField(max_length=20)
    date_of_birth = models.DateField(verbose_name=_("Date of birth"))

    zipcode = NLZipCodeField(verbose_name=_("Zipcode"))
    street_number = models.CharField(max_length=10, verbose_name=_("Street number"))
    street = models.CharField(max_length=200, verbose_name=_("Street"))
    city = models.CharField(max_length=200, verbose_name=_("City"))
    country = CountryField(default="NL", verbose_name=_("Country"))

    email = models.EmailField(max_length=200, verbose_name=_("Email"))
    phone_number = PhoneNumberField(verbose_name=_("Phone number"))
    mobile_phone_number = PhoneNumberField()

    languages = JSONField(schema=LANGUAGES_SCHEMA, default=default_languages, verbose_name=_("Languages"))
    drivers_licenses = models.CharField(max_length=200, verbose_name=_("Drivers Licenses"), default="")
    max_travel_one_way_minutes = models.PositiveSmallIntegerField(default=30)
    has_own_bicycle = models.BooleanField(default=False)
    has_own_car = models.BooleanField(default=False)
    work_experience = models.TextField(verbose_name=_("Work experience"), blank=True, null=True)
    work_willing_to_consider = models.TextField(verbose_name=_("Work willing to consider"), blank=True, null=True)
    diplomas_certificates = models.TextField(verbose_name=_("Diplomas and certificates"), blank=True, null=True)
    cv = models.FileField(verbose_name=_("CV"), blank=True, null=True)

    place_of_birth = models.CharField(max_length=100)
    country_of_birth = CountryField()

    bsn = models.CharField(max_length=9, validators=[RegexValidator(r"^\d*$")])
    bsn_proof_file = models.FileField(blank=True, null=True)
    marital_status = models.CharField(max_length=15, choices=MaritalStatus.choices, default=MaritalStatus.UNMARRIED, verbose_name=_("Marital status"))

    iban = IBANField()
    bic = BICField()

    passport_number = models.CharField(max_length=20, blank=False, null=False)
    passport_valid_to = models.DateField(blank=False, null=False)
    passport_file = models.FileField(blank=True, null=True)
    nationality = CountryField()
