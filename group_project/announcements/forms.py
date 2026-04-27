from django import forms
from .models import Announcement, Comment

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'category', 'end_date', 'is_pinned', 'file', 'image']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишіть коментар...'}),
        }