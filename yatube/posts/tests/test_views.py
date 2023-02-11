"""Contain tests for views in posts app in yatube project."""
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.urls import reverse_lazy
from django import forms

from posts.models import Group, Post, Comment, Follow
from yatube.settings import MAX_POSTS_PER_PAGE, MAX_COMMENTS_PER_PAGE

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewTests(TestCase):
    """Tests views in posts app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instances of models before testing.

        Models User, Post, Group.
        Create test image.
        """
        super().setUpClass()
        cls.test_user = {
            "author": User.objects.create_user(username="auth_author"),
            "base": User.objects.create_user(username="auth_base"),
        }
        cls.test_group = Group.objects.create(
            title="author_group test group",
            slug="author_group-slug",
            description="author_group group description",
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif',
        )
        cls.test_post = Post.objects.create(
            text="Тестовый пост author",
            group=cls.test_group,
            author=cls.test_user["author"],
            image=uploaded,
        )
        cache.clear()

    @classmethod
    def tearDownClass(cls):
        """Delete test dirs."""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

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
            PostsViewTests.test_user["author"],
        )
        self.test_client_auth["auth_base"].force_login(
            PostsViewTests.test_user["base"],
        )
        cache.clear()

    def test_posts_view_uses_expected_templates(self):
        """Check if view-functions in posts app use expected templates.

        View-functions index, group_posts, profile, post_detail.
        """
        user = PostsViewTests.test_user["base"]
        group = PostsViewTests.test_group
        post = PostsViewTests.test_post

        views_templates_names_anon = {
            reverse_lazy("posts:index"): "posts/index.html",
            reverse_lazy(
                "posts:group_list",
                kwargs={"slug": group.slug},
            ): "posts/group_list.html",
            reverse_lazy(
                "posts:profile",
                kwargs={"username": user.username},
            ): "posts/profile.html",
            reverse_lazy(
                "posts:post_detail",
                kwargs={"post_id": post.pk},
            ): "posts/post_detail.html",
        }

        for value, expected in views_templates_names_anon.items():
            with self.subTest(value=value):
                for client_type in self.test_client:
                    cache.clear()
                    response = self.test_client[client_type].get(value)
                    self.assertTemplateUsed(response, expected)

        for value, expected in views_templates_names_anon.items():
            with self.subTest(value=value):
                for client_type in self.test_client_auth:
                    cache.clear()
                    response = self.test_client_auth[client_type].get(value)
                    self.assertTemplateUsed(response, expected)

    def test_posts_post_create_view_uses_expected_templates(self):
        """Check if post create view in posts app uses expected templates."""
        views_templates_names_auth = {
            reverse_lazy("posts:post_create"): "posts/post_create.html",
        }
        for value, expected in views_templates_names_auth.items():
            with self.subTest(value=value):
                for client_type in self.test_client_auth:
                    response = self.test_client_auth[client_type].get(value)
                    self.assertTemplateUsed(response, expected)

    def test_posts_post_edit_view_uses_expected_templates(self):
        """Check if post edit view in posts app uses expected templates."""
        post = PostsViewTests.test_post

        views_templates_names_auth_author = {
            reverse_lazy(
                "posts:post_edit",
                kwargs={"post_id": post.pk},
            ): "posts/post_create.html",
        }
        for value, expected in views_templates_names_auth_author.items():
            with self.subTest(value=value):
                response = self.test_client_auth["auth_author"].get(value)
                self.assertTemplateUsed(response, expected)

    def check_post(self, post):
        """Check given post fields."""
        self.assertEqual(post.text, self.test_post.text)
        self.assertEqual(post.group, self.test_post.group)
        self.assertEqual(post.author, self.test_post.author)
        self.assertEqual(post.image, self.test_post.image)

    def test_posts_index_view_uses_correct_context(self):
        """Check if index view in posts app use correct context."""
        client_list = {**self.test_client, **self.test_client_auth}

        for client_type in client_list:
            cache.clear()
            response = client_list[client_type].get(
                reverse_lazy("posts:index"),
            )
            self.check_post(response.context["page_obj"][0])

    def test_posts_profile_view_uses_correct_context(self):
        """Check if profile view in posts app use correct context."""
        user = PostsViewTests.test_user
        client_list = {
            **self.test_client,
            **self.test_client_auth,
        }

        for client_type in client_list:
            response = client_list[client_type].get(
                reverse_lazy(
                    "posts:profile",
                    kwargs={"username": user["author"].username},
                ),
            )
            self.check_post(response.context["page_obj"][0])

    def test_posts_group_posts_view_uses_correct_context(self):
        """Check if group_posts view in posts app use correct context."""
        group = PostsViewTests.test_group
        client_list = {**self.test_client, **self.test_client_auth}

        for client_type in client_list:
            response = client_list[client_type].get(
                reverse_lazy(
                    "posts:group_list",
                    kwargs={"slug": group.slug},
                ),
            )
            self.check_post(response.context["page_obj"][0])

    def test_posts_post_detail_view_uses_correct_context(self):
        """Check if post_detail view in posts app uses correct context."""
        post = PostsViewTests.test_post
        user = PostsViewTests.test_user['base']
        test_comment = Comment.objects.create(
            text='Text comment text',
            post=post,
            author=user,
        )

        client_list = {
            **self.test_client,
            **self.test_client_auth,
        }
        form_fields = {
            "text": forms.fields.CharField,
        }
        for client_type in client_list:
            response = client_list[client_type].get(
                reverse_lazy(
                    "posts:post_detail",
                    kwargs={"post_id": post.pk},
                ),
            )
            self.check_post(response.context["post"])
            comment = response.context["page_obj"][0]
            self.assertEqual(comment.text, test_comment.text)
            self.assertEqual(comment.post, test_comment.post)
            self.assertEqual(comment.author, test_comment.author)
            if client_type not in self.test_client:
                for value, expected in form_fields.items():
                    form_field = response.context.get("form").fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_posts_post_create_view_and_edit_use_correct_context(self):
        """Check if post_create view in posts app use correct context."""
        post = PostsViewTests.test_post

        responses = [
            self.test_client_auth["auth_author"].get(
                reverse_lazy("posts:post_edit", kwargs={"post_id": post.pk}),
            ),
            self.test_client_auth["auth_author"].get(
                reverse_lazy("posts:post_create"),
            ),
        ]
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
            "image": forms.fields.ImageField,
        }
        for response in responses:
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get("form").fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_posts_index_view_cache_works_correctly(self):
        """Check if caching in index view in posts app works correctly."""
        user = PostsViewTests.test_user['author']

        content_before = (
            self.test_client['guest']
            .get(
                reverse_lazy("posts:index"),
            )
            .content
        )
        Post.objects.create(
            text="New post",
            author=user,
        )

        content_after = (
            self.test_client['guest']
            .get(
                reverse_lazy("posts:index"),
            )
            .content
        )
        self.assertEqual(content_before, content_after)

        cache.clear()
        content_before = (
            self.test_client['guest']
            .get(
                reverse_lazy("posts:index"),
            )
            .content
        )
        self.assertNotEqual(content_before, content_after)

        content_after = (
            self.test_client_auth['auth_base']
            .get(
                reverse_lazy("posts:index"),
            )
            .content
        )
        self.assertNotEqual(content_before, content_after)

    def test_posts_follow_index_view_use_correct_context(self):
        """Check if follow_index view in posts app works correctly."""
        user = PostsViewTests.test_user
        Follow.objects.create(
            user=user['base'],
            author=user['author'],
        )

        response = self.test_client_auth['auth_base'].get(
            reverse_lazy("posts:follow_index"),
        )
        self.check_post(response.context["page_obj"][0])

        response = self.test_client_auth['auth_author'].get(
            reverse_lazy("posts:follow_index"),
        )
        self.assertEqual(len(response.context["page_obj"]), 0)

    def test_posts_profile_follow_unfollow_view_use_correct_context(self):
        """Check if views in posts app works correctly.

        "profile_follow"
        "profile_unfollow"
        """
        user = PostsViewTests.test_user
        follow_count = Follow.objects.count()

        self.test_client_auth['auth_base'].get(
            reverse_lazy(
                "posts:profile_follow",
                kwargs={
                    "username": user['author'].username,
                },
            ),
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)

        self.test_client_auth['auth_base'].get(
            reverse_lazy(
                "posts:profile_unfollow",
                kwargs={
                    "username": user['author'].username,
                },
            ),
        )
        self.assertEqual(Follow.objects.count(), follow_count)


