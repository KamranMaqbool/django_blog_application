from django import forms

from .models import Comment

class EmailForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    to = forms.EmailField(label='Recipient Email')
    comments = forms.CharField(
        widget=forms.Textarea,
        label='Comments',
        help_text='Enter your comments here.'
    )
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'body': 'Comment',
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search...'})
    )
    
    def clean_query(self):
        query = self.cleaned_data.get('query')
        if not query:
            raise forms.ValidationError('This field cannot be empty.')
        return query