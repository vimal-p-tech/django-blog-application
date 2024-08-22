
from django.shortcuts import render
from django.urls import reverse_lazy    
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from hashids import Hashids

from django.views.generic import ListView,DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,DeleteView

from .models import Blog
from .forms import  BlogForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Create your views here.

class BlogDashBoard(TemplateView):
    template_name = "blog_app/base.html"


@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_protect,name='dispatch')
class BlogCreateView(CreateView):
    model           = Blog
    form_class      = BlogForm
    template_name   = 'blog/create_blog.html'
    success_url     = reverse_lazy('blog:blog_list')

    def form_valid(self, form):

        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        self.cleaned_data = form.cleaned_data

        if Blog.objects.filter(title=title, content=content).exists():
            form.add_error(None, "This blog post already exists.")
            return self.form_invalid(form)
        super().form_valid(form)

        rendered_template = render_to_string('blog/blog_list.html',self.get_context_data())
        return JsonResponse({'blog_data':rendered_template})
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context['blogs'] = Blog.objects.get(title=self.cleaned_data['title'], content=self.cleaned_data['content'])
        else:
            context['blogs'] = Blog.objects.filter(auther=self.request.user)
        return context

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
class BlogListView(ListView):
    model = Blog
    template_name = 'blog/front_page.html'
    context_object_name = 'blog_posts'

    
@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_protect,name='dispatch')
class BlogList(ListView):
    model               = Blog
    template_name       = 'blog/list_blogs.html'
    context_object_name = 'blogs'
    paginate_by         = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(auther=self.request.user)

        return filtered_queryset

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

@method_decorator(login_required,name='dispatch')
@method_decorator(csrf_protect,name='dispatch')
class ManageBlog(ListView):
    model               = Blog
    template_name       = 'blog/manage_blog.html'
    context_object_name = 'blogs'
    paginate_by = 1



class DeleteBlog(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:manage_blog')



from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

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
        form     = form_class(instance=instance,prefix='form1')
        
        html_content = render_to_string('blog/test.html',{'form':form},request)
        return JsonResponse({'html_content': html_content})




from .forms import CommentForm
from django.shortcuts import redirect
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
