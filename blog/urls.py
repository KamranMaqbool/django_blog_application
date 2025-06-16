from django.urls import path
from .views import post_list, post_detail, PostListView, post_share, post_comment, post_search, post_search_with_trigram
from .feed import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    
    # path('', PostListView.as_view(), name='post_list'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post_slug>/',
        post_detail,
        name='post_detail'
    ),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<post_id>/comment/', post_comment, name='post_comment'),
    
    ## Uncomment the following lines to use function-based views
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, name="posts_list_by_slug"),
    path('feed/', LatestPostFeed(), name="post_feed"),
    path('search/', post_search, name="post_search"),
    path('search-with-trigram/', post_search_with_trigram, name="post_search_with_trigram"),
    # path(
    #     '<int:year>/<int:month>/<int:day>/<slug:post>/',
    #     post_detail,
    #     name='post_detail'
    # ),
]