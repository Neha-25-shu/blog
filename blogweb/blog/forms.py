from django import forms
from django.forms import ModelForm
from blog.models import Post
from accounts.models import User
from tinymce.widgets import TinyMCE
from blog.models import Comment

class Contactform(forms.Form):
    countries = [("IN","INDIA"),("USA","AMERICA")]
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
    email = forms.EmailField(required=False)
    phone = forms.RegexField(regex="^[6-9][0-9]{9}$",required=False)
    massage = forms.CharField(max_length=500)
    country = forms.ChoiceField(choices=countries) 

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")
        if email == '' and phone == '':
            raise forms.ValidationError("Atleast email or phone number should be provided" ,code= "invalid")



class CommentForm(forms.ModelForm):
    content = forms.CharField()
    # content = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'md-textarea form-control',
    #     'placeholder': 'comment here ...',
    #     'rows': '4',
    # }))

    class Meta:
        model = Comment
        fields = ('content', )

class Postform(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols':20, 'rows': 10}))
    author = forms.CharField(disabled=True)
    class Meta:
        model = Post
        fields = ["title","content","status","category","image",]


class Searchform(forms.Form):
    search = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'special','placeholder':'search'}))
    