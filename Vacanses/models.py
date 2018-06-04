from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils import timezone
# Create your models here.

class Vacanse(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='news', default='/organization/default.jpg')
    content = RichTextField(max_length=10000)
    salary = models.DecimalField(max_digits=6, decimal_places=2)
    organization = models.ForeignKey('Vacanses.Organizations', on_delete=models.CASCADE, blank=True, related_name='entries')
    datetime = models.DateTimeField(u'Publication date')
    city = models.CharField(max_length=100)
    tags = TaggableManager()
    is_approved = models.BooleanField(default=False)
    is_promoted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Organizations(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='organization', default='/organization/default.jpg')
    information = RichTextField(max_length=10000)

    def __str__(self):
        return self.title

