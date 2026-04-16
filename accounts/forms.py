from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """Collect username, email, and password so login emails can be sent."""

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
