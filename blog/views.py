from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from .forms import CommentForm, SearchForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tags = Tag.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 9)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html', {'posts': posts, 'tags': tags, 'tag': tag})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=slug,
                             publish__year=year, publish__month=month, publish__day=day)


    comments = post.comments.filter(active=True)
    comment_count = comments.count()
    form = CommentForm()

    # List of similar posts
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    tags = post.tags.all()
    all_tags = Tag.objects.all()
    return render(request, 'blog/detail.html',
                  {'post': post, 'comments': comments, 
                  'comment_count': comment_count,'form': form, 
                  'tags': tags, 'all_tags': all_tags})



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        comment.user = request.user
        # Save the comment to the database
        comment.save()
        return redirect(reverse('blog:post_detail', kwargs={'year': post.publish.year, 'month': post.publish.month, 'day': post.publish.day, 'slug': post.slug} ))
    
    return render(request, 'blog/comment.html',
                           {'post': post,
                            'form': form,
                            'comment': comment})

