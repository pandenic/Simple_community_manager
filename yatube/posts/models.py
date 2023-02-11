"""Models definition for posts app."""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """Model Group is used to store information about existed groups ."""

    title = models.CharField(
        verbose_name="Group title",
        help_text="Write in the name of the group (max 200 chars)",
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name="Group description",
        help_text="Write short group description",
        unique=True,
    )
    description = models.TextField()

    def __str__(self):
        """Show title of group."""
        return self.title


class Post(models.Model):
    """Model Post is used to store posts linked to authors and groups."""

    text = models.TextField(
        verbose_name="Post text",
        help_text="Write text",
    )
    pub_date = models.DateTimeField(
        verbose_name="Publication date",
        help_text="Moment in time when post was created",
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        related_name="posts",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        verbose_name="Group",
        help_text="Group which post is related to",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
    )
    image = models.ImageField(
        verbose_name="Image",
        help_text="Image may be uploaded if you want",
        upload_to="posts/",
        blank=True,
    )

    class Meta:
        """Used to change the behavior of Post model fields."""

        ordering = ("-pub_date",)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Show truncated title of post."""
        return self.text[:15]


class Comment(models.Model):
    """Model Comment is used to store comments.

    Linked to authors and posts.
    """

    text = models.TextField(
        verbose_name="Comment text",
        help_text="Write text",
    )
    created = models.DateTimeField(
        verbose_name="Creation date",
        help_text="Moment in time when comment was created",
        auto_now_add=True,
    )
    post = models.ForeignKey(
        Post,
        verbose_name="Post",
        help_text="Post to which comment is related to",
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        help_text="Author of comment",
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        """Used to change the behavior of Comment model fields."""

        ordering = ("-created",)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """Show truncated title of comment."""
        return (f'{self.text[:15]}, created '
                f'{self.created.strftime("%d.%m.%y_%M:%H")}')


class Follow(models.Model):
    """Model Follow is used to store comments.

    Linked to authors and followers.
    """

    user = models.ForeignKey(
        User,
        verbose_name="Follower",
        help_text="Follower who going to subscribe to author",
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        help_text="Author who is followed by follower",
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        """Used to change the behavior of Follow model fields."""

        ordering = ("user",)
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'

    def __str__(self):
        """Show follower - following chain."""
        return f'{self.user} follows {self.author}'
