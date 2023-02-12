"""Administrator panel settings for posts app."""
from django.contrib import admin

from posts.models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    """Custom settings for posts admin panel."""

    list_display = (
        "pk",
        "text",
        "pub_date",
        "author",
        "group",
    )
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"
    list_editable = ("group",)


class GroupAdmin(admin.ModelAdmin):
    """Custom settings for groups admin panel."""

    list_display = (
        "pk",
        "title",
        "slug",
        "description",
        "post_count",
    )
    list_display_links = ("title",)
    empty_value_display = "-пусто-"
    list_editable = ("description",)

    def post_count(self, obj):
        """Count post quantity."""
        return obj.posts.count()

    post_count.short_description = "Posts quantity"


class CommentAdmin(admin.ModelAdmin):
    """Custom settings for comment admin panel."""

    list_display = (
        "pk",
        "text",
        "created",
        "post",
        "author",
    )
    search_fields = ("text",)
    list_filter = ("created",)
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    """Custom settings for follow admin panel."""

    list_display = (
        "user",
        "author",
    )
    search_fields = ("user", "author")
    list_filter = ("user",)
    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
