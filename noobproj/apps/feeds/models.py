from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Feed(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    parent = models.ForeignKey('Feed', null=True, blank=True, on_delete = models.CASCADE)

    class Meta:
        verbose_name = ('Feed')
        verbose_name_plural = ('Feeds')
        ordering = ('-date',)

    def __str__(self):
        return self.post

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            data = Feed.objects.filter(parent=None, id__lte=from_feed)
        else:
            data = Feed.objects.filter(parent=None)

        return data

    @staticmethod
    def get_feeds_after(feed):
        feeds = Feed.objects.filter(parent=None, id__gt=feed)
        return feeds

    def post_comment(self, user, post):
        comment_object = Feed(user=user, post=post, parent=self)
        comment_object.save()
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return comment_object

    def comments_count(self):
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def get_comments(self):
        return Feed.objects.filter(parent=self).order_by('date')

