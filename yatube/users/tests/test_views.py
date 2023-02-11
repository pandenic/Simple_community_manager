"""Contain tests for views in users app in yatube project."""
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UsersViewTests(TestCase):
    """Tests views in users app."""

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
        self.test_client["auth_client"].force_login(UsersViewTests.auth_user)

    def test_users_views_use_expected_template_anon(self):
        """Check if public URLs in users app use correct templates."""
        url_templates_names_anon = {
            reverse_lazy("users:signup"): "users/signup.html",
            reverse_lazy("users:login"): "users/login.html",
        }
        for value, expected in url_templates_names_anon.items():
            with self.subTest(value=value):
                for client_type in self.test_client:
                    response = self.test_client[client_type].get(value)
                    self.assertTemplateUsed(response, expected)

    def test_users_views_use_expected_template_auth(self):
        """Check if URLs in users app use correct templates for auth client."""
        url_templates_names_auth = {
            reverse_lazy(
                "users:password_change_form",
            ): "users/password_change_form.html",
            reverse_lazy(
                "users:password_change_done",
            ): "users/password_change_done.html",
            reverse_lazy(
                "users:password_reset_form",
            ): "users/password_reset_form.html",
            reverse_lazy(
                "users:password_reset_done",
            ): "users/password_reset_done.html",
            reverse_lazy(
                "users:password_reset_complete",
            ): "users/password_reset_complete.html",
            reverse_lazy("users:logout"): "users/logged_out.html",
        }
        for value, expected in url_templates_names_auth.items():
            with self.subTest(value=value):
                response = self.test_client["auth_client"].get(value)
                self.assertTemplateUsed(response, expected)

        user = UsersViewTests.auth_user
        uidb = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        address = reverse_lazy(
            "users:password_reset_confirm",
            kwargs={
                "uidb64": uidb,
                "token": token,
            },
        )
        template = "users/password_reset_confirm.html"
        response = self.test_client["auth_client"].get(address, follow=True)

        self.assertTemplateUsed(response, template)

    def test_users_view_sign_up_uses_correct_context(self):
        """Check if signup view-function in users app uses correct context."""
        response = self.test_client["auth_client"].get(
            reverse_lazy("users:signup"),
        )
        self.assertIsInstance(response.context.get("form"), UserCreationForm)
