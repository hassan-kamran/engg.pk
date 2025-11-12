"""
Forms for the companies app - Glassdoor-like company reviews and insights.
"""
from django import forms
from .models import CompanyReview, SalaryReport, CompanyPhoto


class CompanyReviewForm(forms.ModelForm):
    """
    Form for creating and editing company reviews.
    Includes all rating dimensions and review content fields.
    """

    class Meta:
        model = CompanyReview
        fields = [
            'employment_status',
            'job_title',
            'location',
            'employment_length',
            'overall_rating',
            'work_life_balance_rating',
            'culture_values_rating',
            'career_opportunities_rating',
            'compensation_benefits_rating',
            'senior_management_rating',
            'review_title',
            'pros',
            'cons',
            'advice_to_management',
            'recommend_to_friend',
            'ceo_approval',
        ]
        widgets = {
            'employment_status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'job_title': forms.TextInput(attrs={
                'placeholder': 'e.g., Software Engineer, Product Manager',
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g., Karachi, Lahore, Islamabad',
            }),
            'employment_length': forms.NumberInput(attrs={
                'placeholder': '0.0',
                'step': '0.1',
                'min': '0',
                'max': '50',
            }),
            'overall_rating': forms.NumberInput(attrs={
                'min': '1',
                'max': '5',
            }),
            'work_life_balance_rating': forms.NumberInput(attrs={
                'min': '1',
                'max': '5',
            }),
            'culture_values_rating': forms.NumberInput(attrs={
                'min': '1',
                'max': '5',
            }),
            'career_opportunities_rating': forms.NumberInput(attrs={
                'min': '1',
                'max': '5',
            }),
            'compensation_benefits_rating': forms.NumberInput(attrs={
                'min': '1',
                'max': '5',
            }),
            'senior_management_rating': forms.NumberInput(attrs={
                'min': '1',
                'max': '5',
            }),
            'review_title': forms.TextInput(attrs={
                'placeholder': 'Brief summary of your experience',
            }),
            'pros': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'What are the best things about working at this company?',
            }),
            'cons': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'What could be improved?',
            }),
            'advice_to_management': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'What suggestions would you give to management? (Optional)',
            }),
            'recommend_to_friend': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
            'ceo_approval': forms.Select(attrs={
                'class': 'form-select',
            }, choices=[
                ('', 'Prefer not to say'),
                (True, 'Approve'),
                (False, 'Disapprove'),
            ]),
        }
        help_texts = {
            'employment_length': 'How long you worked at the company (in years)',
            'overall_rating': 'Rate from 1 (poor) to 5 (excellent)',
            'pros': 'Be specific about what makes this company a good place to work',
            'cons': 'Be constructive - focus on areas that could be improved',
            'advice_to_management': 'Optional - What would you suggest to improve the company?',
        }

    def clean_employment_length(self):
        """Validate employment length is within reasonable bounds."""
        employment_length = self.cleaned_data.get('employment_length')
        if employment_length is not None:
            if employment_length < 0:
                raise forms.ValidationError('Employment length cannot be negative.')
            if employment_length > 50:
                raise forms.ValidationError('Please enter a valid employment length.')
        return employment_length

    def clean(self):
        """Additional validation for review content."""
        cleaned_data = super().clean()
        pros = cleaned_data.get('pros', '').strip()
        cons = cleaned_data.get('cons', '').strip()

        # Ensure pros and cons have sufficient content
        if pros and len(pros) < 20:
            self.add_error('pros', 'Please provide more detail (at least 20 characters).')

        if cons and len(cons) < 20:
            self.add_error('cons', 'Please provide more detail (at least 20 characters).')

        return cleaned_data


class SalaryReportForm(forms.ModelForm):
    """
    Form for submitting salary information.
    Can be submitted anonymously (submitter is optional).
    """

    is_anonymous = forms.BooleanField(
        required=False,
        initial=False,
        label='Submit Anonymously',
        help_text='Check this box if you want to submit this salary report anonymously',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox',
        })
    )

    class Meta:
        model = SalaryReport
        fields = [
            'job_title',
            'location',
            'experience_years',
            'education_level',
            'employment_type',
            'currency',
            'base_salary',
            'bonus',
            'additional_compensation',
        ]
        widgets = {
            'job_title': forms.TextInput(attrs={
                'placeholder': 'e.g., Senior Software Engineer, Data Scientist',
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g., Karachi, Lahore, Islamabad',
            }),
            'experience_years': forms.NumberInput(attrs={
                'placeholder': '0.0',
                'step': '0.1',
                'min': '0',
                'max': '50',
            }),
            'education_level': forms.Select(attrs={
                'class': 'form-select',
            }),
            'employment_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'currency': forms.Select(attrs={
                'class': 'form-select',
            }),
            'base_salary': forms.NumberInput(attrs={
                'placeholder': 'Annual base salary',
                'step': '1000',
                'min': '0',
            }),
            'bonus': forms.NumberInput(attrs={
                'placeholder': 'Annual bonus (if any)',
                'step': '1000',
                'min': '0',
            }),
            'additional_compensation': forms.NumberInput(attrs={
                'placeholder': 'Stock options, commissions, etc.',
                'step': '1000',
                'min': '0',
            }),
        }
        help_texts = {
            'experience_years': 'Total years of professional experience',
            'base_salary': 'Annual base salary (before bonuses)',
            'bonus': 'Annual bonus amount (optional)',
            'additional_compensation': 'Stock options, equity, commissions, etc. (optional)',
        }

    def clean_experience_years(self):
        """Validate experience years is within reasonable bounds."""
        experience_years = self.cleaned_data.get('experience_years')
        if experience_years is not None:
            if experience_years < 0:
                raise forms.ValidationError('Experience years cannot be negative.')
            if experience_years > 50:
                raise forms.ValidationError('Please enter a valid number of years.')
        return experience_years

    def clean_base_salary(self):
        """Validate base salary is reasonable."""
        base_salary = self.cleaned_data.get('base_salary')
        if base_salary is not None:
            if base_salary < 0:
                raise forms.ValidationError('Salary cannot be negative.')
            if base_salary == 0:
                raise forms.ValidationError('Please enter your base salary.')
            # Check for unreasonably high values (100 million in any currency)
            if base_salary > 100000000:
                raise forms.ValidationError('Please enter a valid salary amount.')
        return base_salary


class CompanyPhotoForm(forms.ModelForm):
    """
    Form for uploading company photos.
    Allows employees to share photos of offices, teams, and events.
    """

    class Meta:
        model = CompanyPhoto
        fields = [
            'photo',
            'caption',
            'photo_type',
        ]
        widgets = {
            'photo': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-file-input',
            }),
            'caption': forms.TextInput(attrs={
                'placeholder': 'Add a caption to describe this photo (optional)',
            }),
            'photo_type': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        help_texts = {
            'photo': 'Upload a photo (JPG, PNG, or GIF format)',
            'caption': 'Describe what this photo shows',
            'photo_type': 'Select the type of photo',
        }

    def clean_photo(self):
        """Validate uploaded photo file."""
        photo = self.cleaned_data.get('photo')

        if photo:
            # Check file size (limit to 5MB)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size cannot exceed 5MB.')

            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            file_name = photo.name.lower()
            if not any(file_name.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError(
                    'Invalid file format. Please upload a JPG, PNG, or GIF image.'
                )

        return photo
