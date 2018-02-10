"""mysite2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app import views as v1

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', v1.userlogin,name='login'),
    url(r'^logout/$', v1.logout,name='logout'),
    url(r'^index/$',v1.index,name='index'),
    url(r'^indexbynew/$',v1.indexbynew,name='indexbynew'),
    url(r'submitcommend/(?P<essay_id>[0-9]+)/$',v1.submitcomment,name='submitcomment'),
    url(r'^$',v1.home),
    url(r'^index/(?P<essay_id>[0-9]+)/$', v1.showblog, name='show_blog'),
    url(r'^index/add_essay/$',v1.add_essay,name='add_essay'),
    url(r'^index/sub_essay/$',v1.sub_essay,name='sub_essay'),
    url(r'^register/$',v1.register,name='register'),
    url(r'^likeit+1/$',v1.likeit,name='likeit+1'),
    url(r'^likeit-1/$',v1.likeit,name='likeit-1'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
