from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from candidates.forms import CandidateForm
from candidates.models import Candidate


class RegistrationView(CreateView):
    model = Candidate
    form_class = CandidateForm
    success_url = "/registration-thanks"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data


class RegistrationThanksView(TemplateView):
    template_name = "candidates/registration_thanks.html"
