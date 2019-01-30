from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from . import views

urlpatterns = [
    # url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^user/(?P<usr>\w+)/$', views.UserRest.as_view()),
    url(r'^user/(?P<usr>\w+)/new/$', views.NewUser.as_view()),
    url(r'^user/$', views.UserRest.as_view()),
]