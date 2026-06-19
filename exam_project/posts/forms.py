from django import forms
from .models import Posts

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content', 'views', 'is_published']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите заголовок поста'
            }),
            
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Введите текст поста...'
            }),
            
            'views': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '1',
                'min': '0'
            }),
            
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
