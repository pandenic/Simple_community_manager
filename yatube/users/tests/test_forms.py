"""Contain tests for forms in users app in yatube project."""
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

User = get_user_model()


class UsersFormTests(TestCase):
    """Tests forms in users app."""

    def setUp(self):
        """Define initial instances of clients before each test.

        Authorized and unauthorized clients.
        """
        self.guest_client = Client()

    def test_users_form_create_user(self):
        """Check if PostForm create correct form."""
        user_count = User.objects.count()
        form_data = {
            "first_name": "Xena",
            "last_name": "",
            "username": "warrior_princess",
            "email": "xena@xenaverse.tv",
            "password1": "XenaFight1!",
            "password2": "XenaFight1!",
        }
        response = self.guest_client.post(
            reverse_lazy("users:signup"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse_lazy("posts:index"))
        self.assertEqual(User.objects.count(), user_count + 1)
