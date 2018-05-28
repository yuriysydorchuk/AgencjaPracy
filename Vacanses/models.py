from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils import timezone
# Create your models here.

class Vacanse(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='news', default='/users/avatar.png')
    datetime = models.DateTimeField(u'Publication date')
    content = RichTextField(max_length=10000)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, related_name='entries')
    tags = TaggableManager()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title