# -*- coding: utf-8 -*-
from django.shortcuts import redirect
#from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
#from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from apps.blog.models import Post
from django.core.exceptions import PermissionDenied


def owner(f):
    def _wrap_view(request, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, id=kwargs['post_id'])
        post_author = post.author
        if user != post_author:
            raise PermissionDenied()
        return f(request, *args, **kwargs)
    return _wrap_view