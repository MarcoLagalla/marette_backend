from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MinLengthValidator
from users.forms import UserCreationForm
from backend.account.models import CustomerUser, BusinessUser
from crispy_forms.helper import FormHelper


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', }))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class CustomerUserForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=['%d/%m/%Y'], help_text='Please insert a date int the format '
                                                                       '<em>gg/mm/yyyy</em>')

    class Meta:
        model = CustomerUser
        fields = ['birth_date', 'cellphone_number']


class BusinessUserForm(forms.ModelForm):
    class Meta:
        model = BusinessUser
        fields = ['activity_name', 'city', 'address', 'cap', 'business_number']


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.Meta.fields:
            self[field_name].field.required = True
        self['password1'].field.validators = [MinLengthValidator(6)]
