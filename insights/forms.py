from django import forms
from .models import IndustryInsight


class IndustryInsightForm(forms.ModelForm):
    """Form for creating/editing industry insights"""
    topics = forms.CharField(
        required=False,
        help_text='Comma-separated topics',
        widget=forms.TextInput(attrs={'placeholder': 'topic1, topic2, topic3'})
    )

    class Meta:
        model = IndustryInsight
        fields = ['title', 'industry', 'discipline', 'content', 'topics']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15}),
        }

    def clean_topics(self):
        topics_str = self.cleaned_data.get('topics', '')
        if topics_str:
            return [topic.strip() for topic in topics_str.split(',') if topic.strip()]
        return []
