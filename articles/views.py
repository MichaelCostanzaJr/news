from http.client import BAD_REQUEST
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView
)

from django.urls import reverse_lazy
from django.core.exceptions import BadRequest, PermissionDenied
from .models import Article, Section, Status


class ArticleNavBarHelper:
    def __init__(self, context, dept):
        self.set_sections(context, dept)
        self.set_statuses(context)
    def set_sections(self, context, dept):
        context["sections"] = Section.objects.filter(name=dept.name)

    def set_statuses(self, context):
        context["statuses"] = Status.objects.all()



class ArticleListView(ListView):
    model = Article
    template_name = "articles/list.html"

    def get_article_list_context(self, context, section, status):
        context["article_list"] = Article.objects.filter(
                section=section
            ).filter(
                status=status
            ).order_by("created_on").reverse()
        return context


    def set_sections(self, context):
        context["sections"] = Section.objects.all()

    def set_statuses(self, context):
        context["statuses"] = Status.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_id = self.kwargs.get("status")
        section_id = self.kwargs.get("section")
        user_department = self.request.user.department
        status = Status.objects.get(id=status_id)
        section = Section.objects.get(id=section_id)
        ArticleNavBarHelper(context, user_department)
        if status.id == 1:
            return self.get_article_list_context(context, section, status)
        if self.request.user.role.id > 1:
            return self.get_article_list_context(context, section, status)
        raise PermissionDenied("You are not authorized to view this page.")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/detail.html"

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = "articles/edit.html"
    fields = [
        "title",
        "subtitle",
        "body",
        "status"
    ]

    def form_valid(self, form):
        if form.instance.status == "published":
            raise BadRequest("You are not authorized to publish; Request a review first."
            )
        return super().form_valid(form)

class ArticleCreateView(CreateView):
    model = Article
    template_name = "articles/new.html"
    fields = [
        "title", "subtitle",
        "body", "status",
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.istance.status == "published":
            raise BadRequest("You are not authorized to publish; Request a review first."
            )
        return super().form_valid(form)

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "articles/delete.html"
