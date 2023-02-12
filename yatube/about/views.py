"""Contain page renders for about app."""
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Create author template page."""

    template_name = "about/author.html"


class AboutTechView(TemplateView):
    """Create using technologies template page."""

    template_name = "about/tech.html"
