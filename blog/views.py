from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown

from .models import Post, Category
from comments.forms import CommentForm

from django.views.generic import ListView,DetailView
# Create your views here.
# def index(request):
# 	return HttpResponse("Welcom to my index.")

# def index(request):
# 	return render(request, 'blog/index.html', context={
# 			'title': 'My blog index page',
# 			'welcome': 'Welcome to my blog index page!'
# 		})

# def index(r):
# 	post_list = Post.objects.all().order_by('-created_time')
# 	return render(r, 'blog/index.html', context={
# 			'post_list': post_list
# 		})

class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 2

def blogs(r):
	post_list = Post.objects.all().order_by('-created_time')
	return render(r, 'blog/blogs.html', context={
			'post_list': post_list
		})

def about(r):
	return render(r, 'blog/about.html',context={

		})

def single(r):
	return render(r, 'blog/single.html')

# def detail(request, pk):
# 	post = get_object_or_404(Post, pk = pk)

# 	post.increase_views()

# 	post.body = markdown.markdown(post.body, extensions=[
# 			'markdown.extensions.extra',
# 			'markdown.extensions.codehilite',
# 			'markdown.extensions.toc',
# 		])
# 	comment_list = post.comment_set.all()
# 	comment_count = post.comment_set.count()
# 	form = CommentForm()
# 	context = {
# 		'post': post,
# 		'comment_list':comment_list,
# 		'comment_count': comment_count,
# 		'form': form
# 	}
# 	return render(request, 'blog/detail.html', context=context)

class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'

	def get(self, request, *args, **kwargs):
		response =  super(PostDetailView, self).get(request, *args, **kwargs)
		self.object.increase_views()
		return response

	def get_object(self, queryset = None):
		post = super(PostDetailView, self).get_object(queryset=None)
		post.body = markdown.markdown(
				post.body,
				extensions = [
					'markdown.extensions.extra',
					'markdown.extensions.codehilite',
					'markdown.extensions.toc',
				]
			)
		return post
	
	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
				'form': form,
				'comment_list': comment_list
			})
		return context

# def archives(request, year, month):
# 	post_list = Post.objects.filter(
# 		created_time__year=year,
# 		created_time__month=month
# 		).order_by('-created_time')
# 	return render(request, 'blog/index.html', context = {'post_list': post_list})

class ArchivesView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 2

	def get_queryset(self):
		return super(ArchivesView,self).get_queryset().filter(created_time__year = self.kwargs.get('year'), created_time__month = self.kwargs.get('month'))


# def category(request, pk):
# 	cate = get_object_or_404(Category, pk = pk)
# 	post_list = Post.objects.filter(category = cate).order_by('-created_time')
# 	return render(request, 'blog/index.html', context = {'post_list': post_list})

class CategoryView(ListView):
	model = Post
	template_name  = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 2

	def get_queryset(self):
		cate = get_object_or_404(Category, pk = self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category = cate)

def fullwidth(request):
	post_list = Post.objects.all().order_by('-created_time')
	context = {'post_list': post_list}
	return render(request, 'blog/full-width.html', context)