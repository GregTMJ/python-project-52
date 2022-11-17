from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class NewUserForm(UserCreationForm):
    """
    Class to handle a form to register a user with
    certain fields that are required
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username",
                  "password1", "password2")

    def save(self, commit=True):
        """
        Saves the form in db if valid
        :return: new user information
        """
        user = super(NewUserForm, self).save(commit=True)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user
