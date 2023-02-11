"""Users description for posts app."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreationForm(UserCreationForm):
    """Form is used to process creation new users."""

    class Meta(UserCreationForm.Meta):
        """Metaclass of PostForm."""

        model = User
        fields = ("first_name", "last_name", "username", "email")
