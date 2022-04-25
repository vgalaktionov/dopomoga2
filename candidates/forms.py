from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from localflavor.nl.forms import NLZipCodeField
from phonenumber_field.formfields import PhoneNumberField

from candidates.models import Candidate, Language


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["title", "last_name", "first_name", "date_of_birth", "email", "phone_number", "zipcode", "street_number", "street", "city", "country"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ["language", "level"]
