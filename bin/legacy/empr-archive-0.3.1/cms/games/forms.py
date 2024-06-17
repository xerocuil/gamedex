from django import forms
from django.forms import CheckboxInput, FileInput, HiddenInput, Select, SelectMultiple, Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from .models import Collection, Game, Genre, Platform, Tag

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={
                'required': True,
            }),
            'tags': SelectMultiple(attrs={'size': '8'})
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


