"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Event

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class EventForm(forms.ModelForm):
    tags = forms.CharField()
    class Meta:
        model = Event
        fields = ('title', 'description', 'latitude', 'longitude', 'session_key')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.fields['description'] = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)
        event.session_key = self.cleaned_data['session_key']
        event.save()
        tags = [tag.strip() for tag in self.cleaned_data['tags'].split(',')]
        event.tags.add(*tags)
        event.save()
        return event
