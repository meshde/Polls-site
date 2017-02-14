from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name = 'index'),
	url(r'^(?P<qid>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<qid>[0-9]+)/results/$', views.results, name='results'),
	url(r'^(?P<qid>[0-9]+)/vote/$', views.vote, name='vote'),
]