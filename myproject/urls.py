from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   # url(r'^login$',""),
  #  url(r'^logout',""),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^anotated/p/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_URL}),
    url(r'^usuarios$', "cms_users_put.views.info"),
    url(r'^anotated/(.*)$', "cms_users_put.views.mostrartemplate"),
    url(r'^usuarios/(.*)$', "cms_users_put.views.valores"),
    url(r'^(.*)$', "cms_users_put.views.NotFound"),
)
