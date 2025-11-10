from django import forms
from .models import ForumPost, Reply


class ForumPostForm(forms.ModelForm):
    """Form for creating/editing forum posts"""
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags (e.g., python, django, career)',
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        if tags_str:
            return [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return []


class ReplyForm(forms.ModelForm):
    """Form for creating replies"""
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your reply...'}),
        }
