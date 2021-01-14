from django import forms
from . models import blog
class edit_blog(forms.ModelForm):
    class Meta:
        model=blog
        fields=('title','dsc')