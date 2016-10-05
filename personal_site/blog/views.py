from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from .forms import FlatPageForm
from blog.models import Post


User = get_user_model()


class HomeView(TemplateView):

    def get(self, request):
        form = FlatPageForm()
        posts = Post.objects.all()
        context = {'posts': posts, 'new_post_form': form}
        return render(request, "blog/home.html", context)


class AboutMeView(TemplateView):

    def get(self, request):
        return render(request, "about_me.html")


class NewPost(View):

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        user = request.user
        content = request.POST['content']

        post = Post(author=user, content=content)
        post.save()
        return redirect('/')


class ProjectView(TemplateView):

    def get(self, request):
        return render(request, "projects.html")
