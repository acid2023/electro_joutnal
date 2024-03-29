
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget

from network.models import SocialUser


class SocialUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=SelectDateWidget())
    avatar = forms.ImageField(required=False)

    class Meta:
        model = SocialUser
        fields = UserCreationForm.Meta.fields + ('date_of_birth', 'avatar')


class SocialUserForm(forms.ModelForm):
    class Meta:
        model = SocialUser
        fields = ['date_of_birth', 'avatar', 'username', 'first_name', 'last_name', 'email', 'password']