from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'apps.blog.views.home', name='blog_home'),
    #url(r'^posts/?$', 'apps.blog.views.posts', name='blog_posts'),
    url(r'^posts/create/$', 'apps.blog.views.create_post', name='blog_create_post'),
    url(r'^posts/edit/(?P<post_id>\d+)/$', 'apps.blog.views.edit_post', name='blog_edit_post'),
    url(r'^posts/(?P<post_id>\d+)/$', 'apps.blog.views.view_post', name='view_post'),
    #url(r'^posts/$', 'apps.blog.views.view_post', name='create_acc'),
    #url(r'^post/(?P<post_id>\d+)/comment/$', 'apps.blog.views.comment_post', name='blog_comment_post'),
)