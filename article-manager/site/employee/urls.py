# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from employee import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.EmployeeDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)