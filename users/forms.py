from django import froms
from alllauth.account.forms import SignupForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")
