"""Contain tests in core app in yatube project."""
from django.test import TestCase, Client, override_settings
from django.urls import reverse_lazy


@override_settings(DEBUG=False)
class ErrorPageTests(TestCase):
    """Tests error pages in posts app."""

    def setUp(self):
        """Define initial instances of clients before each test."""
        self.test_client = Client(enforce_csrf_checks=True)

    def test_core_404_error_page_uses_custom_template(self):
        """Check if 404 error page in core app uses correct template."""
        unexisted_page = '/unexisted_page/'
        template = 'core/404.html'
        response = self.test_client.get(
            unexisted_page,
        )
        self.assertTemplateUsed(response, template)

    def test_core_403csrf_error_page_uses_custom_template(self):
        """Check if 403csrf error page in core app uses correct template."""
        index_page = reverse_lazy('posts:post_create')
        template = 'core/403csrf.html'
        response = self.test_client.post(
            index_page,
        )
        self.assertTemplateUsed(response, template)
