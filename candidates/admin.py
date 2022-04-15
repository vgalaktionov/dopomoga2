from django.contrib import admin

from candidates.models import Candidate, DiplomaCertificate, Language


class LanguageInline(admin.TabularInline):
    model = Language


class DiplomaCertificateInline(admin.TabularInline):
    model = DiplomaCertificate


# Register your models here.
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    inlines = [LanguageInline, DiplomaCertificateInline]
