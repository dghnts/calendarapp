from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm

from .models import CustomUser

class SignupForm(SignupForm,UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")
