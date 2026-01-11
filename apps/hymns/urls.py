from django.urls import path

from . import views, views_social

app_name = "hymns"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("hinarios/", views.HymnBookListView.as_view(), name="hymnbook_list"),
    path("hinarios/<slug:slug>/", views.HymnBookDetailView.as_view(), name="hymnbook_detail"),
    path("hinos/<uuid:pk>/", views.HymnDetailView.as_view(), name="hymn_detail"),
    path("busca/", views.search_view, name="search"),
    # Social features
    path("hinos/<uuid:hymn_id>/favoritar/", views_social.toggle_favorite, name="toggle_favorite"),
    path("hinos/<uuid:hymn_id>/comentar/", views_social.add_comment, name="add_comment"),
    path("comentarios/<uuid:comment_id>/deletar/", views_social.delete_comment, name="delete_comment"),
    path("comentarios/<uuid:comment_id>/reportar/", views_social.flag_comment, name="flag_comment"),
    path("hinos/<uuid:hymn_id>/upload-audio/", views_social.upload_audio, name="upload_audio"),
    path("audios/<uuid:audio_id>/download/", views_social.download_audio, name="download_audio"),
]
