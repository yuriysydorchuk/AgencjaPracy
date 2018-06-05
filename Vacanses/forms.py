from django import forms
from Vacanses.models import Vacanse, Album, Comment
from django.contrib.auth.models import User


class VacanseForm(forms.ModelForm):

    class Meta:
        model = Vacanse
        fields = ('title', 'content', 'salary', 'city', 'is_approved','datetime', 'tags', 'organization', 'author',)

    def clean_author(self):
        if not self.cleaned_data['author']:
            return User()
        return self.cleaned_data['author']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []

    zip = forms.FileField(required=False)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )