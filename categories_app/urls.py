from django.conf.urls import url
from categories_app import views

urlpatterns = [
    url(r'^categories/$', views.CategoryList.as_view(), name='categories-list'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryDetail.as_view(), name='category-detail'),
]