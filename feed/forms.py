from django import forms
from .models import FeedPost, Comment


class FeedPostForm(forms.ModelForm):
    """Form for creating/editing feed posts"""
    topics = forms.CharField(
        required=False,
        help_text='Comma-separated topics (e.g., software, career, industry)',
        widget=forms.TextInput(attrs={'placeholder': 'software, career, industry'})
    )

    class Meta:
        model = FeedPost
        fields = ['post_type', 'title', 'content', 'topics', 'external_link']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
            'external_link': forms.URLInput(attrs={'placeholder': 'https://example.com (optional)'}),
        }

    def clean_topics(self):
        topics_str = self.cleaned_data.get('topics', '')
        if topics_str:
            return [topic.strip() for topic in topics_str.split(',') if topic.strip()]
        return []


class CommentForm(forms.ModelForm):
    """Form for creating comments"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share your thoughts...',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent'
            }),
        }
