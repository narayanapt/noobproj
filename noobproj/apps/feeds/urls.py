from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^$', views.FeedDislay, name='feed-home'),
url(r'new/$', views.CreateNewFeed, name='new-feed'),
url(r'delete/$', views.RemoveFeed, name='delete-feed'),
url(r'comment/$', views.show_comments, name='comments-show')
]
