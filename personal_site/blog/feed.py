from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Post


POST_ITEMS_COUNT = 5


class LatestPostsFeed(Feed):
    title = "MrLokans web-site latest news"
    link = "/posts/"
    description = "Latest blog posts."

    def items(self):
        return Post.objects.order_by('-created')[:POST_ITEMS_COUNT]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return '/#'
        # return reverse('news-item', args=[item.pk])