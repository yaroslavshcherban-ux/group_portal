from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'category', 'end_date', 'is_pinned']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }