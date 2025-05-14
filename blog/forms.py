from django import forms


class EmailForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    to = forms.EmailField(label='Recipient Email')
    comments = forms.CharField(
        widget=forms.Textarea,
        label='Comments',
        help_text='Enter your comments here.'
    )