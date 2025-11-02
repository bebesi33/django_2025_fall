from django.shortcuts import render
import logging

from django_tables2 import RequestConfig
from main.filters import BlogPostFilter
from main.models import BlogPost
from main.tables import BlogPostTable
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic import ListView

logger = logging.getLogger(__name__)


def index(request):
    index_context = dict()
    return render(request, "index.html", index_context)


def posts(request):
    index_context = dict()
    return render(request, "posts.html", index_context)


def error_404_view(request, exception):
    logger.error(f"Hibák vannak és lesznek: {exception}")
    return render(request, "error_404.html", status=404)


def get_posts(request):
    # ezt feleslegesen részletesen kommenteltem ki, hogy érthetőbb legyen a működése
    # 1️ Az összes blogbejegyzést az adatbázisból
    queryset = BlogPost.objects.all()
    # 2️ Létrehozunk egy szűrőt, ami a GET paraméterek alapján szűri a bejegyzéseket
    blog_filter = BlogPostFilter(request.GET, queryset=queryset)

    # 3️ Létrehozunk egy táblázatot a szűrt eredményekből (django tables erre kellett :)
    blog_table = BlogPostTable(blog_filter.qs)

    # 4️ Ez a kiváló táblázat pagination-t is tud kezelni
    RequestConfig(request, paginate={"per_page": 5}).configure(blog_table)
    # erre itt találtok példákat: https://django-tables2.readthedocs.io/en/latest/pages/pagination.html

    # 5️ Debug célból kiírjuk a táblázat objektumot a konzolra
    print(blog_table)
    return render(request, "posts.html", {"table": blog_table, "filter": blog_filter})


def get_posts(request):
    queryset = BlogPost.objects.all()
    blog_filter = BlogPostFilter(request.GET, queryset=queryset)
    blog_table = BlogPostTable(blog_filter.qs)
    RequestConfig(request, paginate={"per_page": 5}).configure(blog_table)
    print(blog_table)
    return render(request, "posts.html", {"table": blog_table, "filter": blog_filter})


def get_posts_no_dependency(request):
    # Szűrés GET paraméter alapján (pl. cím tartalmazza)
    title_query = request.GET.get("title", "")
    if title_query:
        queryset = BlogPost.objects.filter(title__icontains=title_query)
    else:
        queryset = BlogPost.objects.all()

    print(f"get_posts_no_dependency: Title query: {title_query}")
    # Lapozás
    paginator = Paginator(queryset, 5)  # 5 bejegyzés oldalanként
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "posts_no_dep.html",
        {
            "page_obj": page_obj,
            "title_query": title_query,
        },
    )


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "posts_no_dep2.html"
    context_object_name = "page_obj"
    paginate_by = 10

    def get_queryset(self):
        """Ez adja meg a szűrt és rendezett QuerySet-et ami majd a listában megjelenik."""
        qs = super().get_queryset()
        title_query = self.request.GET.get("title")
        print(f"BlogPostListView: Title query: {title_query}")
        if title_query:
            qs = qs.filter(title__icontains=title_query)
        order = self.request.GET.get("order", "title")
        return qs.order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_query2"] = self.request.GET.get("title", "")
        return context
