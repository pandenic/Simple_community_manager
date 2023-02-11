"""Contain tests for urls in posts app in yatube project."""
from http import HTTPStatus

from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Group, Post, Comment

User = get_user_model()


class PostsURLTests(TestCase):
    """Tests URLs in posts app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instances of models User, Post before testing."""
        super().setUpClass()
        cls.test_user = {
            "author": User.objects.create_user(username="auth_author"),
            "base": User.objects.create_user(username="auth_base"),
        }
        cls.group = Group.objects.create(
            title="Test group",
            slug="Test-slug",
            description="Test group description",
        )
        cls.post = Post.objects.create(
            author=cls.test_user["author"],
            text="Тестовый пост",
        )

    def setUp(self):
        """Define initial instances of clients before each test.

        Authorized and unauthorized clients.
        """
        self.test_client = {
            "guest": Client(),
        }
        self.test_client_auth = {
            "auth_author": Client(),
            "auth_base": Client(),
        }
        self.test_client_auth["auth_author"].force_login(
            PostsURLTests.test_user["author"],
        )
        self.test_client_auth["auth_base"].force_login(
            PostsURLTests.test_user["base"],
        )
        cache.clear()

    def test_posts_urls_use_expected_templates(self):
        """Check if URLs in posts app use correct templates."""
        user = PostsURLTests.test_user["author"]
        group = PostsURLTests.group
        post = PostsURLTests.post
        client_list = {
            **self.test_client,
            **self.test_client_auth,
        }

        url_templates_names_anon = {
            "/": "posts/index.html",
            f"/group/{group.slug}/": "posts/group_list.html",
            f"/profile/{user.username}/": "posts/profile.html",
            f"/posts/{post.pk}/": "posts/post_detail.html",
        }
        for value, expected in url_templates_names_anon.items():
            with self.subTest(value=value):
                for client_type in client_list:
                    cache.clear()
                    response = client_list[client_type].get(value)
                    self.assertTemplateUsed(response, expected)

        url_templates_names_auth_base = {
            "/create/": "posts/post_create.html",
        }
        for value, expected in url_templates_names_auth_base.items():
            with self.subTest(value=value):
                for client_type in self.test_client_auth:
                    response = self.test_client_auth[client_type].get(value)
                    self.assertTemplateUsed(response, expected)

        url_templates_names_auth_author = {
            f"/posts/{post.pk}/edit/": "posts/post_create.html",
        }
        for value, expected in url_templates_names_auth_author.items():
            with self.subTest(value=value):
                response = self.test_client_auth["auth_author"].get(value)
                self.assertTemplateUsed(response, expected)

    def test_posts_urls_existence(self):
        """Check if URLs in posts app exist.

        "/",
        "/group/{group.slug}/",
        "/profile/{user.username}/",
        "/posts/{post.pk}/",
        "/unexisting_page/",
        """
        user = PostsURLTests.test_user["author"]
        group = PostsURLTests.group
        post = PostsURLTests.post
        client_list = {
            **self.test_client,
            **self.test_client_auth,
        }

        url_response_anon = {
            "/": HTTPStatus.OK,
            f"/group/{group.slug}/": HTTPStatus.OK,
            f"/profile/{user.username}/": HTTPStatus.OK,
            f"/posts/{post.pk}/": HTTPStatus.OK,
            "/unexisting_page/": HTTPStatus.NOT_FOUND,
        }
        for value, expected in url_response_anon.items():
            with self.subTest(value=value):
                for client_type in client_list:
                    response = client_list[client_type].get(value)
                    self.assertEqual(response.status_code, expected)

    def test_posts_comment_url_existence(self):
        """Check if URLs in posts app exist.

        "/posts/{post.pk}/comment/"
        """
        post = PostsURLTests.post
        user = PostsURLTests.test_user['base']

        Comment.objects.create(
            text="Test comment text",
            post=post,
            author=user,
        )

        url_response_auth_author = {
            f"/posts/{post.pk}/comment/": HTTPStatus.FOUND,
        }
        for value, expected in url_response_auth_author.items():
            with self.subTest(value=value):
                response = self.test_client_auth["auth_author"].get(value)
                self.assertEqual(response.status_code, expected)

        url_response_auth_base_redirect = {
            f"/posts/{post.pk}/comment/": f"/posts/{post.pk}/",
        }
        for value, expected in url_response_auth_base_redirect.items():
            with self.subTest(value=value):
                response = self.test_client_auth["auth_base"].get(value)
                self.assertRedirects(response, expected)

        url_response_anon_redirect = {
            f"/posts/{post.pk}/comment/":
                f"/auth/login/?next=/posts/{str(post.pk)}/comment/",
        }
        for value, expected in url_response_anon_redirect.items():
            with self.subTest(value=value):
                for client_type in self.test_client:
                    response = self.test_client[client_type].get(value)
                    self.assertRedirects(response, expected)

    def test_posts_create_url_existence(self):
        """Check if URLs in posts app exist.

        "/create/"
        """
        url_response_auth_base = {
            "/create/": HTTPStatus.OK,
        }
        for value, expected in url_response_auth_base.items():
            with self.subTest(value=value):
                for client_type in self.test_client_auth:
                    response = self.test_client_auth[client_type].get(value)
                    self.assertEqual(response.status_code, expected)

        url_response_anon_redirect = {
            "/create/": "/auth/login/?next=/create/",
        }
        for value, expected in url_response_anon_redirect.items():
            with self.subTest(value=value):
                for client_type in self.test_client:
                    response = self.test_client[client_type].get(value)
                    self.assertRedirects(response, expected)

    def test_posts_edit_url_existence(self):
        """Check if URLs in posts app exist.

        "/posts/{post.pk}/edit/"
        """
        post = PostsURLTests.post

        url_response_auth_author = {
            f"/posts/{post.pk}/edit/": HTTPStatus.OK,
        }
        for value, expected in url_response_auth_author.items():
            with self.subTest(value=value):
                response = self.test_client_auth["auth_author"].get(value)
                self.assertEqual(response.status_code, expected)

        url_response_auth_base_redirect = {
            f"/posts/{post.pk}/edit/": f"/posts/{str(post.pk)}/",
        }
        for value, expected in url_response_auth_base_redirect.items():
            with self.subTest(value=value):
                response = self.test_client_auth["auth_base"].get(value)
                self.assertRedirects(response, expected)

        url_response_anon_redirect = {
            f"/posts/{post.pk}/edit/":
                f"/auth/login/?next=/posts/{str(post.pk)}/edit/",
        }
        for value, expected in url_response_anon_redirect.items():
            with self.subTest(value=value):
                for client_type in self.test_client:
                    response = self.test_client[client_type].get(value)
                    self.assertRedirects(response, expected)

    def test_posts_follow_url_existence(self):
        """Check if URLs in posts app exist.

        "/follow/"
        "/profile/<str:username>/follow/"
        "/profile/<str:username>/unfollow/"
        """
        user = PostsURLTests.test_user['author']

        url_response_anon_redirect = {
            "/follow/": "/auth/login/?next=/follow/",
            f"/profile/{user.username}/follow/":
                f"/auth/login/?next=/profile/{user.username}/follow/",
            f"/profile/{user.username}/unfollow/":
                f"/auth/login/?next=/profile/{user.username}/unfollow/",
        }
        for value, expected in url_response_anon_redirect.items():
            with self.subTest(value=value):
                for client_type in self.test_client:
                    response = self.test_client[client_type].get(value)
                    self.assertRedirects(response, expected)

        url_response_auth_base = {
            "/follow/": HTTPStatus.OK,
        }
        for value, expected in url_response_auth_base.items():
            with self.subTest(value=value):
                response = self.test_client_auth["auth_base"].get(value)
                self.assertEqual(response.status_code, expected)

        url_response_auth_base_redirect = {
            f"/profile/{user.username}/follow/":
                f"/profile/{user.username}/",
            f"/profile/{user.username}/unfollow/":
                f"/profile/{user.username}/",
        }
        for client_type in self.test_client_auth:
            for value, expected in url_response_auth_base_redirect.items():
                with self.subTest(value=value):
                    response = self.test_client_auth[client_type].get(value)
                    self.assertRedirects(response, expected)
