from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
import uuid
# Create your models here.

class Vacanse(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField(max_length=10000)
    salary = models.DecimalField(max_digits=6, decimal_places=2)
    organization = models.ForeignKey('Vacanses.Organizations', on_delete=models.CASCADE, blank=True, related_name='entries')
    datetime = models.DateTimeField(u'Publication date')
    city = models.CharField(max_length=100)
    tags = TaggableManager()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, related_name='entries')
    is_approved = models.BooleanField(default=False)
    is_promoted = models.BooleanField(default=False)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Organizations(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='organization', default='/organization/default.jpg')
    information = RichTextField(max_length=10000)

    def __str__(self):
        return self.name


class Comment(models.Model):
    Vacanse = models.ForeignKey('Vacanses.Vacanse', related_name='comments', on_delete=models.CASCADE,)
    author = models.CharField(max_length=45)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Album(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=1024)
    thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(300)], format='JPEG',
                                options={'quality': 90})
    Vacanse = models.ForeignKey('Vacanse',on_delete=models.CASCADE)
    tags = TaggableManager()
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class AlbumImage(models.Model):
    image = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(1280)], format='JPEG',
                                options={'quality': 70})
    thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(300)], format='JPEG',
                                options={'quality': 80})
    album = models.ForeignKey('album',on_delete=models.CASCADE)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)