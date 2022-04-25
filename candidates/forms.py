from django import forms
from django.utils.translation import gettext_lazy as _

from candidates.models import Candidate


class CandidateForm(forms.ModelForm):
    drivers_licenses = forms.MultipleChoiceField(choices=Candidate.DriversLicenseType.choices, widget=forms.CheckboxSelectMultiple())

    def clean_drivers_licenses(self):
        if not set(self.cleaned_data["drivers_licenses"]).issubset({val for val, _k in Candidate.DriversLicenseType.choices}):
            raise forms.ValidationError("Select no more than 3.")
        return self.cleaned_data["drivers_licenses"]

    class Meta:
        model = Candidate
        fields = [
            "title",
            "last_name",
            "first_name",
            "date_of_birth",
            "email",
            "phone_number",
            "zipcode",
            "street_number",
            "street",
            "city",
            "country",
            "cv",
            "work_experience",
            "work_willing_to_consider",
            "languages",
            "drivers_licenses",
            "diplomas_certificates",
        ]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}
