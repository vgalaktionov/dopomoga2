from django.contrib import admin

from candidates.models import Candidate


# Register your models here.
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    pass
