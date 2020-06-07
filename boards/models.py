import math
from django.db import models
from django.utils.html import mark_safe
from markdown import markdown
from django.utils.text import Truncator
from django.contrib.auth.models import User

class Board(models.Model) :
    name = models.CharField(max_length = 30, unique = True)
    description = models.CharField(max_length = 100)

    def __str__(self) :
        return self.name

    def get_posts_count(self) :
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self) :
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model) :
    subject = models.CharField(max_length = 255)
    last_updated = models.DateTimeField(auto_now_add = True)
    board = models.ForeignKey(Board, related_name = 'topics', on_delete = models.CASCADE)
    starter = models.ForeignKey(User, related_name = 'topics', on_delete = models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self) :
        return self.subject

    def get_page_count(self):
        count = self.posts.order_by('-created_at')[:self.posts.count() -1].count()
        pages = count / 5
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count =self.get_page_count()
        return count > 5

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages():
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_replies(self):
        return self.posts.order_by('-created_at')[:10 if (self.posts.count() - 1) > 10 else (self.posts.count() - 1) ]

    def main_post(self):
        return self.posts.order_by('-created_at')[self.posts.count() -1:]
    

class Post(models.Model) :
    message = models.TextField(max_length = 4000)
    topic = models.ForeignKey(Topic, related_name = 'posts', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(null = True)
    created_by = models.ForeignKey(User, related_name = 'posts', on_delete = models.CASCADE)
    updated_by = models.ForeignKey(User, null = True, related_name = '+', on_delete = models.CASCADE)

    def __str__(self) :
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
