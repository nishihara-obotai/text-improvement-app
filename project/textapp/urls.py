from django.urls import path

from . import views

app_name = "textapp"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("history/", views.history_list_view, name="history_list"),
    path("history/<int:pk>/", views.history_detail_view, name="history_detail"),
    path("history/<int:pk>/delete/", views.history_delete_view, name="history_delete"),
]
