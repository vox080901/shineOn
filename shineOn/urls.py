"""shineOn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include
from django.contrib import admin
from django.conf.urls import url
from crazyDimond import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.Index.as_view({"get": "list"}), ),
    url(r'^shineon/', include("crazyDimond.urls", namespace="shineon")),
    # url(r'^articles/(\w+)/(\d+)/$', views.Articles.as_view({"get": "list", })),
    url(r'^articles/(?P<pk>\d+)/$', views.Articles.as_view({"get": "retrieve",})),
    url(r'^categories/$', views.Categories.as_view({"get": "list", })),
    # url(r'^categories/(\d+)/$', views.Categories.as_view({"get": "retrive",})),
    url(r"^files/$", views.Files.as_view({"get": "list", })),
    # url(r"^files/(\d+)/$", views.Files.as_view({"get": "retrieve", })),
    url(r"^tags/$", views.Tags.as_view({"get": "list", })),
    # url(r"^tags/(\d+)/$", views.Tags.as_view({"get": "retrieve", })),
    url(r'^categories/articles/(cat4art)|(tag4art)/(\d+)/$', views.Cat4Art.as_view({"get": "list", })),
    url(r'^tagandcat/$', views.TagsAndCats.as_view({"get": "list"})),
    url(r'^sendmail/$', views.SendMail.as_view()),
    url(r'^submit/$', views.UserSubmit.as_view()),
    url(r'^login/$', views.UserLogin.as_view()),
    url(r'^updown/(?P<pk>\d+)/$', views.UpDown.as_view({"patch": "partial_update"})),
]
