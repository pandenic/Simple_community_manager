"""Contain tests for forms in posts app in yatube project."""
import os
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.urls import reverse_lazy

from posts.models import Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFormTests(TestCase):
    """Tests forms in posts app."""

    @classmethod
    def setUpClass(cls):
        """Define initial instances of models before testing.

        Models User, Post, Group.
        """
        super().setUpClass()
        cls.auth_user = User.objects.create_user(username="auth_user")
        cls.test_group = Group.objects.create(
            title="Test group",
            slug="Test-slug",
            description="Test group description",
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded_img = SimpleUploadedFile(
            name='small.gif', content=small_gif, content_type='image/gif',
        )
        cls.test_post = Post.objects.create(
            text="Тестовый пост author",
            group=cls.test_group,
            author=cls.auth_user,
            image=cls.uploaded_img,
        )
        cls.APP_MEDIA_DIR = Post._meta.get_field('image').upload_to
        cls.small_gif_path = os.path.join(
            cls.APP_MEDIA_DIR, cls.uploaded_img.name,
        )

    @classmethod
    def tearDownClass(cls):
        """Delete test dirs."""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        """Define initial instances of before each test.

        Authorized and unauthorized clients
        """
        self.test_client = Client()
        self.test_client.force_login(PostsFormTests.auth_user)

    def test_posts_form_create_post(self):
        """Check if PostForm form allows to create post correctly."""
        group = PostsFormTests.test_group
        user = PostsFormTests.auth_user

        post_count = Post.objects.count()
        small_create_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x70\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        create_img = SimpleUploadedFile(
            name='small_create.gif',
            content=small_create_gif,
            content_type='image/gif',
        )
        form_data = {
            "text": "Form test post",
            "group": group.pk,
            "image": create_img,
        }
        small_create_gif_path = os.path.join(
            self.APP_MEDIA_DIR,
            form_data['image'].name,
        )
        response = self.test_client.post(
            reverse_lazy("posts:post_create"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse_lazy(
                "posts:profile",
                kwargs={"username": user.username},
            ),
        )
        self.assertEqual(Post.objects.count(), post_count + 1)

        post = Post.objects.first()
        self.assertEqual(post.text, form_data["text"])
        self.assertEqual(post.group, group)
        self.assertEqual(post.author, user)
        self.assertEqual(
            str(post.image),
            small_create_gif_path,
        )

    def test_posts_form_edit_post(self):
        """Check if PostForm form allows to edit post correctly."""
        group = PostsFormTests.test_group
        user = PostsFormTests.auth_user
        post = PostsFormTests.test_post

        post_count = Post.objects.count()
        small_changed_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        changed_img = SimpleUploadedFile(
            name='small_changed.gif',
            content=small_changed_gif,
            content_type='image/gif',
        )
        form_data = {
            "text": "Changed form test post",
            "group": group.pk,
            "image": changed_img,
        }
        response = self.test_client.post(
            reverse_lazy(
                "posts:post_edit",
                kwargs={"post_id": post.pk},
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse_lazy(
                "posts:post_detail",
                kwargs={"post_id": post.pk},
            ),
        )
        self.assertEqual(Post.objects.count(), post_count)
        post = Post.objects.last()
        self.assertEqual(post.text, form_data["text"])
        self.assertEqual(post.group, group)
        self.assertEqual(post.author, user)

        small_changed_gif_path = os.path.join(
            self.APP_MEDIA_DIR,
            str(form_data['image']),
        )
        self.assertEqual(
            str(post.image),
            small_changed_gif_path,
        )

    def test_posts_form_add_comment(self):
        """Check if CommentForm form allows to create comment correctly."""
        user = PostsFormTests.auth_user
        post = PostsFormTests.test_post

        comments_count = post.comments.count()
        form_data = {
            "text": "Test comment text",
        }
        response = self.test_client.post(
            reverse_lazy(
                "posts:add_comment",
                kwargs={"post_id": post.pk},
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse_lazy(
                "posts:post_detail",
                kwargs={"post_id": post.pk},
            ),
        )
        self.assertEqual(post.comments.count(), comments_count + 1)
        comment = post.comments.first()
        self.assertEqual(comment.text, form_data['text'])
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, user)
