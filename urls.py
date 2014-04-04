from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'apps.core.views.home', name='home'),
    url(r'^', include('apps.core.urls')),
    url(r'^blog/', include('apps.blog.urls')),
    url(r'^accounts/login/', "django.contrib.auth.views.login", dict(template_name="login.html"), name="login"),
    url(r'^accounts/logout/', "django.contrib.auth.views.logout", {"next_page": "/"}, name="logout"),
    url(r'^accounts/profile/$', 'apps.blog.views.view_profile', name='view_profile'),
    url(r'^accounts/profile/edit_profile$', 'apps.blog.views.edit_profile', name='edit_profile'),
    url(r'^accounts/create/$', 'apps.blog.views.create_user', name='create_acc'),
    #url(r'^users/profile/$', 'django.contrib.auth.views.get_profile', name='view_profile'),
    # -------- ADMIN -----------
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )