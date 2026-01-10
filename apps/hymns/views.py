from django.shortcuts import render
from django.views.generic import DetailView, ListView

from apps.search.typesense_client import search_hymns

from .models import Hymn, HymnBook


class HymnBookListView(ListView):
    """List all hymn books."""

    model = HymnBook
    template_name = "hymns/hymnbook_list.html"
    context_object_name = "hymnbooks"
    paginate_by = 20

    def get_queryset(self):
        return HymnBook.objects.all().order_by("name")


class HymnBookDetailView(DetailView):
    """Display a single hymn book with all its hymns."""

    model = HymnBook
    template_name = "hymns/hymnbook_detail.html"
    context_object_name = "hymnbook"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hymns"] = self.object.hymns.all().order_by("number")
        return context


class HymnDetailView(DetailView):
    """Display a single hymn."""

    model = Hymn
    template_name = "hymns/hymn_detail.html"
    context_object_name = "hymn"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return Hymn.objects.select_related("hymn_book")


def search_view(request):
    """Search hymns using TypeSense."""
    query = request.GET.get("q", "").strip()
    results = []
    total = 0

    if query:
        try:
            # Search in TypeSense
            ts_results = search_hymns(query, per_page=50)
            total = ts_results.get("found", 0)

            # Get hymn IDs from results
            hymn_ids = [hit["document"]["id"] for hit in ts_results.get("hits", [])]

            # Fetch actual hymns from database
            if hymn_ids:
                hymns = Hymn.objects.filter(id__in=hymn_ids).select_related("hymn_book")
                # Preserve TypeSense order
                hymns_dict = {str(h.id): h for h in hymns}
                results = [hymns_dict[hid] for hid in hymn_ids if hid in hymns_dict]
        except Exception:
            # Fallback to database search if TypeSense fails
            results = (
                Hymn.objects.filter(title__icontains=query)
                | Hymn.objects.filter(text__icontains=query)
                | Hymn.objects.filter(hymn_book__name__icontains=query)
            ).select_related("hymn_book")[:50]
            total = results.count()

    context = {
        "query": query,
        "results": results,
        "total": total,
    }
    return render(request, "hymns/search.html", context)


def home_view(request):
    """Home page with featured hymn books and search."""
    recent_hymnbooks = HymnBook.objects.all().order_by("-created_at")[:6]
    total_hymnbooks = HymnBook.objects.count()
    total_hymns = Hymn.objects.count()

    context = {
        "recent_hymnbooks": recent_hymnbooks,
        "total_hymnbooks": total_hymnbooks,
        "total_hymns": total_hymns,
    }
    return render(request, "hymns/home.html", context)
