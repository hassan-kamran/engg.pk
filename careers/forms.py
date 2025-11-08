from django import forms
from .models import ExperienceStory


class ExperienceStoryForm(forms.ModelForm):
    """Form for creating/editing experience stories"""
    class Meta:
        model = ExperienceStory
        fields = ['title', 'content', 'current_position', 'years_of_experience']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 12, 'placeholder': 'Share your career journey...'}),
            'current_position': forms.TextInput(attrs={'placeholder': 'e.g., Senior Software Engineer'}),
        }
