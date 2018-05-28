from django.contrib import admin
from .models import Vacanse
from MainSite import settings
from .forms import VacanseForm

@admin.register(Vacanse)
class VacanseModelAdmin(admin.ModelAdmin):
    form = VacanseForm
    prepopulated_fields = {'title': ('title',)}
    list_display = ('title', 'datetime', 'author')
    list_filter = ('datetime',)

    def save_model(self, request, obj, form, change):
        if not obj.author.id:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()

# Register your models here.
