from django.contrib import admin

from candidates.models import Candidate, Language


class LanguageInline(admin.TabularInline):
    model = Language


# Register your models here.
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    inlines = [LanguageInline]
