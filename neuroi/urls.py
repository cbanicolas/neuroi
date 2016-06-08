from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.sites.models import Site
from neuroi import views
admin.autodiscover()
admin.site.unregister(Site)

urlpatterns = [
    #url(r'^$', TemplateView.as_view(template_name='base.html')),

    # Examples:
    url(r'^$', views.index, name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^pacientes/$', views.pacientes, name='pacientes'),

    url(r'^notas/(?P<tit_slug>[-\w]+)/$', views.nota, name='nota'),

    url(r'^contacto/$', views.contacto, name='contacto'),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^calendar/', include('django_bootstrap_calendar.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

if not settings.PRODUCCION:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]
