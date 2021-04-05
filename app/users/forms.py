from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserRegistrationForm(forms.ModelForm):
    new_password = forms.CharField(
        label=_("New Password"), widget=forms.PasswordInput, strip=False)

    def save(self, commit=True):
        is_new_user = self.instance.pk is None

        user = super(UserRegistrationForm, self).save(commit)

        # new users should be made active by default
        if is_new_user:
            user.is_active = True

        # if we had a new password set, use it
        new_pass = self.cleaned_data['new_password']
        if new_pass:
            user.set_password(new_pass)
            if commit:
                user.save()

        return user

    class Meta:
        model = User
        fields = (
            'username', 'new_password', 'first_name',
            'last_name', 'email'
        )
