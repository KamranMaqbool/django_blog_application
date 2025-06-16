from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)
from django.contrib.postgres.search import TrigramSimilarity

from taggit.models import Tag

from .models import Post
from .forms import EmailForm, CommentForm, SearchForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
        
        
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailForm()
    
    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post, 
        id=post_id, 
        status=Post.Status.PUBLISHED
    )
    comment = None
    
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})

# Old Function-Based View
def post_list(request, tag_slug=None):
    posts_list = Post.objects.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    
    paginator = Paginator(posts_list, 3)  # Show 3 posts per page
    page_number = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post, 
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post_slug,
        status=Post.Status.PUBLISHED)
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
        ).exclude(id=post.id)
    
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by(
        '-same_tags', '-publish'
    )[:4]
    
    comments = post.comments.filter(active=True)
    form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts
    }
    
    return render(request, 'blog/post/detail.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Weighting queries
            
            # The default weights are D, C, B, and A, and they refer to the numbers 0.1, 0.2, 0.4, and 1.0,
            # respectively. We apply a weight of 1.0 to the title search vector (A) and a weight of 0.4 to the body
            # vector (B).
            
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query)
                )
                .filter(rank__gt=0.3)
                .order_by('-rank')
            )
            
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )
    
    
def post_search_with_trigram(request):
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity('title', query),
                )
                .filter(similarity__gt=0.1)
                .order_by('-similarity')
            )
    
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'results': results,
            'query': query
        }
    )