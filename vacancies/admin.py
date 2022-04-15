from django.contrib import admin

from vacancies.models import Company, CompanyLocation, Vacancy


class CompanyLocationInline(admin.TabularInline):
    model = CompanyLocation


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyLocationInline]


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass
