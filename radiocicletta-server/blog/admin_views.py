from blog.models import Blog, Post
from programmi.models import Programmi
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required


def report(request):
    progr = {}
    tuttiblog = Blog.objects.all()
    for b in tuttiblog:
        progr[str(b.id)] = Programmi.objects.filter(blog=b)

    return render_to_response("admin/blog/report.html",
                              {'blog_list': tuttiblog,
                               'prog_dict': progr},
                              RequestContext(request, {}),)
report = staff_member_required(report)
