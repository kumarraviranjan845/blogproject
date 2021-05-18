from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import BlogPost
from django.urls import reverse
from hitcount.views import HitCountDetailView

class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'blogposts'
    ordering = ['-date_posted']
    paginate_by = 3
    
class UserPostListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/user_blogs.html'
    context_object_name = 'blogposts'
    paginate_by = 3
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return BlogPost.objects.filter(author=user).order_by('-date_posted')
    
class PostDetailView(LoginRequiredMixin, HitCountDetailView):
    model = BlogPost
    count_hit = True
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        blogpost = get_object_or_404(BlogPost, id=self.kwargs['pk'])
        total_likes = blogpost.total_likes()
        is_liked = False
        if blogpost.likes.filter(id=self.request.user.id).exists():
            is_liked = True
        context['total_likes'] = total_likes
        context['is_liked'] = is_liked
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        blogpost = self.get_object()
        if self.request.user == blogpost.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = '/'
    
    def test_func(self):
        blogpost = self.get_object()
        if self.request.user == blogpost.author:
            return True
        return False

def like_view(request, pk):
    blogpost = get_object_or_404(BlogPost, id=request.POST.get('blogpost_id'))
    is_liked = False
    if blogpost.likes.filter(id=request.user.id).exists():
        blogpost.likes.remove(request.user)
        is_liked = False
    else:
        blogpost.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(reverse('blog-detail', args=[str(pk)]))

class UserLikeView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/user_likes.html'
    context_object_name = 'blogposts'
    paginate_by = 3
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return BlogPost.objects.filter(likes=user).order_by('-date_posted')
    
# def user_like(request):
#     user = User.objects.filter(username='username')
#     context = {
#         'liked_posts': BlogPost.objects.filter(likes=user)
#     }
#     return render(request, 'blog/user_likes.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})