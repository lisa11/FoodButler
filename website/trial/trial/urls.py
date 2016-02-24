"""trial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


from django.http import HttpResponse

#def abc(request):
    #path = request.path
    #name = request.GET.get("name", "(no name)")
    #return HttpResponse("""
    #<h1>Title</h1>
    #<p>Welcome! You came to {}. Your name is {}.</p>
    #""".format(path, name))

#http://localhost:8000/sdjtnfjhkgh/?name=lisa


urlpatterns = [
    #url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    #url(r'', abc),
    url(r'^testing1', "menu.views.index"),
    url(r'^testing', "menu.views.testing"),
    url(r'^start/$', "query.views.query", name='start'),
    url(r'^results/$', "query.views.results", name='results'),

]