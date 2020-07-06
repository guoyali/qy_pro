from django.conf.urls import  include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
                       # Examples:
                       # url(r'^$', 'qy_project.views.home', name='home'),
                       # url(r'^qy_project/', include('qy_project.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('new_app.urls')),
                       # url(r'^$', RedirectView.as_view(url='new_app/callback/')),
                       ]
