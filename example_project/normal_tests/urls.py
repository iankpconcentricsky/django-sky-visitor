from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from normal_tests.views import CustomLogoutView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'authuser_tests.views.home', name='home'),
    # url(r'^authuser_tests/', include('authuser_tests.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^user/', include('sky_visitor.urls')),
    url(r'^customlogout', CustomLogoutView.as_view(), name='custom_logout'),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
)
