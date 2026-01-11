"""
Views sociais para usuários (follow, notifications).
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Notification, User, UserFollow


@login_required
@require_POST
def toggle_follow(request, username):
    """Seguir/deixar de seguir usuário."""
    user_to_follow = get_object_or_404(User, username=username)

    # Não pode seguir a si mesmo
    if user_to_follow == request.user:
        messages.error(request, "Você não pode seguir a si mesmo.")
        return redirect("users:profile", username=username)

    follow, created = UserFollow.objects.get_or_create(follower=request.user, followed=user_to_follow)

    if not created:
        # Já seguia, então deixa de seguir
        follow.delete()
        is_following = False
        message = f"Você deixou de seguir {user_to_follow.username}"
    else:
        # Começou a seguir
        is_following = True
        message = f"Você agora segue {user_to_follow.username}"

        # Criar notificação
        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            notification_type=Notification.TYPE_FOLLOW,
            title="Novo seguidor",
            message=f"{request.user.username} começou a seguir você",
            link=f"/perfil/{request.user.username}/",
        )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"is_following": is_following, "message": message})

    messages.success(request, message)
    return redirect("users:profile", username=username)


@login_required
def notifications_list(request):
    """Listar notificações do usuário."""
    # Marcar não lidas como lidas
    request.user.notifications.filter(is_read=False).update(is_read=True)

    # Buscar últimas 50
    notifications = request.user.notifications.all()[:50]

    return render(request, "users/notifications.html", {"notifications": notifications})


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Marcar notificação como lida (AJAX)."""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)

    notification.is_read = True
    notification.save(update_fields=["is_read"])

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True})

    return redirect("users:notifications")


@login_required
def unread_notifications_count(request):
    """Retorna contagem de notificações não lidas (AJAX)."""
    count = request.user.notifications.filter(is_read=False).count()

    return JsonResponse({"count": count})


@login_required
def following_list(request, username):
    """Listar usuários que o usuário segue."""
    user = get_object_or_404(User, username=username)

    following = UserFollow.objects.filter(follower=user).select_related("followed")[:100]

    return render(request, "users/following_list.html", {"profile_user": user, "following": following})


@login_required
def followers_list(request, username):
    """Listar seguidores de um usuário."""
    user = get_object_or_404(User, username=username)

    followers = UserFollow.objects.filter(followed=user).select_related("follower")[:100]

    return render(request, "users/followers_list.html", {"profile_user": user, "followers": followers})
