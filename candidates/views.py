from django.db import transaction
from django.views.generic.edit import CreateView

from candidates.forms import CandidateForm, LanguagesFormSet
from candidates.models import Candidate


class RegistrationView(CreateView):
    model = Candidate
    form_class = CandidateForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["languages_formset"] = LanguagesFormSet(self.request.POST)
        else:
            data["languages_formset"] = LanguagesFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        languages_formset = context["languages_formset"]
        with transaction.commit_on_success():
            form.instance.created_by = self.request.user
            form.instance.updated_by = self.request.user
            self.object = form.save()
        if languages_formset.is_valid():
            languages_formset.instance = self.object
            languages_formset.save()

        return super().form_valid(form)
