from django import forms
from .models import ProgramReview


class ProgramReviewForm(forms.ModelForm):
    """Form for creating/editing program reviews"""
    class Meta:
        model = ProgramReview
        fields = ['rating', 'content', 'graduation_year']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Share your experience...'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'graduation_year': forms.TextInput(attrs={'placeholder': 'YYYY (optional)'}),
        }
