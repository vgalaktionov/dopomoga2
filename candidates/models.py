from django.conf.global_settings import LANGUAGES
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_jsonform.models.fields import JSONField
from dopomoga2.models import TimestampedModel
from localflavor.generic.models import BICField, IBANField
from localflavor.nl.models import NLZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


def default_languages():
    return [{"language": "uk", "level": 4}]


class Candidate(TimestampedModel):
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
    mobile_phone_number = PhoneNumberField(blank=True, null=True)

    languages = JSONField(schema=LANGUAGES_SCHEMA, default=default_languages, verbose_name=_("Languages"))
    drivers_licenses = models.CharField(max_length=200, verbose_name=_("Drivers Licenses"), default="")
    max_travel_one_way_minutes = models.PositiveSmallIntegerField(verbose_name=_("Maximum travel time to work (in minutes)"), default=30)
    work_time_restrictions = models.TextField(verbose_name=_("Work time restrictions"), blank=True, null=True)
    has_own_bicycle = models.BooleanField(verbose_name=_("Own bicycle"), default=False)
    has_own_car = models.BooleanField(verbose_name=_("Own car"), default=False)
    work_experience = models.TextField(verbose_name=_("Work experience"), blank=True, null=True)
    work_willing_to_consider = models.TextField(verbose_name=_("Types of work you are willing to consider"), blank=True, null=True)
    diplomas_certificates = models.TextField(verbose_name=_("Diplomas and certificates"), blank=True, null=True)
    cv = models.FileField(verbose_name=_("CV"), blank=True, null=True)

    place_of_birth = models.CharField(verbose_name=_("Place of birth"), max_length=100)
    country_of_birth = CountryField(verbose_name=_("Country of birth"))

    bsn = models.CharField(verbose_name=_("BSN"), max_length=9, validators=[RegexValidator(r"^\d*$")], blank=True, null=True)
    bsn_proof_file = models.FileField(verbose_name=_("BSN proof"), blank=True, null=True)
    marital_status = models.CharField(
        max_length=15, choices=MaritalStatus.choices, default=MaritalStatus.UNMARRIED, verbose_name=_("Marital status"), blank=True, null=True
    )

    iban = IBANField(verbose_name=_("IBAN"), blank=True, null=True)
    bic = BICField(verbose_name=_("SWIFT"), blank=True, null=True)

    passport_number = models.CharField(verbose_name=_("Passport number"), max_length=20, blank=True, null=True)
    passport_valid_to = models.DateField(verbose_name=_("Passport valid to"), blank=True, null=True)
    passport_file = models.FileField(verbose_name=_("Passport scan"), blank=True, null=True)
    nationality = CountryField(verbose_name=_("Nationality"), blank=True, null=True)

    comments = models.TextField(verbose_name=_("Comments"), blank=True, null=True)
    internal_comments = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.get_title_display()} {self.first_name} {self.last_name}"
