from django.urls import path
from articles import views

urlpatterns = [
    path('',views.ArticleListView.as_view(), {"section": 1, "status": 1}, name="home"),
    path('<int:section>/<int:status>/', views.ArticleListView.as_view(), name="article_list"),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name="article_detail"),
    path('<int:pk>/edit/', views.ArticleUpdateView.as_view(), name="article_edit"),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name="article_delete")
]