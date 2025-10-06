from django.urls import path
from .views.views import SingleEmailValidationView, BatchEmailValidationView

urlpatterns = [
    path("validate-email/", SingleEmailValidationView.as_view(), name="validate-email"),
    path("validate-emails/", BatchEmailValidationView.as_view(), name="validate-emails"),
]
