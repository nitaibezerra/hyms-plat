from django.urls import path

from . import views

app_name = "hymns"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("hinarios/", views.HymnBookListView.as_view(), name="hymnbook_list"),
    path("hinarios/<slug:slug>/", views.HymnBookDetailView.as_view(), name="hymnbook_detail"),
    path("hinos/<uuid:pk>/", views.HymnDetailView.as_view(), name="hymn_detail"),
    path("busca/", views.search_view, name="search"),
]
