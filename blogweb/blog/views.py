from django.shortcuts import render
from django.http import HttpResponse
from blog.models import post
from blog.forms import Contactform,Postform,Searchform
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView
from blog.models import Category
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin


class Postlistview(LoginRequiredMixin,ListView):
    login_url = 'login'
    model = post
    queryset = post.objects.filter(status="P")
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context



class Postdetailview(LoginRequiredMixin,DetailView):
    login_url = 'login'
    model = post
    template_name = 'blog/details.html'
    context_object_name = 'posts'


class Contact_form_view(FormView):
    form_class = Contactform
    success_url = "contact"
    template_name = 'blog/contact.html'

    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)



class Post_create_view(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = 'login'
    permission_required = 'blog.add_post'
    form_class =  Postform
    template_name = 'blog/post.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = User.objects.get(username= self.request.user)
        kwargs.update({'initial':{'author': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class post_update_view(LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'login'
    permission_required = 'blog.change_post'
    model = post
    form_class = Postform
    template_name = 'blog/post.html'

    def test_func(self,*args,**kwargs):
        slug = self.kwargs.get('slug')
        posts = post.objects.get(slug = slug)
        if self.request.user.get_username()== posts.author.get_username():
            return True
        else:
            return False

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = User.objects.get(username= self.request.user)
        kwargs.update({'initial':{'author': user}})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def search_view(request,*args,**kwargs):
    if request.method == 'GET':
        srch = request.GET.get('search')
        try:
            posts = post.objects.filter(title__icontains = srch)
            return render(request,'blog/index.html',context= {"posts":posts})
        except:
            return render(request,'blog/index.html',context= {"posts":posts})
    else:
        return render(request,'blog/index.html',context= {"posts":posts})

def specific_cat_list_view(request,slug,*args,**kwargs):
    cat = Category.objects.get(name__contains = slug)
    posts = cat.posts.all()
    if posts:
        return render(request,'blog/search.html',context= {"posts":posts})
    else:
        posts = post.objects.all()
        return render(request,'blog/search.html',context= {"posts":posts})
         

