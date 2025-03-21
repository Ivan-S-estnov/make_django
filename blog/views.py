from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ["name", "description", "photo"]
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("blog:article_list")


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ["name", "description", "photo"]
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("blog:article_list")

    def get_success_url(self):
        return reverse("blog:article_detail", args=[self.kwargs.get("pk")])


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"
    success_url = reverse_lazy("blog:article_list")
