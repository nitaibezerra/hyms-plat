from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Notification, User, UserFollow


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (("Perfil", {"fields": ("bio", "avatar")}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    """Admin para relacionamentos de seguir."""

    list_display = ["follower", "followed", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["follower__username", "followed__username"]
    readonly_fields = ["id", "created_at"]
    list_select_related = ["follower", "followed"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin para notificações."""

    list_display = ["recipient", "notification_type", "title", "is_read", "sender", "created_at"]
    list_filter = ["notification_type", "is_read", "created_at"]
    search_fields = ["recipient__username", "title", "message"]
    readonly_fields = ["id", "created_at"]
    list_select_related = ["recipient", "sender"]

    fieldsets = [
        (
            "Destinatário",
            {
                "fields": ["recipient", "sender"],
            },
        ),
        (
            "Conteúdo",
            {
                "fields": ["notification_type", "title", "message", "link"],
            },
        ),
        (
            "Estado",
            {
                "fields": ["is_read"],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["id", "created_at"],
                "classes": ["collapse"],
            },
        ),
    ]
