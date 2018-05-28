from django import forms
from Vacanses.models import Vacanse
from django.contrib.auth.models import User


class VacanseForm(forms.ModelForm):

    class Meta:
        model = Vacanse
        fields = ('title', 'image', 'content', 'datetime', 'tags', 'author')

    def clean_author(self):
        if not self.cleaned_data['author']:
            return User()
        return self.cleaned_data['author']