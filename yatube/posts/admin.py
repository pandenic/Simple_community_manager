"""Administrator panel settings for posts app."""
from django.contrib import admin

from posts.models import Post, Group


class PostAdmin(admin.ModelAdmin):
    """Custom settings to posts admin panel."""

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
    """Custom settings to groups admin panel."""

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


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
