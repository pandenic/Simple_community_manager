"""Contain tests for models in post app in yatube django project."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post, Comment, Follow

User = get_user_model()


class PostModelTests(TestCase):
    """Test model Post in posts app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instances of models before testing.

        Models User, Post.
        """
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост",
        )

    def test_posts_post_model_has_correct_object_name(self):
        """Check if __str__ function in model Post works correctly."""
        post = PostModelTests.post
        self.assertEqual(str(post), "Тестовый пост")

    def test_posts_post_model_has_correct_verbose_and_help_text(self):
        """Check if verbose names and help texts in model Post are correct."""
        post = PostModelTests.post

        field_verbose = {
            "text": "Post text",
            "pub_date": "Publication date",
            "author": "Author",
            "image": "Image",
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_value,
                )

        field_help_texts = {
            "text": "Write text",
            "pub_date": "Moment in time when post was created",
            "group": "Group which post is related to",
            "image": "Image may be uploaded if you want",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text,
                    expected_value,
                )


class GroupModelTests(TestCase):
    """Tests model Group in posts app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instances of model Group before testing."""
        super().setUpClass()
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )

    def test_posts_group_model_has_correct_object_names(self):
        """Check if __str__ function of model Group works correctly."""
        group = GroupModelTests.group
        self.assertEqual(str(group), "Тестовая группа")

    def test_posts_group_model_has_correct_verbose_and_help_text(self):
        """Check if verbose names and help texts in model Post are correct."""
        group = GroupModelTests.group

        field_verbose = {
            "title": "Group title",
            "slug": "Group description",
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    expected_value,
                )

        field_help_texts = {
            "title": "Write in the name of the group (max 200 chars)",
            "slug": "Write short group description",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text,
                    expected_value,
                )


class CommentModelTests(TestCase):
    """Tests model Comment in posts app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instances of model Comment before testing."""
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост",
        )
        cls.test_comment = Comment.objects.create(
            text="Text comment text",
            post=cls.post,
            author=cls.user,
        )

    def test_posts_comment_model_has_correct_object_names(self):
        """Check if __str__ function of model Comment works correctly."""
        comment = CommentModelTests.test_comment
        self.assertEqual(
            str(comment),
            f"Text comment te, created "
            f"{comment.created.strftime('%d.%m.%y_%M:%H')}",
        )

    def test_posts_comment_model_has_correct_verbose_help_text(self):
        """Check if in model Comment are correct.

        "verbose name"
        "help text"
        """
        comment = CommentModelTests.test_comment

        field_verbose = {
            "text": "Comment text",
            "created": "Creation date",
            "post": "Post",
            "author": "Author",
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name,
                    expected_value,
                )

        field_help_texts = {
            "text": "Write text",
            "created": "Moment in time when comment was created",
            "post": "Post to which comment is related to",
            "author": "Author of comment",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).help_text,
                    expected_value,
                )


class FollowModelTests(TestCase):
    """Tests model Follow in posts app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instances of model Follow before testing."""
        super().setUpClass()
        cls.user = {
            "author": User.objects.create_user(username="author"),
            "base": User.objects.create_user(username="base"),
        }
        cls.test_follow = Follow.objects.create(
            user=cls.user["base"],
            author=cls.user["author"],
        )

    def test_posts_comment_model_has_correct_object_names(self):
        """Check if __str__ function of model Follow works correctly."""
        follow = FollowModelTests.test_follow
        self.assertEqual(
            str(follow), f"{self.user['base']} follows {self.user['author']}",
        )

    def test_posts_comment_model_has_correct_verbose_and_help_text(self):
        """Check if meta in model Follow are correct.

        "Verbose name"
        "Help texts"
        """
        follow = FollowModelTests.test_follow

        field_verbose = {
            "user": "Follower",
            "author": "Author",
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).verbose_name,
                    expected_value,
                )

        field_help_texts = {
            "user": "Follower who going to subscribe to author",
            "author": "Author who is followed by follower",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    follow._meta.get_field(field).help_text,
                    expected_value,
                )
