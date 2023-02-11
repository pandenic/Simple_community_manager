"""Contain tests for urls in users app in yatube project."""
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase, Client
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()


class UsersURLTests(TestCase):
    """Tests URLs in users app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instance of model User before testing."""
        super().setUpClass()
        cls.auth_user = User.objects.create_user(username="auth_user")

    def setUp(self):
        """Define initial instances of clients before each test.

        Authorized and unauthorized clients.
        """
        self.test_client = {
            "guest_client": Client(),
            "auth_client": Client(),
        }
        self.test_client["auth_client"].force_login(UsersURLTests.auth_user)

    def test_users_urls_use_expected_template_anon(self):
        """Check if public URLs in users app use correct templates."""
        url_templates_names_anon = {
            "/auth/signup/": "users/signup.html",
            "/auth/login/": "users/login.html",
        }
        for value, expected in url_templates_names_anon.items():
            with self.subTest(value=value):
                for client_type in self.test_client:
                    response = self.test_client[client_type].get(value)
                    self.assertTemplateUsed(response, expected)

    def test_users_urls_use_expected_template_auth(self):
        """Check if URLs in users app use correct templates for auth client."""
        url_templates_names_auth = {
            "/auth/password_change/": "users/password_change_form.html",
            "/auth/password_change/done/": "users/password_change_done.html",
            "/auth/password_reset/": "users/password_reset_form.html",
            "/auth/password_reset/done/": "users/password_reset_done.html",
            "/auth/reset/done/": "users/password_reset_complete.html",
            "/auth/logout/": "users/logged_out.html",
        }
        for value, expected in url_templates_names_auth.items():
            with self.subTest(value=value):
                response = self.test_client["auth_client"].get(value)
                self.assertTemplateUsed(response, expected)

        user = UsersURLTests.auth_user
        uidb = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        address = f"/auth/reset/{uidb}/{token}/"
        template = "users/password_reset_confirm.html"
        response = self.test_client["auth_client"].get(address, follow=True)

        self.assertTemplateUsed(response, template)

    def test_users_urls_existence_anon(self):
        """Check if public URLs in users app exist."""
        url_response_public = {
            "/auth/signup/": HTTPStatus.OK,
            "/auth/login/": HTTPStatus.OK,
        }
        for value, expected in url_response_public.items():
            with self.subTest(value=value):
                for client_type in self.test_client:
                    response = self.test_client[client_type].get(value)
                    self.assertEqual(response.status_code, expected)

    def test_users_urls_existence_auth_password_change(self):
        """Check if URLs in users app exist for auth client."""
        url_response_auth = {
            "/auth/password_reset/": HTTPStatus.OK,
            "/auth/password_reset/done/": HTTPStatus.OK,
            "/auth/reset/done/": HTTPStatus.OK,
            "/auth/password_change/": HTTPStatus.OK,
            "/auth/password_change/done/": HTTPStatus.OK,
            "/auth/logout/": HTTPStatus.OK,
        }
        for value, expected in url_response_auth.items():
            with self.subTest(value=value):
                response = self.test_client["auth_client"].get(value)
                self.assertEqual(response.status_code, expected)

        user = UsersURLTests.auth_user
        uidb = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        address = rf"/auth/reset/{uidb}/{token}/"
        redirect_address = "/auth/reset/MQ/set-password/"
        response = self.test_client["auth_client"].get(address)
        self.assertRedirects(response, redirect_address)
