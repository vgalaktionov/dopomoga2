"""dopomoga2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from candidates.views import RegistrationThanksView, RegistrationView
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

from dopomoga2.views import IndexView

last_modified_date = timezone.now()

admin.site.site_header = "Dopomoga Admin"
admin.site.site_title = "Dopomoga Admin Portal"
admin.site.index_title = "Welcome to Dopomoga Admin Portal"


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("jsi18n/", last_modified(lambda req, **kw: last_modified_date)(JavaScriptCatalog.as_view()), name="javascript-catalog"),
    path("registration-form", RegistrationView.as_view()),
    path("registration-thanks", RegistrationThanksView.as_view()),
    path("", IndexView.as_view()),
] + i18n_patterns(
    path("jsi18n/", last_modified(lambda req, **kw: last_modified_date)(JavaScriptCatalog.as_view()), name="javascript-catalog"),
)
