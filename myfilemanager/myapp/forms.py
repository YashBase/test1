from django import forms
from .models import Project
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class ProjectForm(forms.ModelForm):
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
        label="Assign Users"
    )

    class Meta:
        model = Project
        fields = ['name', 'assigned_users']

        


from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role',)


class UploadFileForm(forms.Form):
    file = forms.FileField()
