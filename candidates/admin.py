import json
import re
from io import BytesIO

import requests
from admin_numeric_filter.admin import NumericFilterModelAdmin, RangeNumericFilter, SingleNumericFilter, SliderNumericFilter
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.core import files
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from transliterate import translit
from transliterate.utils import detect_language

from candidates.models import Candidate, default_languages


class DriversLicenseFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Drivers License")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "drivers_license"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ("A", _("A")),
            ("AM", _("AM")),
            ("B", _("B")),
            ("BE", _("BE")),
            ("C", _("C")),
            ("CE", _("CE")),
            ("D", _("D")),
            ("T", _("T")),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value():
            return queryset.filter(
                drivers_licenses__contains=f"'{self.value()}'",
            )


class AgeGroupListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Age Group")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "age_group"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ("0", _("0 - 18")),
            ("18", _("18 - 25")),
            ("25", _("25 - 35")),
            ("35", _("35 - 45")),
            ("45", _("45 - 55")),
            ("55", _("55 - 65")),
            ("65", _("65+")),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value() == "0":
            return queryset.filter(
                date_of_birth__gte=now() - relativedelta(years=18),
            )
        elif self.value() == "18":
            return queryset.filter(
                date_of_birth__gte=now() - relativedelta(years=25),
                date_of_birth__lt=now() - relativedelta(years=18),
            )
        elif self.value() == "25":
            return queryset.filter(
                date_of_birth__gte=now() - relativedelta(years=35),
                date_of_birth__lt=now() - relativedelta(years=25),
            )
        elif self.value() == "35":
            return queryset.filter(
                date_of_birth__gte=now() - relativedelta(years=45),
                date_of_birth__lt=now() - relativedelta(years=35),
            )
        elif self.value() == "45":
            return queryset.filter(
                date_of_birth__gte=now() - relativedelta(years=55),
                date_of_birth__lt=now() - relativedelta(years=45),
            )
        elif self.value() == "55":
            return queryset.filter(
                date_of_birth__gte=now() - relativedelta(years=65),
                date_of_birth__lt=now() - relativedelta(years=55),
            )
        elif self.value() == "65":
            return queryset.filter(
                date_of_birth__lt=now() - relativedelta(years=65),
            )


class FileFetchField(Field):
    def clean(self, data, **kwargs):
        if url := data[self.column_name]:
            try:
                print(f"Downloading file {url}...")
                res = requests.get(url)
                res.raise_for_status()
                buffer = BytesIO()
                buffer.write(res.content)
                file_name = url.split("/")[-1]
                print(f"File {url} downloaded successfully, size: {buffer.getbuffer().nbytes / 1000}kb .")
                return files.File(buffer, name=file_name)
            except Exception as e:
                print(e)
                raise
        return super().clean(data, **kwargs)


RUSSIAN_RE = re.compile(r"(усский|осійська|Russian)", re.I)
ENGLISH_RE = re.compile(r"(английский|English|англійською|англійська)", re.I)
GERMAN_RE = re.compile(r"(german|)$")
FRENCH_RE = re.compile(r"(французька|French|francais)")
DUTCH_RE = re.compile(r"(dutch|nederlands)")
POLISH_RE = re.compile(r"(польск|польська|Polish)", re.I)

CONVERSATIONAL_RE = re.compile(r"(середній)", re.I)
PROFESSIONAL_RE = re.compile(r"(професійний)", re.I)
FLUENT_RE = re.compile(r"(вільн|рідн)", re.I)


