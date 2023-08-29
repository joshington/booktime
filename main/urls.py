
from django.urls import path 
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from main import views
from main import models
from django.contrib.auth import views as auth_views
from main import forms


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            form_class=forms.AuthenticationForm,
        ),
        name="login",
    ),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path(
        "product/<slug:slug>/",
        DetailView.as_view(model=models.Product),
        name="product",
    ),
    path(
        "products/<slug:tag>/",
        views.ProductListView.as_view(),
        name="products",
    ),
    path(
        "about-us/", TemplateView.as_view(template_name="about_us.html"),name="about-us"
    ),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("contact-us/",views.ContactUsView.as_view(),name="contact_us")
]