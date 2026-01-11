"""
Forms for the users app.
"""

from django import forms

from .models import User


class ProfileEditForm(forms.ModelForm):
    """
    Form for editing user profile.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio", "avatar"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Sobrenome",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Conte um pouco sobre você...",
                    "rows": 5,
                }
            ),
            "avatar": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "bio": "Biografia",
            "avatar": "Foto de Perfil",
        }
