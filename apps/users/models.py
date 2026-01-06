from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model.
    """

    # Add custom fields here in the future
    bio = models.TextField(blank=True, help_text="Biografia do usuário")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.get_full_name() or self.email or self.username
