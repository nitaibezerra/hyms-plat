import uuid

from django.db import models
from django.utils.text import slugify


class HymnBook(models.Model):
    """
    Hinário - coleção de hinos.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Nome", max_length=255, unique=True, db_index=True, help_text="Nome do hinário")
    intro_name = models.CharField("Nome curto", max_length=100, blank=True, help_text="Nome de exibição curto")
    slug = models.SlugField("Slug", unique=True, max_length=255)
    owner_name = models.CharField(
        "Nome do dono", max_length=255, help_text="Pessoa que recebeu o hinário (texto livre)"
    )
    owner_user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_hymnbooks",
        verbose_name="Usuário dono",
        help_text="Usuário cadastrado como dono deste hinário",
    )
    cover_image = models.ImageField("Imagem de capa", upload_to="hymn_covers/", blank=True, null=True)
    description = models.TextField("Descrição", blank=True)

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Hinário"
        verbose_name_plural = "Hinários"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["owner_name"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def hymn_count(self):
        """Retorna o número de hinos neste hinário."""
        return self.hymns.count()


class Hymn(models.Model):
    """
    Hino - canto individual dentro de um hinário.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hymn_book = models.ForeignKey(
        HymnBook, on_delete=models.CASCADE, related_name="hymns", verbose_name="Hinário"
    )
    number = models.PositiveIntegerField("Número", help_text="Número sequencial do hino no hinário")
    title = models.CharField("Título", max_length=255, db_index=True)
    text = models.TextField("Letra", help_text="Letra completa do hino")

    # Campos opcionais
    received_at = models.DateField("Recebido em", null=True, blank=True, help_text="Data em que o hino foi recebido")
    offered_to = models.CharField("Oferecido para", max_length=255, blank=True, help_text="Pessoa dedicatária")
    style = models.CharField(
        "Estilo musical", max_length=50, blank=True, help_text="Ex: Valsa, Marcha, Mazurca"
    )
    extra_instructions = models.TextField("Instruções extras", blank=True, help_text="Instruções especiais de canto")
    repetitions = models.CharField(
        "Repetições", max_length=100, blank=True, help_text="Ex: 1-4, 5-8 (indicação de estrofes a repetir)"
    )

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Hino"
        verbose_name_plural = "Hinos"
        ordering = ["hymn_book", "number"]
        unique_together = [["hymn_book", "number"]]
        indexes = [
            models.Index(fields=["hymn_book", "number"]),
            models.Index(fields=["title"]),
            models.Index(fields=["received_at"]),
        ]

    def __str__(self):
        return f"{self.hymn_book.name} - {self.number}. {self.title}"

    @property
    def full_title(self):
        """Retorna título completo: Hinário - Nº. Título"""
        return str(self)