class PaginatorTest(TestCase):
    """Tests paginator in posts app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instances of models before testing.

        Models User, Post, Group.
        """
        super().setUpClass()
        cls.test_user = {
            "author": User.objects.create_user(username="auth_author"),
            "base": User.objects.create_user(username="auth_base"),
        }
        cls.test_group = Group.objects.create(
            title="test group",
            slug="group-slug",
            description="group description",
        )
        cls.POST_SET_QUANTITY = MAX_POSTS_PER_PAGE + 1
        cls.COMMENTS_SET_QUANTITY = MAX_COMMENTS_PER_PAGE + 1
        for i in range(cls.POST_SET_QUANTITY):
            Post.objects.create(
                author=cls.test_user["base"],
                text=f"Тестовый пост base with group #{str(i)}",
            )
        for i in range(cls.POST_SET_QUANTITY):
            Post.objects.create(
                author=cls.test_user["author"],
                text=f"Тестовый пост author with group #{str(i)}",
                group=cls.test_group,
            )
        for i in range(cls.POST_SET_QUANTITY):
            Post.objects.create(
                author=cls.test_user["author"],
                text=f"Тестовый пост author no group #{str(i)}",
            )
        for i in range(cls.COMMENTS_SET_QUANTITY):
            Comment.objects.create(
                text=f"Test comment text #{str(i)}",
                post=Post.objects.first(),
                author=cls.test_user["author"],
            )

    def setUp(self):
        """Define initial instance of authorized client before each test."""
        self.test_client = Client()
        self.test_client.force_login(PaginatorTest.test_user["base"])

    def test_posts_index_view_paginator(self):
        """Check if paginator in index view shows works correctly."""
        posts_quantity = Post.objects.count()

        paginator_dict = {
            reverse_lazy("posts:index"): MAX_POSTS_PER_PAGE,
            reverse_lazy("posts:index") + "?page=2": MAX_POSTS_PER_PAGE,
            reverse_lazy("posts:index") + "?page=3": MAX_POSTS_PER_PAGE,
            reverse_lazy("posts:index")
            + "?page=4": posts_quantity % MAX_POSTS_PER_PAGE,
        }
        for url, expected_len in paginator_dict.items():
            cache.clear()
            response = self.test_client.get(url)
            self.assertEqual(len(response.context["page_obj"]), expected_len)

    def test_posts_group_view_paginator(self):
        """Check if paginator in group_posts view works correctly."""
        group = PaginatorTest.test_group
        last_page_quantity = self.POST_SET_QUANTITY - MAX_POSTS_PER_PAGE

        paginator_dict = {
            reverse_lazy(
                "posts:group_list",
                kwargs={"slug": group.slug},
            ): MAX_POSTS_PER_PAGE,
            reverse_lazy("posts:group_list", kwargs={"slug": group.slug})
            + "?page=2": last_page_quantity,
        }
        for url, expected_len in paginator_dict.items():
            response = self.test_client.get(url)
            self.assertEqual(len(response.context["page_obj"]), expected_len)

    def test_posts_profile_view_paginator(self):
        """Check if paginator in profile view works correctly."""
        user = PaginatorTest.test_user["base"]
        last_page_quantity = self.POST_SET_QUANTITY - MAX_POSTS_PER_PAGE

        paginator_dict = {
            reverse_lazy(
                "posts:profile",
                kwargs={"username": user.username},
            ): MAX_POSTS_PER_PAGE,
            reverse_lazy("posts:profile", kwargs={"username": user.username})
            + "?page=2": last_page_quantity,
        }
        for url, expected_len in paginator_dict.items():
            response = self.test_client.get(url)
            self.assertEqual(len(response.context["page_obj"]), expected_len)

    def test_posts_post_detail_view_comments_paginator(self):
        """Check if paginator for comments works correctly.

        in "post detail view".
        """
        post = Post.objects.first()
        last_page_quantity = self.COMMENTS_SET_QUANTITY - MAX_COMMENTS_PER_PAGE

        paginator_dict = {
            reverse_lazy(
                "posts:post_detail",
                kwargs={"post_id": post.pk},
            ): MAX_COMMENTS_PER_PAGE,
            reverse_lazy(
                "posts:post_detail",
                kwargs={"post_id": post.pk},
            )
            + "?page=2": last_page_quantity,
        }
        for url, expected_len in paginator_dict.items():
            response = self.test_client.get(url)
            self.assertEqual(len(response.context["page_obj"]), expected_len)

    def test_posts_follow_index_view_paginator(self):
        """Check if follow_index in index view shows works correctly."""
        user = PaginatorTest.test_user
        posts_quantity = Post.objects.filter(author=user['author']).count()
        Follow.objects.create(
            user=user['base'],
            author=user['author'],
        )

        paginator_dict = {
            reverse_lazy("posts:follow_index"): MAX_POSTS_PER_PAGE,
            reverse_lazy("posts:follow_index") + "?page=2": MAX_POSTS_PER_PAGE,
            reverse_lazy("posts:follow_index")
            + "?page=3": posts_quantity % MAX_POSTS_PER_PAGE,
        }
        for url, expected_len in paginator_dict.items():
            cache.clear()
            response = self.test_client.get(url)
            self.assertEqual(len(response.context["page_obj"]), expected_len)
