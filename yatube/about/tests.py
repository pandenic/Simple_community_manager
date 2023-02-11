"""Contain tests for about app in yatube project."""
from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse_lazy


class AboutURLTests(TestCase):
    """Tests URLs in about app."""

    def setUp(self):
        """Define initial instance of a guest client before each test."""
        self.guest_client = Client()

    def test_about_templates_urls_and_existence(self):
        """Check if templates and URLs in about app are correct."""
        url_templates = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for value, expected in url_templates.items():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
                self.assertTemplateUsed(response, expected)

        url_responses = {
            reverse_lazy('about:author'): HTTPStatus.OK,
            reverse_lazy('about:tech'): HTTPStatus.OK,
        }
        for value, expected in url_responses.items():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
                self.assertEqual(response.status_code, expected)

    def test_about_templates_views(self):
        """Check if namespaces in about app work correctly."""
        url_templates = {
            reverse_lazy('about:author'): 'about/author.html',
            reverse_lazy('about:tech'): 'about/tech.html',
        }
        for value, expected in url_templates.items():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
                self.assertTemplateUsed(response, expected)