class CandidateResource(resources.ModelResource):
    id = Field(attribute="id", column_name="\ufeffId")
    created = Field(attribute="created", column_name="Date")
    date_of_birth = Field(attribute="date_of_birth", column_name="Date 288", default=now)
    email = Field(attribute="email", column_name="Email")
    phone_number = Field(attribute="phone_number", column_name="Tel 970")
    city = Field(attribute="city", column_name="Gemeente")
    comments = Field(attribute="comments", column_name="Message")
    work_willing_to_consider = Field(attribute="work_willing_to_consider", column_name="Field")
    drivers_licenses = Field(attribute="drivers_licenses", column_name="Driving Licence")
    first_name = Field(attribute="first_name", column_name="First name")
    patronymic = Field(attribute="patronymic", column_name="Patronymic")
    last_name = Field(attribute="last_name", column_name="Last name")
    name_cyrillic = Field(attribute="name_cyrillic", column_name="Name (cyrillic)")
    cv = FileFetchField(attribute="cv", column_name="File Cv")
    original_data = Field(attribute="original_data", column_name="original")
    languages = Field(attribute="languages", column_name="Languages")

    class Meta:
        model = Candidate
        fields = ("id", "created", "date_of_birth", "email", "phone_number", "city", "work_willing_to_consider", "drivers_licenses")
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, row_number=None, **kwargs):
        if row["Other Sectors"]:
            row["Field"] += f' , {row["Other Sectors"]}'
        row["Tel 970"] = row["Tel 970"].replace("'", "")
        self.parse_drivers_licenses(row)
        self.parse_name(row)
        self.parse_languages(row)
        try:
            row["Gemeente"] = translit(row["Gemeente"], reversed=True)
        except Exception:
            pass
        row["original"] = {**row}
        return super().before_import_row(row, row_number, **kwargs)

    def parse_languages(self, row):
        languages = default_languages()
        seen = {"uk"}
        for lang in re.split(r";|,|\.", row["Languages"].strip()):
            level = 0
            if CONVERSATIONAL_RE.search(lang):
                level = 1
            elif PROFESSIONAL_RE.search(lang):
                level = 2
            elif FLUENT_RE.search(lang):
                level = 3

            if ENGLISH_RE.search(lang) and "en" not in seen:
                languages.append({"language": "en", "level": level})
                seen.add("en")
            if RUSSIAN_RE.search(lang) and "ru" not in seen:
                languages.append({"language": "ru", "level": level or 2})
                seen.add("ru")
            if FRENCH_RE.search(lang) and "fr" not in seen:
                languages.append({"language": "fr", "level": level})
                seen.add("fr")
            if POLISH_RE.search(lang) and "pl" not in seen:
                languages.append({"language": "pl", "level": level})
                seen.add("pl")
            if DUTCH_RE.search(lang) and "nl" not in seen:
                languages.append({"language": "nl", "level": level})
                seen.add("nl")

        row["Languages"] = json.dumps(languages)

    def parse_name(self, row):
        name = row["Name"].strip()
        name_parts = name.split()
        is_cyrillic = detect_language(name) in ("ru", "ua") and not any(p.isascii() for p in name_parts)
        try:
            if len(name_parts) == 1:
                row["First name"] = name_parts[0] if not is_cyrillic else translit(name_parts[0], reversed=True)
            elif len(name_parts) == 2:
                if is_cyrillic:
                    row["Last name"] = translit(name_parts[0], reversed=True)
                    row["First name"] = translit(name_parts[1], reversed=True)
                else:
                    row["First name"] = name_parts[0]
                    row["Last name"] = name_parts[1]
            elif len(name_parts) == 3:
                if is_cyrillic:
                    row["Last name"] = translit(name_parts[0], reversed=True)
                    row["First name"] = translit(name_parts[1], reversed=True)
                    row["Patronymic"] = translit(name_parts[2], reversed=True)
                else:
                    row["First name"] = name_parts[0]
                    row["Patronymic"] = name_parts[1]
                    row["Last name"] = name_parts[2]
            row["Name (cyrillic)"] = name if is_cyrillic else translit(name, "uk")
        except Exception as e:
            print(e)
            pass

    def parse_drivers_licenses(self, row):
        licenses = []
        for license_type in ("A", "AM", "B", "BE", "C", "CE", "D", "T"):
            if license_type in row["Driving Licence"]:
                licenses.append(license_type)
        row["Driving Licence"] = licenses


@admin.register(Candidate)
class CandidateAdmin(NumericFilterModelAdmin, ImportExportModelAdmin):
    resource_class = CandidateResource
    list_display = (
        "__str__",
        "name_cyrillic",
        "date_of_birth",
        "age",
        "zipcode",
        "city",
        "email",
        "phone_number",
        "has_own_bicycle",
        "has_own_car",
        "get_drivers_licenses",
    )
    list_filter = (
        AgeGroupListFilter,
        "has_own_bicycle",
        "has_own_car",
        ("max_travel_one_way_minutes", RangeNumericFilter),
        DriversLicenseFilter,
    )
    search_fields = ("first_name", "last_name", "patronymic", "name_cyrillic", "zipcode", "city", "email", "phone_number", "max_travel_one_way_minutes")

    def get_drivers_licenses(self, obj):
        return json.loads(obj.drivers_licenses.replace("'", '"'))

    get_drivers_licenses.short_description = _("Drivers licenses")

    def age(self, obj):
        return (now().date() - obj.date_of_birth).days // 365
