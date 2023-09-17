from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('organisation', )


class ImageUploadForm(forms.ModelForm):
    # Add a field for custom image name
    custom_name = forms.CharField(max_length=256, required=False, help_text="Leave blank for a generated name.")

    class Meta:
        model = Image
        fields = ['image']  # Only the 'image' field is required

    def save(self, commit=True):
        instance = super().save(commit=False)
        custom_name = self.cleaned_data.get('custom_name')
        
        if custom_name:
            instance.name = custom_name
        else:
            # Generate a default name here, e.g., based on the timestamp
            # You can customize this naming logic as needed
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            instance.name = f'img_{timestamp}'

        if commit:
            instance.save()
        return instance



class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['content']


class UserSearchForm(forms.Form):
    friend_name = forms.CharField(max_length=100, required=False)
    # Add additional search filters as needed