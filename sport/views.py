
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sport.models import SportPost, SportComment
from .forms import SportCommentFrom
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db.models import Count
from django.contrib import messages

# Create your views here.

def sport_index(request):
    
    sport_post_all = SportPost.objects.filter(status=1).order_by('-created_on')
    
    most_view_sport_posts = SportPost.objects.filter(status=1).order_by('-created_on')[4:8]
    
    popular_sport_posts = SportPost.objects.filter(status=1).order_by('-created_on')[:4]
    
    
    
    paginator = Paginator(sport_post_all, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'most_view_sport_posts': most_view_sport_posts,
        'popular_sport_posts': popular_sport_posts,
        
    }
    return render(request, "sport_index.html", context)



def sport_detail(request, pk):
    
    
    sportpost = SportPost.objects.get(pk=pk)
    
    

    sport_slide_post = SportPost.objects.filter(status=1).order_by('-created_on')[:3]
    
    sport_post_related_s3 = SportPost.objects.filter(status=1).order_by('-created_on')[:3]
    
    sport_post_related_s6 = SportPost.objects.filter(status=1).order_by('-created_on')[3:6]
    
    
    
   
    
    most_view_sport_posts = SportPost.objects.filter(status=1).order_by('-created_on')[4:8]
    
    popular_sport_posts = SportPost.objects.filter(status=1).order_by('-created_on')[:4]
    
    sportpost.visit_sport += 1
    sportpost.save()
    
    comments = sportpost.sport_comments.filter(active=True, parent__isnull=True).order_by('-created')
    
    commentslatest = sportpost.sport_comments.filter(active=True, parent__isnull=True).order_by('-created')[:2]
    
    if request.method == 'POST':
        # comment has been added
        comment_form = SportCommentFrom(data=request.POST)
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
                parent_obj = SportComment.objects.get(id=parent_id)
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
            new_comment.sportpost = sportpost
            # save
            new_comment.save()
            messages.success(request, '??????????????? ????????????????????? ????????????????????? ????????? ???????????????!', extra_tags='alert')
            return HttpResponseRedirect(reverse('sport_detail', args=(sportpost.pk,)))
    else:
        comment_form = SportCommentFrom()
    
    
    
    
    context = {
        
        "sportpost": sportpost,

        "sport_slide_post": sport_slide_post,
        "sport_post_related_s3": sport_post_related_s3,
        "sport_post_related_s6": sport_post_related_s6,
        
        
        "most_view_sport_posts": most_view_sport_posts,
        "popular_sport_posts": popular_sport_posts,
        
       
        "comments": comments,
        "commentslatest": commentslatest,
        "comment_form": comment_form,
      
       
      
    }

    return render(request, "sport_detail.html", context)




def search_sport(request):
    queryset = SportPost.objects.filter(status=1).order_by('-created_on')
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(sport_title__icontains=query) |
            Q(sport_content__icontains=query)
           
        
        ).distinct()
    context = {
        'queryset': queryset,
       

    }
    return render(request, 'search_sport.html', context)
