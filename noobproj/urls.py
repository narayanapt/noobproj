"""noobproj URL Configuration

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
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from noobproj.apps.core import views as core_views
from noobproj.apps.feeds import views as feed_views




    
urlpatterns = [
    url(r'^$', feed_views.FeedDislay, name='home'),
    url(r'^blog/$', core_views.blog, name='blog'),
    url(r'^qa/$', core_views.qa, name='qa'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^feeds/', include('noobproj.apps.feeds.urls')),
    url(r'^verify/(?P<uuid>[a-z0-9\-]+)/', core_views.verify, name='verify'),

    path('admin/', admin.site.urls),
 
]
"""  url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^feeds/', include('noobproj.apps.feeds.urls')),
"""