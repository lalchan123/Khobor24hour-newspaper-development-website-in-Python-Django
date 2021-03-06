
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from health.models import HealthPost, HealthComment
from .forms import HealthCommentFrom
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db.models import Count
from django.contrib import messages


# Create your views here.

def health_index(request):
    
    health_post_all = HealthPost.objects.filter(status=1).order_by('-created_on')
    
    most_view_health_posts = HealthPost.objects.filter(status=1).order_by('-created_on')[4:8]
    
    popular_health_posts = HealthPost.objects.filter(status=1).order_by('-created_on')[:4]
    
    
    
    paginator = Paginator(health_post_all, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'most_view_health_posts': most_view_health_posts,
        'popular_health_posts': popular_health_posts,
        
    }
    return render(request, "health_index.html", context)



def health_detail(request, pk):
    
    
    healthpost = HealthPost.objects.get(pk=pk)
    
    

    health_slide_post = HealthPost.objects.filter(status=1).order_by('-created_on')[:3]
    
    health_post_related_s3 = HealthPost.objects.filter(status=1).order_by('-created_on')[:3]
    
    health_post_related_s6 = HealthPost.objects.filter(status=1).order_by('-created_on')[3:6]
    
    
    
   
    
    most_view_health_posts = HealthPost.objects.filter(status=1).order_by('-created_on')[4:8]
    
    popular_health_posts = HealthPost.objects.filter(status=1).order_by('-created_on')[:4]
    
    healthpost.visit_health += 1
    healthpost.save()
    
    comments = healthpost.health_comments.filter(active=True, parent__isnull=True).order_by('-created')
    
    commentslatest = healthpost.health_comments.filter(active=True, parent__isnull=True).order_by('-created')[:2]
    
    if request.method == 'POST':
        # comment has been added
        comment_form = HealthCommentFrom(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = HealthComment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.healthpost = healthpost
            # save
            new_comment.save()
            messages.success(request, '??????????????? ????????????????????? ????????????????????? ????????? ???????????????!', extra_tags='alert')
            return HttpResponseRedirect(reverse('health_detail', args=(healthpost.pk,)))
    else:
        comment_form = HealthCommentFrom()
    
    
    
    
    context = {
        
        "healthpost": healthpost,

        "health_slide_post": health_slide_post,
        "health_post_related_s3": health_post_related_s3,
        "health_post_related_s6": health_post_related_s6,
        
        
        "most_view_health_posts": most_view_health_posts,
        "popular_health_posts": popular_health_posts,
        
       
        "comments": comments,
        "commentslatest": commentslatest,
        "comment_form": comment_form,
       
       
      
    }

    return render(request, "health_detail.html", context)



def search_health(request):
    queryset = HealthPost.objects.filter(status=1).order_by('-created_on')
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(health_title__icontains=query) |
            Q(health_content__icontains=query)
           
        
        ).distinct()
    context = {
        'queryset': queryset,
       

    }
    return render(request, 'search_health.html', context)

