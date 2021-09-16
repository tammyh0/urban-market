from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("saved", views.saved, name="saved"),
    path("bid", views.bid, name="bid"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("comment", views.comment, name="comment"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.category, name="category"),
    path("close", views.close, name="close"),
    path("<str:id>", views.listing, name="listing")
]
