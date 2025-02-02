
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse   
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404,redirect

from hashids import Hashids

from django.views.generic.base import TemplateView
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,DeleteView

from .models import Blog
from .forms import  BlogForm,CommentForm

from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required



# View for listing the created blogs.
class BlogListView(ListView):
    model = Blog
    template_name = 'blog/front_page.html'
    context_object_name = 'blog_posts'


# User Dashboard after the login.
@method_decorator(login_required,name='dispatch')
class BlogDashBoard(TemplateView):
    template_name = "blog_app/base.html"

# View for creating blogs.
@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_protect,name='dispatch')
class BlogCreateView(CreateView):
    form_class      = BlogForm
    template_name   = 'blog/create_blog.html'
    success_url     = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        form.instance.auther = self.request.user
        super().form_valid(form)
        messages.success(self.request,"Post Created Successfully..")
        return self.render_to_response(self.get_context_data(form=self.form_class()))


    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


# Blog List view for loggined user.
@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_protect,name='dispatch')
class BlogList(ListView):
    model               = Blog
    template_name       = 'blog/list_blogs.html'
    context_object_name = 'blogs'
    paginate_by         = 4

    def get_queryset(self): 
        return Blog.objects.filter(auther=self.request.user)

# Blog detail view for specific blog.
@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_protect,name='dispatch')
class BlogDetail(DetailView):
    model               = Blog
    template_name       = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        encrypted_pk = self.kwargs.get('encrypted_pk')
        hashids = Hashids(salt="test_id",min_length=8)
        blog_id = hashids.decode(encrypted_pk)[0]
        obj = get_object_or_404(Blog,id=blog_id)
        return obj
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context

# Manage view for CRUD operation on the blogs.
# blogs rendered on table data.
@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_protect,name='dispatch')
class ManageBlog(ListView):
    model               = Blog
    template_name       = 'blog/manage_blog.html'
    context_object_name = 'blogs'
    paginate_by = 4
    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(auther=self.request.user)

        return filtered_queryset

# View for deleting the blog.
class DeleteBlog(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:manage_blog')

# View that prints the ajax edit form.
@csrf_exempt
def get_edit_form(request,blog_id):
    form_class = BlogForm
    form_class.method = 'POST'
    form_class.action = request.path
    instance = Blog.objects.get(pk=blog_id)

    if request.method == form_class.method:
        form = form_class(request.POST,instance=instance,prefix='form1')
        if form.is_valid():
            form.save()
            return JsonResponse({'message':'Blog Updated successfully..'})
    else:
        form = form_class(instance=instance,prefix='form1')
        
        html_content = render_to_string('blog/edit_form.html',{'form':form},request)
        return JsonResponse({'html_content': html_content})    


@login_required
def add_comment(request,post_id):
    blog = Blog.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.auther = request.user
            comment.save()
            hashids = Hashids(salt="test_id",min_length=8)
            enc_id = hashids.encode(blog.pk)
            return redirect('blog:blog_detail', encrypted_pk=enc_id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})
