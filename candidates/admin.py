import json
from datetime import date

from admin_numeric_filter.admin import NumericFilterModelAdmin, RangeNumericFilter, SingleNumericFilter, SliderNumericFilter
from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from candidates.models import Candidate


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


class CandidateResource(resources.ModelResource):
    id = Field(attribute="id", column_name="Id")
    created = Field(attribute="created", column_name="Date")
    date_of_birth = Field(attribute="date_of_birth", column_name="Date 288")
    email = Field(attribute="email", column_name="Email")
    phone_number = Field(attribute="phone_number", column_name="Tel 970")
    city = Field(attribute="city", column_name="Gemeente")
    comments = Field(attribute="comments", column_name="Message")
    work_willing_to_consider = Field(attribute="work_willing_to_consider", column_name="Field")

    class Meta:
        model = Candidate
        fields = ("id", "created", "date_of_birth", "email", "phone_number", "city", "work_willing_to_consider")
        skip_unchanged = True
        report_skipped = True


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


@admin.register(Candidate)
class CandidateAdmin(NumericFilterModelAdmin, ImportExportModelAdmin):
    resource_class = CandidateResource
    list_display = ("__str__", "date_of_birth", "age", "zipcode", "city", "email", "phone_number", "has_own_bicycle", "has_own_car", "get_drivers_licenses")
    list_filter = (
        AgeGroupListFilter,
        "city",
        "has_own_bicycle",
        "has_own_car",
        ("max_travel_one_way_minutes", RangeNumericFilter),
        DriversLicenseFilter,
    )
    search_fields = ("first_name", "last_name", "zipcode", "city", "email", "phone_number", "max_travel_one_way_minutes")

    def get_drivers_licenses(self, obj):
        return json.loads(obj.drivers_licenses.replace("'", '"'))

    get_drivers_licenses.short_description = _("Drivers licenses")

    def age(self, obj):
        return now().date() - obj.date_of_birth
