from django.contrib import admin

from .models import Hymn, HymnBook


class HymnInline(admin.TabularInline):
    """Inline para exibir hinos dentro do hinário."""

    model = Hymn
    extra = 0
    fields = ["number", "title", "style", "received_at"]
    ordering = ["number"]


@admin.register(HymnBook)
class HymnBookAdmin(admin.ModelAdmin):
    """Admin para Hinários."""

    list_display = ["name", "intro_name", "owner_name", "owner_user", "hymn_count", "created_at"]
    list_filter = ["created_at", "owner_name"]
    search_fields = ["name", "intro_name", "owner_name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["id", "created_at", "updated_at", "hymn_count"]
    inlines = [HymnInline]

    fieldsets = [
        (
            "Informações Básicas",
            {
                "fields": ["name", "intro_name", "slug", "description", "cover_image"],
            },
        ),
        (
            "Proprietário",
            {
                "fields": ["owner_name", "owner_user"],
            },
        ),
        (
            "Metadados",
            {
                "fields": ["id", "hymn_count", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]


@admin.register(Hymn)
class HymnAdmin(admin.ModelAdmin):
    """Admin para Hinos."""

    list_display = ["number", "title", "hymn_book", "style", "received_at", "created_at"]
    list_filter = ["hymn_book", "style", "received_at", "created_at"]
    search_fields = ["title", "text", "hymn_book__name"]
    readonly_fields = ["id", "created_at", "updated_at", "full_title"]
    list_select_related = ["hymn_book"]

    fieldsets = [
        (
            "Informações Básicas",
            {
                "fields": ["hymn_book", "number", "title", "text"],
            },
        ),
        (
            "Detalhes",
            {
                "fields": ["style", "received_at", "offered_to", "repetitions", "extra_instructions"],
            },
        ),
        (
            "Metadados",
            {
                "fields": ["id", "full_title", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]
