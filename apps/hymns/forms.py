"""
Forms for hymns app.
"""

from django import forms

from .models import HymnBook, HymnBookVersion


class HymnBookUploadForm(forms.Form):
    """
    Form for uploading a hymnbook via YAML file.
    """

    yaml_file = forms.FileField(
        label="Arquivo YAML",
        help_text="Envie um arquivo YAML com a estrutura do hinário",
        widget=forms.FileInput(
            attrs={
                "accept": ".yaml,.yml",
                "class": "form-control",
            }
        ),
    )

    cover_image = forms.ImageField(
        label="Imagem de Capa (opcional)",
        required=False,
        help_text="JPG, PNG ou GIF. Tamanho recomendado: 600x800px",
        widget=forms.FileInput(
            attrs={
                "accept": "image/*",
                "class": "form-control",
            }
        ),
    )

    def clean_yaml_file(self):
        """Validate YAML file."""
        yaml_file = self.cleaned_data.get("yaml_file")

        if yaml_file:
            # Verifica extensão
            if not yaml_file.name.endswith((".yaml", ".yml")):
                raise forms.ValidationError("O arquivo deve ter extensão .yaml ou .yml")

            # Verifica tamanho (max 10MB)
            if yaml_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("O arquivo não pode ser maior que 10MB")

        return yaml_file


class HymnBookVersionForm(forms.ModelForm):
    """
    Form for creating a new version of an existing hymnbook.
    """

    class Meta:
        model = HymnBookVersion
        fields = ["version_name", "description", "pdf_file", "yaml_file"]
        widgets = {
            "version_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Edição 2020, Versão Revisada",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descreva as diferenças desta versão...",
                    "rows": 4,
                }
            ),
            "pdf_file": forms.FileInput(
                attrs={
                    "accept": ".pdf",
                    "class": "form-control",
                }
            ),
            "yaml_file": forms.FileInput(
                attrs={
                    "accept": ".yaml,.yml",
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "version_name": "Nome da Versão",
            "description": "Descrição",
            "pdf_file": "Arquivo PDF (opcional)",
            "yaml_file": "Arquivo YAML (opcional)",
        }
        help_texts = {
            "version_name": "Identifique esta versão do hinário",
            "description": "Explique o que diferencia esta versão das outras",
        }


class DisambiguationChoiceForm(forms.Form):
    """
    Form for user to choose what to do when duplicates are detected.
    """

    CHOICE_CREATE_NEW = "create_new"
    CHOICE_ADD_VERSION = "add_version"
    CHOICE_CANCEL = "cancel"

    CHOICES = [
        (CHOICE_CREATE_NEW, "Criar novo hinário (são hinários diferentes)"),
        (CHOICE_ADD_VERSION, "Adicionar como nova versão de um hinário existente"),
        (CHOICE_CANCEL, "Cancelar upload"),
    ]

    choice = forms.ChoiceField(
        label="O que deseja fazer?",
        choices=CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        initial=CHOICE_CREATE_NEW,
    )

    selected_hymnbook = forms.UUIDField(
        label="Hinário selecionado",
        required=False,
        widget=forms.HiddenInput(),
    )

    version_name = forms.CharField(
        label="Nome da versão",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: Edição 2020",
            }
        ),
    )

    def clean(self):
        """Validate form based on choice."""
        cleaned_data = super().clean()
        choice = cleaned_data.get("choice")

        if choice == self.CHOICE_ADD_VERSION:
            # Se escolheu adicionar versão, precisa selecionar um hinário
            selected_hymnbook = cleaned_data.get("selected_hymnbook")
            version_name = cleaned_data.get("version_name")

            if not selected_hymnbook:
                raise forms.ValidationError("Você deve selecionar um hinário para adicionar a versão")

            if not version_name:
                raise forms.ValidationError("Você deve fornecer um nome para a versão")

        return cleaned_data


class HymnAudioUploadForm(forms.ModelForm):
    """Form para upload de áudio de hino."""

    class Meta:
        from .models import HymnAudio

        model = HymnAudio
        fields = ["audio_file", "title", "source", "recorded_at", "credits", "allow_download"]
        widgets = {
            "audio_file": forms.FileInput(
                attrs={
                    "accept": "audio/mpeg,audio/ogg,audio/flac",
                    "class": "form-control",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Gravação Studio 2023",
                }
            ),
            "source": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Studio XYZ, Rio de Janeiro",
                }
            ),
            "recorded_at": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "credits": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Quem cantou, gravou, produziu...",
                    "rows": 3,
                }
            ),
        }

    def clean_audio_file(self):
        """Valida o arquivo de áudio."""
        audio_file = self.cleaned_data.get("audio_file")

        if audio_file:
            # Validar tamanho (max 25MB)
            if audio_file.size > 25 * 1024 * 1024:
                raise forms.ValidationError("O arquivo não pode ter mais de 25MB.")

            # Validar extensão
            valid_extensions = [".mp3", ".ogg", ".flac"]
            if not any(audio_file.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError("Formato inválido. Use MP3, OGG ou FLAC.")

        return audio_file


class CommentForm(forms.ModelForm):
    """Form para comentários em hinos."""

    class Meta:
        from .models import Comment

        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escreva seu comentário...",
                    "rows": 4,
                    "maxlength": 1000,
                }
            ),
        }

    def clean_text(self):
        """Valida o texto do comentário."""
        text = self.cleaned_data.get("text")

        if text:
            # Validar comprimento mínimo
            if len(text.strip()) < 5:
                raise forms.ValidationError("O comentário deve ter pelo menos 5 caracteres.")

            # Validar se não é só espaços
            if not text.strip():
                raise forms.ValidationError("O comentário não pode estar vazio.")

        return text.strip()
