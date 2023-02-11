"""Contain page renders for users app."""
from django.views.generic import CreateView
from django.urls import reverse_lazy

from users.forms import CreationForm


class SignUp(CreateView):
    """View for Sign up."""

    form_class = CreationForm
    success_url = reverse_lazy("posts:index")
    template_name = "users/signup.html"