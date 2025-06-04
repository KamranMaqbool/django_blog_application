from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

import markdown

from .models import Post


class LatestPostFeed(Feed):
    
    name = 'K-Company Blog Latest Posts'
    description = 'New blog posts from K-Company.'
    link = reverse_lazy('blog:post_list')
    
    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_updated(self, item):
        return item.updated
