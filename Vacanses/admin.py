from django.contrib import admin
from .models import Vacanse, Comment, Organizations, Album, AlbumImage
from MainSite import settings
from .forms import VacanseForm, AlbumForm, CommentForm
from django.core.files.base import ContentFile
import uuid
import zipfile
from datetime import datetime
from PIL import Image

class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = True
    verbose_name_plural = "Comment"
    fieldsets = (
        (None, {
            'fields': ('text', 'author', 'approved_comment',)
        }),
    )
    extra = 0


@admin.register(Vacanse)
class VacanseModelAdmin(admin.ModelAdmin):
    form = VacanseForm
    prepopulated_fields = {'title': ('title',)}
    list_display = ('title', 'datetime', 'organization')
    list_filter = ('datetime',)
    inlines = (CommentInline,)

    def save_model(self, request, obj, form, change):
        if not obj.author.id:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    readonly_fields = ('author',)


@admin.register(Organizations)
class OrganizationsModelAdmin(admin.ModelAdmin):
    list_filter =('name',)


class AlbumImageInline(admin.StackedInline):
    model = AlbumImage
    can_delete = True
    verbose_name_plural = "Images"
    fieldsets = (
        (None, {
            'fields': ('image', 'thumb')
        }),
    )
    extra = 0


@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    form = AlbumForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'thumb')
    list_filter = ('created',)
    inlines = (AlbumImageInline,)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            album = form.save(commit=False)
            album.modified = datetime.now()
            album.save()

            if form.cleaned_data['zip'] is not None:
                zip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip.namelist()):
                    data = zip.read(filename)
                    contentfile = ContentFile(data)

                    img = AlbumImage()
                    img.album = album
                    img.alt = filename
                    filename = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])
                    img.image.save(filename, contentfile)

                    filepath = '{0}/albums/{1}'.format(settings.MEDIA_ROOT, filename)
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    img.thumb.save('thumb-{0}'.format(filename), contentfile)
                    img.save()
                zip.close()
            super(AlbumModelAdmin, self).save_model(request, obj, form, change)


# In case image should be removed from album.
@admin.register(AlbumImage)
class AlbumImageModelAdmin(admin.ModelAdmin):
    list_display = ('alt', 'album')
    list_filter = ('album', 'created')


# Register your models here.
